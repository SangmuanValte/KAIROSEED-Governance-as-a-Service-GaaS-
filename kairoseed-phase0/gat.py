"""GAT: authorization-only worker for the synthetic Phase 0 testbed.

HMAC signatures authenticate fixture values, not a real human principal,
trusted hardware, or production authorization.
"""
from __future__ import annotations

import hashlib
import hmac
import json
import time


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def digest(value):
    return hashlib.sha256(canonical(value).encode("utf-8")).hexdigest()


def mac(value, key):
    return hmac.new(key, canonical(value).encode("utf-8"), hashlib.sha256).hexdigest()


def verify_token(token, principal_key):
    if not isinstance(token, dict):
        return False
    fields = {k: v for k, v in token.items() if k != "signature"}
    sig = token.get("signature")
    return isinstance(sig, str) and hmac.compare_digest(mac(fields, principal_key), sig)


def check_scope(token, proposal, scope):
    if not isinstance(token, dict) or not isinstance(proposal, dict):
        return False
    if token.get("scope_digest") != digest(scope):
        return False
    for field in ("principal_id", "purpose"):
        if token.get(field) != scope[field] or proposal.get(field) != scope[field]:
            return False
    if not proposal.get("request_id") or not isinstance(proposal.get("request_id"), str):
        return False
    if proposal.get("resource") != token.get("resource"):
        return False
    if proposal.get("action") != token.get("action"):
        return False
    resource = proposal.get("resource")
    if resource not in scope["allowed_resources"]:
        return False
    if proposal.get("action") not in scope["allowed_actions"]:
        return False
    return proposal.get("expected_delta") == {resource: scope["allowed_delta"][resource]}


def check_time(token, scope):
    """Service wall clock for deterministic expiry semantics; NOT attested time."""
    try:
        now_ns = time.time_ns()
        issued = token["issued_ns"]
        expires = token["expires_ns"]
        if not isinstance(issued, int) or not isinstance(expires, int):
            return False
        return issued <= now_ns < expires and 0 < expires - issued <= scope["max_duration_ms"] * 1_000_000
    except (KeyError, TypeError, ValueError):
        return False


def check_revocation(token, ledger_query):
    """Read fresh data from the separate ledger service, fail closed on outage."""
    try:
        ledger_query.send({"op": "query_revoked", "token_id": token["token_id"]})
        if not ledger_query.poll(2.0):
            return False
        reply = ledger_query.recv()
        return reply.get("ok") is True and reply.get("revoked") is False
    except (KeyError, TypeError, AttributeError, EOFError, BrokenPipeError, OSError):
        return False


def make_receipt(proposal, token, decision, reason, scope, receipt_key):
    body = {
        "request_id": proposal.get("request_id"),
        "proposal_hash": digest(proposal),
        "token_id": token.get("token_id") if isinstance(token, dict) else None,
        "decision": decision,
        "reason": reason,
        "scope_digest": digest(scope),
        "issued_ns": time.time_ns(),
        "expires_ns": token.get("expires_ns") if isinstance(token, dict) else None,
    }
    return {**body, "signature": mac(body, receipt_key)}


def gat_worker(request_conn, ledger_query, scope_path, principal_key, receipt_key):
    with open(scope_path, encoding="utf-8") as f:
        scope = json.load(f)
    while True:
        try:
            request = request_conn.recv()
        except EOFError:
            return
        if request.get("op") == "stop":
            request_conn.send({"ok": True})
            return
        if request.get("op") != "authorize":
            request_conn.send({"ok": False, "reason": "DENY_UNKNOWN_OPERATION"})
            continue
        proposal = request.get("proposal")
        token = request.get("token")
        if not isinstance(proposal, dict):
            request_conn.send({"ok": False, "reason": "DENY_INVALID_PROPOSAL"})
            continue

        # Failure reasons are audit metadata; no decision grants execution itself.
        if token is None:
            reason = "DENY_MISSING_GRANT"
        elif not verify_token(token, principal_key):
            reason = "DENY_INVALID_SIGNATURE"
        elif not check_scope(token, proposal, scope):
            reason = "DENY_SCOPE_MISMATCH"
        elif not check_time(token, scope):
            reason = "DENY_EXPIRED_GRANT"
        elif not check_revocation(token, ledger_query):
            reason = "DENY_REVOKED_OR_LEDGER_UNAVAILABLE"
        else:
            reason = "ALLOW"
        decision = "ALLOW" if reason == "ALLOW" else "DENY"
        receipt = make_receipt(proposal, token, decision, reason, scope, receipt_key)
        request_conn.send({"ok": True, "receipt": receipt})
