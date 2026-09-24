"""Deterministic ASTRA authorization gate.

Fail-closed rules:
- capability does not imply permission
- missing authority blocks
- expired authority blocks
- scope mismatch blocks
- resource violations block
- consequential execution requires a valid authorization envelope
"""
from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Mapping, Sequence

class Decision(str, Enum):
    ALLOW = "ALLOW"
    BLOCK = "BLOCK"
    REVIEW = "REVIEW"

@dataclass(frozen=True)
class ExecutionRequest:
    actor: str
    capability: str
    action: str
    resource: str
    requested_scope: Mapping[str, Any] = field(default_factory=dict)
    requested_resources: Mapping[str, float] = field(default_factory=dict)
    purpose: str | None = None
    now: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

@dataclass(frozen=True)
class Policy:
    allowed_actions: frozenset[str]
    allowed_capabilities: frozenset[str]
    allowed_actors: frozenset[str]
    allowed_resources: frozenset[str]
    authority_scope: Mapping[str, Any] = field(default_factory=dict)
    resource_limits: Mapping[str, float] = field(default_factory=dict)
    expires_at: datetime | None = None
    require_purpose: bool = False
    review_actions: frozenset[str] = frozenset()
    metadata: Mapping[str, Any] = field(default_factory=dict)

def _scope_covers(granted: Mapping[str, Any], requested: Mapping[str, Any]) -> bool:
    for key, wanted in requested.items():
        if key not in granted:
            return False
        allowed = granted[key]
        if isinstance(wanted, Mapping):
            if not isinstance(allowed, Mapping) or not _scope_covers(allowed, wanted):
                return False
        elif isinstance(allowed, (set, frozenset, list, tuple)):
            if isinstance(wanted, (set, frozenset, list, tuple)):
                if not set(wanted).issubset(set(allowed)):
                    return False
            elif wanted not in allowed:
                return False
        elif allowed != wanted:
            return False
    return True

def evaluate(request: ExecutionRequest, policy: Policy) -> tuple[Decision, list[str]]:
    reasons: list[str] = []
    if request.actor not in policy.allowed_actors:
        reasons.append("actor_not_authorized")
    if request.capability not in policy.allowed_capabilities:
        reasons.append("capability_not_authorized")
    if request.action not in policy.allowed_actions:
        reasons.append("action_not_authorized")
    if request.resource not in policy.allowed_resources:
        reasons.append("resource_not_authorized")
    if policy.expires_at is not None and request.now >= policy.expires_at:
        reasons.append("authorization_expired")
    if not _scope_covers(policy.authority_scope, request.requested_scope):
        reasons.append("scope_outside_authority")
    for name, requested in request.requested_resources.items():
        limit = policy.resource_limits.get(name)
        if limit is None or requested > limit:
            reasons.append(f"resource_limit_exceeded:{name}")
    if policy.require_purpose and not request.purpose:
        reasons.append("purpose_required")
    if reasons:
        return Decision.BLOCK, reasons
    if request.action in policy.review_actions:
        return Decision.REVIEW, ["human_review_required"]
    return Decision.ALLOW, ["authorized"]

def decision_record(
    request: ExecutionRequest,
    decision: Decision,
    reasons: Sequence[str],
    *,
    result: Any = None,
    evidence: Mapping[str, Any] | None = None,
    parent_action_id: str | None = None,
    correlation_id: str | None = None,
) -> dict[str, Any]:
    return {
        "event_type": "ASTRA_EXECUTION_DECISION",
        "actor": request.actor,
        "capability": request.capability,
        "action": request.action,
        "resource": request.resource,
        "authority_scope": dict(request.requested_scope),
        "decision": decision.value,
        "reason": list(reasons),
        "parent_action_id": parent_action_id,
        "correlation_id": correlation_id,
        "result": result,
        "evidence": dict(evidence or {}),
        "created_at": request.now.astimezone(timezone.utc).isoformat(),
    }
