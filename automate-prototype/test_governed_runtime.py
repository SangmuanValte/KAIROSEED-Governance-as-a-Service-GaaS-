import json

from governed_runtime import Proposal, execute, outcome_verified


def test_denied_request_returns_403_semantics_and_does_not_mutate_state():
    state = {"protected_resource": "unchanged"}
    before = dict(state)

    evidence = execute(
        Proposal("prop-deny", "agent-1", "write_demo_state", "protected_resource"),
        state,
        allowed_actions=set(),
    )

    assert state == before
    assert evidence.requested is True
    assert evidence.authorized is False
    assert evidence.executed is False
    assert evidence.committed is False
    assert evidence.outcome == "denied"
    assert evidence.state_before_hash == evidence.state_after_hash


def test_authorized_execution_validates_and_emits_outcome_verified():
    state = {"protected_resource": "unchanged"}

    evidence = execute(
        Proposal("prop-admit", "agent-1", "write_demo_state", "protected_resource"),
        state,
        allowed_actions={"write_demo_state"},
    )

    assert state["protected_resource"] == "updated"
    assert evidence.authorized is True
    assert evidence.executed is True
    assert evidence.validated is True
    assert evidence.committed is True

    settlement = outcome_verified(evidence)
    assert settlement["event"] == "OUTCOME_VERIFIED"
    assert settlement["billable"] is True


def test_denied_evidence_cannot_settle():
    state = {"protected_resource": "unchanged"}
    evidence = execute(
        Proposal("prop-deny-2", "agent-2", "write_demo_state", "protected_resource"),
        state,
        allowed_actions=set(),
    )

    try:
        outcome_verified(evidence)
    except ValueError:
        pass
    else:
        raise AssertionError("Denied execution must never become OUTCOME_VERIFIED")
