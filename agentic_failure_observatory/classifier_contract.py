"""Model-agnostic contract for Hugging Face or other classifiers.

A classifier produces a proposal. KAIROSEED evidence and policy checks remain
independent of the model and no classifier output is treated as truth.
"""

from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Protocol, Sequence


FAILURE_MODES = (
    "UNAUTHORIZED_ACTION",
    "SCOPE_EXPANSION",
    "TOOL_MISUSE",
    "PRIVILEGE_ESCALATION",
    "GOAL_PATH_CONFUSION",
    "INSTRUCTION_CONFLICT",
    "DELEGATION_FAILURE",
    "MISSING_HUMAN_APPROVAL",
    "VERIFICATION_FAILURE",
    "AUDIT_EVIDENCE_FAILURE",
    "RUNTIME_CONTAINMENT_FAILURE",
    "FALSE_BELIEF_OR_HALLUCINATION",
)


@dataclass(frozen=True)
class ClassificationProposal:
    label: str
    confidence: float
    model_id: str


class FailureClassifier(Protocol):
    def classify(self, text: str) -> Sequence[ClassificationProposal]: ...


def validate_proposal(proposal: ClassificationProposal) -> ClassificationProposal:
    if proposal.label not in FAILURE_MODES:
        raise ValueError(f"Unknown failure mode: {proposal.label}")
    if not 0.0 <= proposal.confidence <= 1.0:
        raise ValueError("confidence must be between 0 and 1")
    if not proposal.model_id.strip():
        raise ValueError("model_id is required")
    return proposal


def proposal_record(proposal: ClassificationProposal) -> dict:
    return asdict(validate_proposal(proposal))
