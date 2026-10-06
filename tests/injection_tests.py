"""Deterministic staging tests for C ⊆ E ⊆ S_auth.

These tests exercise the policy model only. They do not establish eBPF, OPA,
TPM, or production-runtime correctness.
"""

from __future__ import annotations

import unittest
from dataclasses import dataclass
from typing import FrozenSet, Iterable


@dataclass(frozen=True)
class EvidenceAtom:
    evidence_id: str
    supports_claims: FrozenSet[str]
    scope_atoms: FrozenSet[str]


@dataclass(frozen=True)
class Payload:
    claims: FrozenSet[str]
    evidence: tuple[EvidenceAtom, ...]
    token_epoch: int


@dataclass(frozen=True)
class Policy:
    epoch: int
    authorized_scope: FrozenSet[str]


@dataclass(frozen=True)
class Decision:
    allow: bool
    subsystem: str
    code: str


def _union(items: Iterable[FrozenSet[str]]) -> FrozenSet[str]:
    out: set[str] = set()
    for item in items:
        out.update(item)
    return frozenset(out)


def evaluate(payload: Payload, policy: Policy) -> Decision:
    """Fail-closed deterministic policy evaluation."""
    if payload.token_epoch != policy.epoch:
        return Decision(False, "GOVANA", "STALE_EPOCH")

    evidence_scope = _union(e.scope_atoms for e in payload.evidence)
    if not evidence_scope.issubset(policy.authorized_scope):
        return Decision(False, "GOVANA", "EVIDENCE_OUTSIDE_SCOPE")

    evidenced_claims = _union(e.supports_claims for e in payload.evidence)
    if not payload.claims.issubset(evidenced_claims):
        return Decision(False, "JIREH", "CLAIM_WITHOUT_EVIDENCE")

    return Decision(True, "KAIROSEED", "ALLOW")


class VerificationInequalityInjectionTests(unittest.TestCase):
    def setUp(self) -> None:
        self.policy = Policy(
            epoch=7,
            authorized_scope=frozenset({"seq", "par", "worker:cpu"}),
        )

    def test_1_claim_not_subset_evidence_is_denied(self) -> None:
        payload = Payload(
            claims=frozenset({"step:1", "step:2", "step:3", "step:4", "step:5"}),
            evidence=(
                EvidenceAtom("ev-1", frozenset({"step:1", "step:2"}), frozenset({"seq"})),
                EvidenceAtom("ev-2", frozenset({"step:3"}), frozenset({"seq"})),
                EvidenceAtom("ev-3", frozenset({"step:4"}), frozenset({"seq"})),
            ),
            token_epoch=7,
        )
        decision = evaluate(payload, self.policy)
        self.assertFalse(decision.allow)
        self.assertEqual(
            (decision.subsystem, decision.code),
            ("JIREH", "CLAIM_WITHOUT_EVIDENCE"),
        )

    def test_2_evidence_not_subset_authorized_scope_is_denied_preexec(self) -> None:
        payload = Payload(
            claims=frozenset({"claim:efficiency"}),
            evidence=(
                EvidenceAtom(
                    "ev-perfect",
                    frozenset({"claim:efficiency"}),
                    frozenset({"prohibited_enclave"}),
                ),
            ),
            token_epoch=7,
        )
        decision = evaluate(payload, self.policy)
        self.assertFalse(decision.allow)
        self.assertEqual(
            (decision.subsystem, decision.code),
            ("GOVANA", "EVIDENCE_OUTSIDE_SCOPE"),
        )

    def test_3_historical_token_reuse_has_zero_active_authority(self) -> None:
        payload = Payload(
            claims=frozenset({"claim:within-scope"}),
            evidence=(
                EvidenceAtom(
                    "ev-epoch6",
                    frozenset({"claim:within-scope"}),
                    frozenset({"seq"}),
                ),
            ),
            token_epoch=6,
        )
        decision = evaluate(payload, self.policy)
        self.assertFalse(decision.allow)
        self.assertEqual(
            (decision.subsystem, decision.code),
            ("GOVANA", "STALE_EPOCH"),
        )

    def test_valid_payload_is_allowed(self) -> None:
        payload = Payload(
            claims=frozenset({"claim:seq"}),
            evidence=(
                EvidenceAtom(
                    "ev-seq",
                    frozenset({"claim:seq"}),
                    frozenset({"seq"}),
                ),
            ),
            token_epoch=7,
        )
        decision = evaluate(payload, self.policy)
        self.assertTrue(decision.allow)
        self.assertEqual(decision.code, "ALLOW")


if __name__ == "__main__":
    unittest.main(verbosity=2)
