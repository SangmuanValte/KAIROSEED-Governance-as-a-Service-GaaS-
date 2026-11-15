"""Phase 0 research auditor: reads ledger and produces a scoped finding.

No execution capability; this is an executable model check, NOT a theorem
checker, third-party audit, or independent security attestation.
"""
from __future__ import annotations

import json
from pathlib import Path

from ledger import Ledger


def assert_claim_le_evidence(claim_atoms, evidence_atoms, scope_atoms):
    """Compare declared effect atoms under a fixed synthetic scope."""
    claims, evidence, scope = map(set, (claim_atoms, evidence_atoms, scope_atoms))
    return claims.issubset(evidence) and evidence.issubset(scope)


def audit_ledger(ledger_path, scope_path):
    source = Ledger(ledger_path)
    if not source.verify_chain():
        return {"status": "BROKEN_CHAIN", "valid": False, "checked": 0}
    scope = json.loads(Path(scope_path).read_text(encoding="utf-8"))
    allowed = {"share:" + target for target in scope["allowed_resources"]}
    checked = 0
    for item in source.records():
        body = item["body"]
        if body.get("event") == "REVOKE":
            continue
        if body.get("event") != "CASE":
            return {"status": "UNKNOWN_EVENT", "valid": False, "checked": checked}
        claimed = body.get("claimed_atoms")
        observed = body.get("observed_atoms")
        verdict = body.get("decision")
        delta = body.get("observed_delta")
        if not isinstance(claimed, list) or not isinstance(observed, list):
            return {"status": "INVALID_CLAIM_EVIDENCE", "valid": False, "checked": checked}
        if not assert_claim_le_evidence(claimed, observed, allowed):
            return {"status": "CLAIM_SCOPE_MISMATCH", "valid": False, "checked": checked}
        if verdict == "DENY" and (delta != {} or observed or claimed):
            return {"status": "DENIAL_STATE_MISMATCH", "valid": False, "checked": checked}
        if verdict == "ALLOW" and (
            len(observed) != 1 or not delta or
            list(delta.values()) != [True]
        ):
            return {"status": "ALLOW_STATE_MISMATCH", "valid": False, "checked": checked}
        if body.get("observer_verdict") != "MATCH":
            return {"status": "OBSERVER_MISMATCH", "valid": False, "checked": checked}
        checked += 1
    return {"status": "SCOPED_DATA_CONSISTENCY_OK", "valid": True, "checked": checked}


def audit_report(ledger_path, scope_path, output_path):
    result = audit_ledger(ledger_path, scope_path)
    Path(output_path).write_text(
        json.dumps(result, sort_keys=True, indent=2) + "\n", encoding="utf-8"
    )
    return result


def audit_worker(request_channel, ledger_path, scope_path):
    """Dedicated read-only audit process; reports on file content, never modifies it."""
    while True:
        try:
            message = request_channel.recv()
        except EOFError:
            return
        if message.get("op") == "stop":
            request_channel.send({"ok": True})
            return
        if message.get("op") != "audit":
            request_channel.send({"ok": False, "status": "UNKNOWN_AUDIT_REQUEST"})
            continue
        target = message.get("ledger_path", ledger_path)
        result = audit_ledger(target, scope_path)
        request_channel.send(result)
