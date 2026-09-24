from datetime import datetime, timedelta, timezone
from astra import Decision, ExecutionRequest, Policy, evaluate

NOW = datetime(2026, 1, 1, tzinfo=timezone.utc)

def policy(**overrides):
    values = dict(
        allowed_actions=frozenset({"mine"}),
        allowed_capabilities=frozenset({"compute"}),
        allowed_actors=frozenset({"agent-1"}),
        allowed_resources=frozenset({"worker-1"}),
        authority_scope={"environment": "authorized"},
        resource_limits={"cpu": 4},
        expires_at=NOW + timedelta(hours=1),
    )
    values.update(overrides)
    return Policy(**values)

def request(**overrides):
    values = dict(
        actor="agent-1",
        capability="compute",
        action="mine",
        resource="worker-1",
        requested_scope={"environment": "authorized"},
        requested_resources={"cpu": 2},
        now=NOW,
    )
    values.update(overrides)
    return ExecutionRequest(**values)

def test_authorized_request_allows():
    decision, reasons = evaluate(request(), policy())
    assert decision is Decision.ALLOW
    assert reasons == ["authorized"]

def test_capability_without_authority_is_blocked():
    decision, reasons = evaluate(request(requested_scope={"environment": "untrusted"}), policy())
    assert decision is Decision.BLOCK
    assert "scope_outside_authority" in reasons

def test_expired_authority_is_blocked():
    decision, reasons = evaluate(request(now=NOW + timedelta(hours=2)), policy())
    assert decision is Decision.BLOCK
    assert "authorization_expired" in reasons

def test_resource_overage_is_blocked():
    decision, reasons = evaluate(request(requested_resources={"cpu": 8}), policy())
    assert decision is Decision.BLOCK
    assert "resource_limit_exceeded:cpu" in reasons

def test_review_action_is_not_automatic_execution():
    decision, reasons = evaluate(
        request(action="withdraw"),
        policy(
            allowed_actions=frozenset({"mine", "withdraw"}),
            review_actions=frozenset({"withdraw"}),
        ),
    )
    assert decision is Decision.REVIEW
    assert reasons == ["human_review_required"]
