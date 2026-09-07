from cognitive_coordination.evidence import record
from cognitive_coordination.execution import execute
from cognitive_coordination.governance import govern
from cognitive_coordination.validation import validate


def proposal():
    return {
        "proposal_id": "p-002",
        "objective": "test execution",
        "scope": "research",
        "action": "analyze",
        "risk_class": "low",
        "evidence_required": ["result"],
    }


def test_denied_action_never_executes():
    p = proposal() | {"action": "publish"}
    d = govern(p, "research", {"analyze"})
    result = execute(p, d)
    evidence = record(p, d.status, result, validate(result, p))
    assert result["performed"] is False
    assert evidence["proven"] is False


def test_admitted_action_validates_and_is_recorded():
    p = proposal()
    d = govern(p, "research", {"analyze"})
    result = execute(p, d)
    evidence = record(p, d.status, result, validate(result, p))
    assert result["performed"] is True
    assert evidence["proven"] is True
