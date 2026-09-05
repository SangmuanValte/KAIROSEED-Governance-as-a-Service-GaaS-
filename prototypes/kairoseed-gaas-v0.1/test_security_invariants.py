import json
from dataclasses import asdict
from hashlib import sha256

from kairoseed_gaas import ActionProposal, Decision, EvidenceLedger, govern, proposal_hash


def test_capability_is_fail_closed():
    ledger = EvidenceLedger()
    result = govern(
        ActionProposal("agent-1", "read_report", "authorized", "v0.1", capability=False),
        ledger,
    )
    assert result.decision is Decision.BLOCK
    assert result.reason == "capability_missing"


def test_empty_intent_is_fail_closed():
    ledger = EvidenceLedger()
    result = govern(ActionProposal("agent-1", "   ", "authorized", "v0.1"), ledger)
    assert result.decision is Decision.BLOCK
    assert result.reason == "intent_missing"


def test_allow_requires_all_required_predicates():
    baseline = ActionProposal("agent-1", "read_report", "authorized", "v0.1")
    predicates = [
        ActionProposal("agent-1", "read_report", "authorized", "v0.1", capability=False),
        ActionProposal("agent-1", "", "authorized", "v0.1"),
        ActionProposal("agent-1", "read_report", "unauthorized", "v0.1"),
        ActionProposal("agent-1", "read_report", "authorized", "unsupported"),
        ActionProposal("agent-1", "read_report", "authorized", "v0.1", validation_passed=False),
    ]

    assert govern(baseline, EvidenceLedger()).decision is Decision.ALLOW
    for proposal in predicates:
        assert govern(proposal, EvidenceLedger()).decision is Decision.BLOCK


def test_proposal_hash_is_deterministic():
    proposal = ActionProposal("agent-1", "read_report", "authorized", "v0.1")
    assert proposal_hash(proposal) == proposal_hash(proposal)


def test_evidence_record_hash_reconstructs():
    ledger = EvidenceLedger()
    proposal = ActionProposal("agent-1", "read_report", "authorized", "v0.1")
    govern(proposal, ledger)
    record = ledger.records[0]

    payload = {key: value for key, value in record.items() if key != "record_hash"}
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    expected = sha256(canonical.encode()).hexdigest()
    assert record["record_hash"] == expected


def test_evidence_chain_detects_modified_previous_record():
    ledger = EvidenceLedger()
    proposal = ActionProposal("agent-1", "read_report", "authorized", "v0.1")
    govern(proposal, ledger)
    govern(proposal, ledger)

    original_hash = ledger.records[0]["record_hash"]
    ledger.records[0]["reason"] = "tampered"
    payload = {key: value for key, value in ledger.records[0].items() if key != "record_hash"}
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    recomputed = sha256(canonical.encode()).hexdigest()

    assert recomputed != original_hash
    assert ledger.records[1]["previous_hash"] == original_hash
