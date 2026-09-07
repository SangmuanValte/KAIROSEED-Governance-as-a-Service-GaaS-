from datetime import datetime, timezone
from typing import Any


def record(proposal: dict[str, Any], decision: str, result: dict[str, Any], proven: bool) -> dict[str, Any]:
    return {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "proposal_id": proposal.get("proposal_id"),
        "decision": decision,
        "proposed_action": proposal.get("action"),
        "performed": result.get("performed", False),
        "result": result,
        "proven": proven,
    }
