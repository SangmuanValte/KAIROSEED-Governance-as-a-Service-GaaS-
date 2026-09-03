from typing import Any


def validate(result: dict[str, Any], proposal: dict[str, Any]) -> bool:
    return (
        result.get("status") == "EXECUTED"
        and result.get("performed") is True
        and result.get("action") == proposal.get("action")
    )
