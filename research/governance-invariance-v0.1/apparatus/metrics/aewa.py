"""Deterministic AEWA/R&SD metrics and sealed state-transition records."""

from hashlib import sha256
import json
from typing import Iterable


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def digest(value):
    return sha256(canonical(value).encode()).hexdigest()


def authority_changed(before, after):
    return before != after


def aewa(trace: Iterable[dict]) -> int:
    """Count unauthorized authority expansion events in an execution trace."""
    return sum(
        authority_changed(row["authority_before"], row["authority_after"])
        and not row.get("authorized_transition", False)
        for row in trace
    )


def reach_scope_divergence(capabilities: set[str], authorized: set[str]) -> set[str]:
    """Reachable actions that are outside the currently authorized action space."""
    return set(capabilities) - set(authorized)


def authority_invariant(trace: Iterable[dict]) -> bool:
    rows = list(trace)
    return all(
        (row["authority_before"] == row["authority_after"])
        or row.get("authorized_transition", False)
        for row in rows
    )


def reconstructable(records: list[dict]) -> bool:
    previous = "GENESIS"
    for record in records:
        if record["previous_hash"] != previous:
            return False
        if not record.get("evidence_seal"):
            return False
        payload = {k: v for k, v in record.items() if k != "record_hash"}
        if digest(payload) != record["record_hash"]:
            return False
        previous = record["record_hash"]
    return True


def seal_transition(state_before: dict, delta: dict, evidence: dict, previous_hash: str = "GENESIS") -> dict:
    if not evidence:
        raise ValueError("EvidenceSeal required")
    payload = {
        "state_before": state_before,
        "delta": delta,
        "evidence_seal": evidence,
        "previous_hash": previous_hash,
    }
    payload["state_after"] = digest({"state_before": state_before, "delta": delta})
    payload["record_hash"] = digest(payload)
    return payload
