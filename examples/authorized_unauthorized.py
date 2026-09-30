"""Safe, local ASTRA authorization example.

This example only evaluates a reference policy and mutates a local in-memory
simulation. It does not invoke an external system.
"""

from astra.core import ExecutionRequest, Policy, evaluate

NOW = __import__("datetime").datetime(2026, 1, 1, tzinfo=__import__("datetime").timezone.utc)

policy = Policy(
    allowed_actions=frozenset({"read"}),
    allowed_capabilities=frozenset({"document.read"}),
    allowed_actors=frozenset({"agent-1"}),
    allowed_resources=frozenset({"local-demo"}),
    authority_scope={"environment": "sandbox"},
    resource_limits={"bytes": 1024},
    expires_at=NOW.replace(hour=23),
)

def check(label: str, request: ExecutionRequest) -> None:
    decision, reasons = evaluate(request, policy)
    print(f"{label}: {decision.value} {reasons}")

check("authorized", ExecutionRequest(
    actor="agent-1",
    capability="document.read",
    action="read",
    resource="local-demo",
    requested_scope={"environment": "sandbox"},
    requested_resources={"bytes": 100},
    now=NOW,
))

check("unauthorized scope expansion", ExecutionRequest(
    actor="agent-1",
    capability="document.read",
    action="read",
    resource="local-demo",
    requested_scope={"environment": "production"},
    requested_resources={"bytes": 100},
    now=NOW,
))

# Expected:
# authorized: ALLOW ['authorized']
# unauthorized scope expansion: BLOCK ['scope_outside_authority']
