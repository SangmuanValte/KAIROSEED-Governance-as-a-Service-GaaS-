"""Synthetic PEP and mock-effect worker; not a seccomp/eBPF sandbox.

A fixture process owns synthetic booleans, with a dedicated PEP apply channel
and an independent read-only observer channel. IPC possession is assumed secure
ONLY inside the laboratory harness. No OS enforcement is claimed.
"""
from __future__ import annotations

import hashlib
import hmac
import json
import time
from multiprocessing.connection import wait


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def digest(value):
    return hashlib.sha256(canonical(value).encode("utf-8")).hexdigest()


def mac(value, key):
    return hmac.new(key, canonical(value).encode("utf-8"), hashlib.sha256).hexdigest()


def verify_gat_receipt(receipt, proposal, scope, receipt_key):
    if not isinstance(receipt, dict) or not isinstance(proposal, dict):
        return False
    try:
        signature = receipt["signature"]
        body = {k: v for k, v in receipt.items() if k != "signature"}
        if not isinstance(signature, str):
            return False
        if not hmac.compare_digest(signature, mac(body, receipt_key)):
            return False
        if receipt["decision"] != "ALLOW" or receipt["reason"] != "ALLOW":
            return False
        if receipt["request_id"] != proposal["request_id"]:
            return False
        if receipt["proposal_hash"] != digest(proposal):
            return False
        if receipt["scope_digest"] != digest(scope):
            return False
        current = time.time_ns()
        if not (receipt["issued_ns"] <= current < receipt["expires_ns"]):
            return False
        if current - receipt["issued_ns"] > 5_000_000_000:
            return False
        resource = proposal["resource"]
        if resource not in scope["allowed_resources"]:
            return False
        if proposal["action"] not in scope["allowed_actions"]:
            return False
        return proposal["expected_delta"] == {resource: scope["allowed_delta"][resource]}
    except (KeyError, TypeError, ValueError):
        return False


def jireh_trap():
    """A simulated denial hook ONLY. Never represented as syscall trapping."""
    raise SystemExit(73)


def fixture_worker(apply_channel, observer_channel, scope, receipt_key):
    """Own mock protected state; observer channel supports snapshots only."""
    state = dict(scope["fixture_baseline"])
    channels = {apply_channel: "apply", observer_channel: "observe"}
    while channels:
        for conn in wait(list(channels)):
            try:
                request = conn.recv()
            except EOFError:
                channels.pop(conn, None)
                continue
            op = request.get("op")
            if channels[conn] == "observe" and op == "snapshot":
                response = {"ok": True, "state": dict(state)}
            elif channels[conn] == "apply" and op == "share":
                proposal = request.get("proposal")
                receipt = request.get("receipt")
                if not verify_gat_receipt(receipt, proposal, scope, receipt_key):
                    response = {"ok": False, "reason": "DENY_INVALID_RECEIPT"}
                else:
                    resource = proposal["resource"]
                    state[resource] = True
                    response = {"ok": True, "result": "SYNTHETIC_SHARED"}
            elif op == "stop":
                conn.send({"ok": True})
                return
            else:
                response = {"ok": False, "reason": "DENY_UNKNOWN_CHANNEL_OPERATION"}
            try:
                conn.send(response)
            except (EOFError, BrokenPipeError, OSError):
                channels.pop(conn, None)


def execute_via_pep(proposal, token, gat_channel, fixture_channel, scope, receipt_key):
    """Only this synthetic boundary can submit an apply command to fixture."""
    if not isinstance(proposal, dict):
        return {"decision": "DENY", "reason": "DENY_INVALID_PROPOSAL"}
    try:
        gat_channel.send({"op": "authorize", "proposal": proposal, "token": token})
        if not gat_channel.poll(0.8):
            return {"decision": "DENY", "reason": "DENY_GAT_UNAVAILABLE"}
        answer = gat_channel.recv()
    except (EOFError, BrokenPipeError, OSError):
        return {"decision": "DENY", "reason": "DENY_GAT_UNAVAILABLE"}
    receipt = answer.get("receipt") if isinstance(answer, dict) else None
    if receipt is None:
        return {"decision": "DENY", "reason": "DENY_GAT_UNAVAILABLE"}
    if receipt.get("decision") != "ALLOW":
        return {"decision": "DENY", "reason": receipt.get("reason", "DENY")}
    if not verify_gat_receipt(receipt, proposal, scope, receipt_key):
        return {"decision": "DENY", "reason": "DENY_INVALID_RECEIPT"}
    try:
        fixture_channel.send({"op": "share", "proposal": proposal, "receipt": receipt})
        if not fixture_channel.poll(0.8):
            return {"decision": "DENY", "reason": "DENY_FIXTURE_TIMEOUT"}
        result = fixture_channel.recv()
    except (EOFError, BrokenPipeError, OSError):
        return {"decision": "DENY", "reason": "DENY_FIXTURE_UNAVAILABLE"}
    if not result.get("ok"):
        return {"decision": "DENY", "reason": result.get("reason", "DENY_FIXTURE")}
    return {"decision": "ALLOW", "reason": "ALLOW", "receipt": receipt}


def pep_worker(request_channel, gat_channel, fixture_channel, scope, receipt_key):
    while True:
        try:
            request = request_channel.recv()
        except EOFError:
            return
        if request.get("op") == "stop":
            request_channel.send({"ok": True})
            return
        if request.get("op") == "submit":
            result = execute_via_pep(
                request.get("proposal"), request.get("token"), gat_channel,
                fixture_channel, scope, receipt_key
            )
        else:
            result = {"decision": "DENY", "reason": "DENY_BYPASS_TRAPPED"}
        request_channel.send(result)
