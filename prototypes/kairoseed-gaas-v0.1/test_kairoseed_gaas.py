from kairoseed_gaas import ActionProposal, Decision, EvidenceLedger, govern


def test_authorized_action_allows_and_records_evidence():
    ledger = EvidenceLedger()
    result = govern(ActionProposal("agent-1", "read_report", "authorized", "v0.1"), ledger)
    assert result.decision is Decision.ALLOW
    assert result.evidence_initialized
    assert len(ledger.records) == 1


def test_unauthorized_action_blocks():
    ledger = EvidenceLedger()
    result = govern(ActionProposal("agent-1", "send_message", "unauthorized", "v0.1"), ledger)
    assert result.decision is Decision.BLOCK
    assert result.reason == "authority_invalid"


def test_invalid_policy_blocks():
    ledger = EvidenceLedger()
    result = govern(ActionProposal("agent-1", "read_report", "authorized", "v9"), ledger)
    assert result.decision is Decision.BLOCK
    assert result.reason == "unsupported_policy_version"


def test_validation_failure_blocks():
    ledger = EvidenceLedger()
    result = govern(ActionProposal("agent-1", "read_report", "authorized", "v0.1", validation_passed=False), ledger)
    assert result.decision is Decision.BLOCK
    assert result.reason == "validation_failed"


def test_evidence_chain_links_records():
    ledger = EvidenceLedger()
    proposal = ActionProposal("agent-1", "read_report", "authorized", "v0.1")
    govern(proposal, ledger)
    govern(proposal, ledger)
    assert ledger.records[1]["previous_hash"] == ledger.records[0]["record_hash"]
