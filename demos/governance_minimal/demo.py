"""Smallest local Govana -> VEP -> PEP -> JIREH governance demo.

No network calls. No credentials. No external side effects.
"""

from dataclasses import dataclass
from enum import Enum
from typing import Any


class Decision(str, Enum):
    PASS = "PASS"
    BLOCK = "BLOCK"


@dataclass(frozen=True)
class Proposal:
    actor: str
    action: str
    resource: str
    scope: str


@dataclass(frozen=True)
class Authorization:
    actor: str
    action: str
    resource: str
    scope: str


@dataclass(frozen=True)
class Verdict:
    decision: Decision
    reason: str


def govana(actor: str, action: str, resource: str, scope: str) -> Proposal:
    """Create the minimal proposal. Govana does not authorize it."""
    return Proposal(actor, action, resource, scope)


def vep(proposal: Proposal) -> tuple[bool, str]:
    """Validate proposal shape. VEP does not grant authority."""
    fields = (proposal.actor, proposal.action, proposal.resource, proposal.scope)
    if not all(isinstance(value, str) and value.strip() for value in fields):
        return False, "invalid_proposal"
    return True, "proposal_valid"


def pep(proposal: Proposal, authorization: Authorization | None) -> Verdict:
    """Policy Enforcement Point: the sole authorization decision in this demo."""
    if authorization is None:
        return Verdict(Decision.BLOCK, "missing_authorization")

    if (
        proposal.actor != authorization.actor
        or proposal.action != authorization.action
        or proposal.resource != authorization.resource
        or proposal.scope != authorization.scope
    ):
        return Verdict(Decision.BLOCK, "authorization_binding_mismatch")

    return Verdict(Decision.PASS, "authorized")


def jireh(verdict: Verdict, state: dict[str, Any], proposal: Proposal) -> dict[str, Any]:
    """Post-authorization verification + local state transition."""
    if verdict.decision is not Decision.PASS:
        raise PermissionError("JIREH cannot execute without PEP PASS")

    before = dict(state)
    state["last_action"] = proposal.action
    state["resource"] = proposal.resource
    after = dict(state)

    if after.get("last_action") != proposal.action:
        raise AssertionError("post_state_verification_failed")

    return {
        "verified": True,
        "pre_state": before,
        "post_state": after,
        "action": proposal.action,
    }


def run(proposal: Proposal, authorization: Authorization | None, state: dict[str, Any]) -> dict[str, Any]:
    """Complete governed transition: VEP -> PEP -> JIREH."""
    valid, reason = vep(proposal)
    if not valid:
        return {"decision": "BLOCK", "reason": reason, "executed": False}

    verdict = pep(proposal, authorization)
    if verdict.decision is Decision.BLOCK:
        return {
            "decision": verdict.decision.value,
            "reason": verdict.reason,
            "executed": False,
        }

    evidence = jireh(verdict, state, proposal)
    return {
        "decision": verdict.decision.value,
        "reason": verdict.reason,
        "executed": True,
        "evidence": evidence,
    }


if __name__ == "__main__":
    auth = Authorization("agent-1", "read", "document-1", "sandbox")

    allowed = govana("agent-1", "read", "document-1", "sandbox")
    print("AUTHORIZED:", run(allowed, auth, {}))

    denied = govana("agent-1", "delete", "document-1", "sandbox")
    print("UNAUTHORIZED:", run(denied, auth, {}))
