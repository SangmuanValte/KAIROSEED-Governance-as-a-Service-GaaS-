from dataclasses import dataclass
from typing import Any

@dataclass(frozen=True)
class Decision:
    status: str
    reasons: tuple[str, ...]


def govern(proposal: dict[str, Any], allowed_scope: str, authorized_actions: set[str]) -> Decision:
    reasons: list[str] = []
    required = {"proposal_id", "objective", "scope", "action", "risk_class", "evidence_required"}
    missing = sorted(required - proposal.keys())
    if missing:
        reasons.append(f"missing_fields:{','.join(missing)}")
    if proposal.get("scope") != allowed_scope:
        reasons.append("scope_mismatch")
    if proposal.get("action") not in authorized_actions:
        reasons.append("action_not_authorized")
    if not isinstance(proposal.get("evidence_required"), list) or not proposal.get("evidence_required"):
        reasons.append("evidence_requirements_missing")
    if reasons:
        return Decision("DENY", tuple(reasons))
    return Decision("ADMIT", ("policy_pass",))
