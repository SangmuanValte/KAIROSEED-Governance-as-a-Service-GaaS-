from dataclasses import dataclass, asdict
from enum import Enum
from hashlib import sha256
import json
from time import time
from uuid import uuid4


class Decision(str, Enum):
    APPROVE = "APPROVE"
    REVIEW = "REVIEW"
    BLOCK = "BLOCK"


@dataclass
class Proposal:
    task: str
    capability: bool
    permission: bool
    risk: str
    authorization: str | None


def new_id(prefix: str) -> str:
    return f"{prefix}_{uuid4().hex[:12]}"


def classify(p: Proposal) -> Decision:
    if not p.capability:
        return Decision.BLOCK
    if not p.permission or not p.authorization:
        return Decision.REVIEW
    if p.risk == "high":
        return Decision.REVIEW
    return Decision.APPROVE


def event(stage: str, status: str, **fields) -> dict:
    return {
        "event_id": new_id("evt"),
        "stage": stage,
        "status": status,
        "timestamp": int(time()),
        **fields,
    }


def run_pipeline(p: Proposal) -> dict:
    proposal_id = new_id("proposal")
    interpretation_id = new_id("interpretation")
    decision = classify(p)

    events = [
        event("INGEST", "PASS", proposal_id=proposal_id),
        event(
            "INTERPRET",
            "PASS",
            interpretation_id=interpretation_id,
            proposal_id=proposal_id,
            task=p.task,
        ),
        event(
            "PROPOSE",
            "PASS",
            proposal_id=proposal_id,
            interpretation_id=interpretation_id,
            risk=p.risk,
        ),
    ]

    authorization_id = p.authorization if decision == Decision.APPROVE else None

    if authorization_id:
        events.append(
            event(
                "AUTHORIZE",
                "PASS",
                authorization_id=authorization_id,
                proposal_id=proposal_id,
                scope=p.task,
            )
        )
        execution_id = new_id("execution")
        events.append(
            event(
                "EXECUTE",
                "PASS",
                execution_id=execution_id,
                authorization_id=authorization_id,
                mode="sandbox_simulation",
                result="simulated_bounded_execution",
            )
        )
        verification_id = new_id("verification")
        events.append(
            event(
                "VERIFY",
                "PASS",
                verification_id=verification_id,
                execution_id=execution_id,
                checks=["authorization_scope", "execution_result"],
            )
        )
        result = "simulated_bounded_execution"
        verification_status = "PASS"
    else:
        events.append(
            event(
                "AUTHORIZE",
                decision.value,
                proposal_id=proposal_id,
                reason="authorization_boundary_not_satisfied",
            )
        )
        execution_id = None
        verification_id = None
        events.append(
            event(
                "EXECUTE",
                "HALTED",
                proposal_id=proposal_id,
                reason="no_valid_authorization",
            )
        )
        events.append(
            event(
                "VERIFY",
                "NOT_RUN",
                proposal_id=proposal_id,
                reason="execution_not_started",
            )
        )
        result = "execution_not_started"
        verification_status = "NOT_RUN"

    evidence_id = new_id("evidence")
    evidence = {
        "evidence_id": evidence_id,
        "timestamp": int(time()),
        "lineage": {
            "proposal_id": proposal_id,
            "interpretation_id": interpretation_id,
            "authorization_id": authorization_id,
            "execution_id": execution_id,
            "verification_id": verification_id,
            "evidence_id": evidence_id,
        },
        "proposal": asdict(p),
        "decision": decision.value,
        "result": result,
        "verification_status": verification_status,
        "events": events,
        "invariant": "No execution exists without a traceable authorization.",
        "safety_boundary": "simulation_only",
    }

    canonical = json.dumps(evidence, sort_keys=True, separators=(",", ":")).encode()
    evidence["evidence_sha256"] = sha256(canonical).hexdigest()
    return evidence


if __name__ == "__main__":
    cases = [
        Proposal("Prepare an OpenAI API integration proposal", True, False, "medium", None),
        Proposal("Simulate a governed research workflow", True, True, "medium", "AUTH-AUG-001"),
        Proposal("Publish directly to production", True, False, "high", None),
    ]
    for case in cases:
        print(json.dumps(run_pipeline(case), indent=2))
