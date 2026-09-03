from dataclasses import dataclass, asdict
from datetime import datetime, timezone
import hashlib
import json


class AuthorizationDenied(Exception):
    status = 403
    code = "AUTHORIZATION_DENIED"

    def __init__(self, reason: str):
        super().__init__(reason)
        self.reason = reason


@dataclass(frozen=True)
class Proposal:
    proposal_id: str
    agent_id: str
    action: str
    resource: str


@dataclass(frozen=True)
class Evidence:
    receipt_id: str
    proposal_id: str
    agent_id: str
    action: str
    resource: str
    requested: bool
    authorized: bool
    executed: bool
    validated: bool
    committed: bool
    outcome: str
    decision_reason: str
    timestamp: str
    state_before_hash: str
    state_after_hash: str


def state_hash(state: dict) -> str:
    payload = json.dumps(state, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(payload).hexdigest()


def authorize(proposal: Proposal, allowed_actions: set[str]) -> None:
    if proposal.action not in allowed_actions:
        raise AuthorizationDenied(
            f"Action '{proposal.action}' is outside the authorized scope."
        )


def execute(proposal: Proposal, state: dict, allowed_actions: set[str]) -> Evidence:
    before = state_hash(state)
    timestamp = datetime.now(timezone.utc).isoformat()

    try:
        authorize(proposal, allowed_actions)
    except AuthorizationDenied as exc:
        after = state_hash(state)
        return Evidence(
            receipt_id=f"ev-{proposal.proposal_id}",
            proposal_id=proposal.proposal_id,
            agent_id=proposal.agent_id,
            action=proposal.action,
            resource=proposal.resource,
            requested=True,
            authorized=False,
            executed=False,
            validated=True,
            committed=False,
            outcome="denied",
            decision_reason=exc.reason,
            timestamp=timestamp,
            state_before_hash=before,
            state_after_hash=after,
        )

    # Controlled execution occurs only after authorization.
    if proposal.action == "write_demo_state":
        state[proposal.resource] = "updated"
    else:
        raise ValueError(f"No executor is registered for action: {proposal.action}")

    after = state_hash(state)
    validated = state.get(proposal.resource) == "updated"

    return Evidence(
        receipt_id=f"ev-{proposal.proposal_id}",
        proposal_id=proposal.proposal_id,
        agent_id=proposal.agent_id,
        action=proposal.action,
        resource=proposal.resource,
        requested=True,
        authorized=True,
        executed=True,
        validated=validated,
        committed=validated,
        outcome="success" if validated else "failed",
        decision_reason="authorized",
        timestamp=timestamp,
        state_before_hash=before,
        state_after_hash=after,
    )


def outcome_verified(evidence: Evidence) -> dict:
    if not (
        evidence.authorized
        and evidence.executed
        and evidence.validated
        and evidence.outcome == "success"
        and evidence.committed
    ):
        raise ValueError("Only independently validated successful execution may settle.")

    return {
        "event": "OUTCOME_VERIFIED",
        "proposal_id": evidence.proposal_id,
        "execution_id": evidence.receipt_id,
        "authorized": True,
        "executed": True,
        "validated": True,
        "outcome": "success",
        "evidence_id": evidence.receipt_id,
        "billable": True,
    }


if __name__ == "__main__":
    state = {"protected_resource": "unchanged"}

    denied = execute(
        Proposal("prop-deny", "agent-1", "write_demo_state", "protected_resource"),
        state,
        allowed_actions=set(),
    )
    print(json.dumps(asdict(denied), indent=2))

    admitted = execute(
        Proposal("prop-admit", "agent-1", "write_demo_state", "protected_resource"),
        state,
        allowed_actions={"write_demo_state"},
    )
    print(json.dumps(asdict(admitted), indent=2))
    print(json.dumps(outcome_verified(admitted), indent=2))
