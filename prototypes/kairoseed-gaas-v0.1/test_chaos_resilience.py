import tempfile
from concurrent.futures import ThreadPoolExecutor

import pytest

from kairoseed_gaas import ActionProposal, Decision, EvidenceLedger, govern


def _proposal(**overrides):
    values = {
        "agent_id": "chaos-agent",
        "intent": "run_controlled_experiment",
        "authority_scope": "authorized",
        "policy_version": "v0.1",
    }
    values.update(overrides)
    return ActionProposal(**values)


def test_authority_failure_fails_closed_and_records():
    ledger = EvidenceLedger()
    result = govern(_proposal(authority_scope="unavailable"), ledger)
    assert result.decision is Decision.BLOCK
    assert result.reason == "authority_invalid"
    assert ledger.verify_chain()
    assert ledger.records[-1]["decision"] == Decision.BLOCK.value


def test_policy_failure_fails_closed_and_records():
    ledger = EvidenceLedger()
    result = govern(_proposal(policy_version="unavailable"), ledger)
    assert result.decision is Decision.BLOCK
    assert result.reason == "unsupported_policy_version"
    assert ledger.verify_chain()


def test_evidence_failure_prevents_unguarded_execution():
    class BrokenLedger:
        def append(self, *args, **kwargs):
            raise OSError("evidence store unavailable")

    with pytest.raises(OSError):
        govern(_proposal(), BrokenLedger())


def test_verification_failure_blocks_before_execution():
    ledger = EvidenceLedger()
    result = govern(_proposal(validation_passed=False), ledger)
    assert result.decision is Decision.BLOCK
    assert result.reason == "validation_failed"
    assert ledger.verify_chain()


def test_concurrent_pressure_preserves_evidence_chain():
    ledger = EvidenceLedger()
    proposals = [_proposal(agent_id=f"agent-{i}") for i in range(32)]

    with ThreadPoolExecutor(max_workers=8) as pool:
        results = list(pool.map(lambda p: govern(p, ledger), proposals))

    assert all(result.decision is Decision.ALLOW for result in results)
    assert len(ledger.records) == len(proposals)
    assert ledger.verify_chain()


def test_recovery_reconstructs_valid_chain_after_restart():
    with tempfile.TemporaryDirectory() as directory:
        path = f"{directory}/chaos.sqlite3"
        first = EvidenceLedger(path)
        blocked = govern(_proposal(authority_scope="unavailable"), first)
        allowed = govern(_proposal(), first)
        assert blocked.decision is Decision.BLOCK
        assert allowed.decision is Decision.ALLOW
        first.close()

        recovered = EvidenceLedger(path)
        assert len(recovered.records) == 2
        assert recovered.verify_chain()
        assert recovered.records[0]["decision"] == Decision.BLOCK.value
        assert recovered.records[1]["decision"] == Decision.ALLOW.value
        recovered.close()
