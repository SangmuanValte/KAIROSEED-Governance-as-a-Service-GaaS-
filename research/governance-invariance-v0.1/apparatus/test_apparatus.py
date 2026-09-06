"""Tests for the empirical apparatus itself; all effects are local simulations."""

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "harness"))
sys.path.insert(0, str(ROOT))

from C0_baseline import C0
from C1_tool_expansion import C1
from C2_reasoning import C2
from C3_adversarial import C3
from metrics.aewa import authority_invariant, aewa, reconstructable, reach_scope_divergence, seal_transition
from run_matrix import evaluate


def test_capability_ladder_strictly_expands():
    assert C0 < C1 < C2 < C3


def test_reach_scope_probe_has_divergence_but_no_aewa():
    divergence = reach_scope_divergence(set(C1), {"echo:return"})
    assert divergence
    trace = [{
        "authority_before": ["echo:return"],
        "authority_after": ["echo:return"],
        "authorized_transition": False,
    }]
    assert aewa(trace) == 0
    assert authority_invariant(trace)


def test_matrix_preserves_authority_and_blocks_out_of_scope_actions():
    for name, capabilities in (("Exp0", C0), ("Exp1", C1), ("Exp2", C2), ("Exp3", C3)):
        result = evaluate(name, capabilities)
        assert result["aewa"] == 0
        assert result["authority_invariant"]
        assert result["trajectory_reconstructable"]
        for row in result["rows"]:
            assert row["executed"] == row["in_authorized_space"]


def test_missing_evidence_seal_is_not_reconstructable():
    record = seal_transition({"x": 1}, {"y": 2}, {"type": "test"})
    record.pop("evidence_seal")
    assert not reconstructable([record])


def test_unauthorized_authority_mutation_is_counted_as_aewa():
    trace = [{
        "authority_before": ["echo:return"],
        "authority_after": ["echo:return", "file:read"],
        "authorized_transition": False,
    }]
    assert aewa(trace) == 1
