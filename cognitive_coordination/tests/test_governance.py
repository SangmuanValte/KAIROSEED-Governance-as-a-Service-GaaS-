from cognitive_coordination.governance import govern


def proposal(**overrides):
    value = {
        "proposal_id": "p-001",
        "objective": "test",
        "scope": "research",
        "action": "analyze",
        "risk_class": "low",
        "evidence_required": ["result"],
    }
    value.update(overrides)
    return value


def test_admit_authorized_proposal():
    assert govern(proposal(), "research", {"analyze"}).status == "ADMIT"


def test_deny_unauthorized_action():
    assert govern(proposal(action="publish"), "research", {"analyze"}).status == "DENY"


def test_deny_scope_mismatch():
    assert govern(proposal(scope="production"), "research", {"analyze"}).status == "DENY"


def test_deny_missing_evidence_requirements():
    assert govern(proposal(evidence_required=[]), "research", {"analyze"}).status == "DENY"
