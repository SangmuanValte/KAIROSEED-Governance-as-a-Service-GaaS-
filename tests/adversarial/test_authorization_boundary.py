from datetime import datetime, timedelta, timezone

from astra.core import Decision, ExecutionRequest, Policy, evaluate

NOW = datetime(2026, 1, 1, tzinfo=timezone.utc)


def base_policy(**overrides):
    values = dict(
        allowed_actions=frozenset({"read"}),
        allowed_capabilities=frozenset({"document.read"}),
        allowed_actors=frozenset({"agent-1"}),
        allowed_resources=frozenset({"sandbox-doc"}),
        authority_scope={"environment": "sandbox"},
        resource_limits={"bytes": 1024},
        expires_at=NOW + timedelta(hours=1),
    )
    values.update(overrides)
    return Policy(**values)


def request(**overrides):
    values = dict(
        actor="agent-1",
        capability="document.read",
        action="read",
        resource="sandbox-doc",
        requested_scope={"environment": "sandbox"},
        requested_resources={"bytes": 100},
        now=NOW,
    )
    values.update(overrides)
    return ExecutionRequest(**values)


def assert_blocked(**overrides):
    decision, reasons = evaluate(request(**overrides), base_policy())
    assert decision is Decision.BLOCK
    return reasons


def test_actor_substitution_is_blocked():
    assert "actor_not_authorized" in assert_blocked(actor="attacker")


def test_capability_substitution_is_blocked():
    assert "capability_not_authorized" in assert_blocked(capability="document.write")


def test_action_substitution_is_blocked():
    assert "action_not_authorized" in assert_blocked(action="delete")


def test_resource_substitution_is_blocked():
    assert "resource_not_authorized" in assert_blocked(resource="production-db")


def test_scope_expansion_is_blocked():
    assert "scope_outside_authority" in assert_blocked(
        requested_scope={"environment": "production"}
    )


def test_resource_escalation_is_blocked():
    assert "resource_limit_exceeded:bytes" in assert_blocked(
        requested_resources={"bytes": 4096}
    )


def test_expired_authority_is_blocked():
    reasons = assert_blocked(now=NOW + timedelta(hours=2))
    assert "authorization_expired" in reasons


def test_review_does_not_become_allow():
    policy = base_policy(
        allowed_actions=frozenset({"read", "delete"}),
        review_actions=frozenset({"delete"}),
    )
    decision, reasons = evaluate(request(action="delete"), policy)
    assert decision is Decision.REVIEW
    assert reasons == ["human_review_required"]


def test_blocked_request_does_not_execute_reference_side_effect():
    executed = False

    decision, _ = evaluate(
        request(requested_scope={"environment": "production"}),
        base_policy(),
    )

    if decision is Decision.ALLOW:
        executed = True

    assert decision is Decision.BLOCK
    assert executed is False
