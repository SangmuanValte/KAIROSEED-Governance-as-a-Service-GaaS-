from dataclasses import dataclass, asdict
from enum import Enum
from hashlib import sha256
import json
import time


class Decision(str, Enum):
    ALLOW = "ALLOW"
    ESCALATE = "ESCALATE"
    BLOCK = "BLOCK"


@dataclass(frozen=True)
class ActionProposal:
    agent_id: str
    intent: str
    authority_scope: str
    policy_version: str
    capability: bool = True
    validation_passed: bool = True


@dataclass(frozen=True)
class GovernanceDecision:
    decision: Decision
    reason: str
    proposal_hash: str
    evidence_initialized: bool


class EvidenceLedger:
    def __init__(self):
        self.records = []

    def append(self, proposal: ActionProposal, decision: Decision, reason: str):
        previous = self.records[-1]["record_hash"] if self.records else "GENESIS"
        payload = {
            "timestamp": time.time(),
            "proposal": asdict(proposal),
            "decision": decision.value,
            "reason": reason,
            "previous_hash": previous,
        }
        canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"))
        record = {**payload, "record_hash": sha256(canonical.encode()).hexdigest()}
        self.records.append(record)
        return record


def proposal_hash(proposal: ActionProposal) -> str:
    canonical = json.dumps(asdict(proposal), sort_keys=True, separators=(",", ":"))
    return sha256(canonical.encode()).hexdigest()


def govern(proposal: ActionProposal, ledger: EvidenceLedger) -> GovernanceDecision:
    # Fail closed: every required predicate must pass before ALLOW.
    if not proposal.capability:
        decision, reason = Decision.BLOCK, "capability_missing"
    elif not proposal.intent.strip():
        decision, reason = Decision.BLOCK, "intent_missing"
    elif proposal.authority_scope != "authorized":
        decision, reason = Decision.BLOCK, "authority_invalid"
    elif proposal.policy_version != "v0.1":
        decision, reason = Decision.BLOCK, "unsupported_policy_version"
    elif not proposal.validation_passed:
        decision, reason = Decision.BLOCK, "validation_failed"
    else:
        decision, reason = Decision.ALLOW, "all_required_predicates_passed"

    record = ledger.append(proposal, decision, reason)
    return GovernanceDecision(
        decision=decision,
        reason=reason,
        proposal_hash=proposal_hash(proposal),
        evidence_initialized=bool(record),
    )
