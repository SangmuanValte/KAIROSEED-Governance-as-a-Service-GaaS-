from typing import Any
from .governance import Decision


def execute(proposal: dict[str, Any], decision: Decision) -> dict[str, Any]:
    if decision.status != "ADMIT":
        return {"status": "BLOCKED", "performed": False, "reason": "governance_denied"}
    # Prototype execution is deliberately side-effect free.
    return {"status": "EXECUTED", "performed": True, "action": proposal["action"]}
