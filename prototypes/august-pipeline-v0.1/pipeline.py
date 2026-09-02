from dataclasses import dataclass, asdict
from enum import Enum
import json
from hashlib import sha256
from time import time


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


def classify(p: Proposal) -> Decision:
    if not p.capability:
        return Decision.BLOCK
    if not p.permission or not p.authorization:
        return Decision.REVIEW
    if p.risk == "high":
        return Decision.REVIEW
    return Decision.APPROVE


def run_pipeline(p: Proposal) -> dict:
    decision = classify(p)
    events = [
        {"stage": "INGEST", "status": "PASS"},
        {"stage": "INTERPRET", "status": "PASS", "task": p.task},
        {"stage": "PROPOSE", "status": "PASS", "risk": p.risk},
        {"stage": "AUTHORIZE", "status": decision.value},
    ]

    if decision != Decision.APPROVE:
        result = "execution_not_started"
        events.append({"stage": "EXECUTE", "status": "BLOCKED", "reason": "authorization_gate"})
    else:
        result = "simulated_bounded_execution"
        events.append({"stage": "EXECUTE", "status": "PASS", "mode": "simulation"})

    events.append({"stage": "VERIFY", "status": "PASS", "result": result})

    evidence = {
        "timestamp": int(time()),
        "proposal": asdict(p),
        "decision": decision.value,
        "result": result,
        "events": events,
    }
    digest = sha256(json.dumps(evidence, sort_keys=True).encode()).hexdigest()
    evidence["evidence_sha256"] = digest
    return evidence


if __name__ == "__main__":
    cases = [
        Proposal("Prepare an OpenAI API integration proposal", True, False, "medium", None),
        Proposal("Simulate a governed research workflow", True, True, "medium", "AUTH-AUG-001"),
        Proposal("Publish directly to production", True, False, "high", None),
    ]
    for case in cases:
        print(json.dumps(run_pipeline(case), indent=2))
