"""Run Exp0-Exp3 as deterministic, local-only governance experiments.

This runner is deliberately a simulator: no network, credentials, external tools,
or real-world side effects are used. It records proposal reach, fixed authority,
governance outcome, execution, AEWA, and a hash-linked EvidenceSeal.
"""

from datetime import datetime, timezone
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "harness"))
sys.path.insert(0, str(ROOT))

from metrics.aewa import digest, reconstructable, reach_scope_divergence, seal_transition
from C0_baseline import C0
from C1_tool_expansion import C1
from C2_reasoning import C2
from C3_adversarial import C3

AUTHORITY = {"echo:return"}


def evaluate(experiment, capabilities):
    divergence = reach_scope_divergence(set(capabilities), AUTHORITY)
    rows = []
    previous_hash = "GENESIS"
    state = {"authority": sorted(AUTHORITY), "experiment": experiment}

    # The governed reference behavior is fail-closed for every action outside A_t.
    for action in sorted(capabilities):
        allowed = action in AUTHORITY
        executed = allowed
        decision = "ALLOW" if allowed else "BLOCK"
        delta = {"action": action, "decision": decision, "executed": executed}
        record = seal_transition(
            state,
            delta,
            {"type": "governance-decision", "decision": decision, "experiment": experiment},
            previous_hash,
        )
        rows.append({
            "experiment": experiment,
            "capability_set_size": len(capabilities),
            "action": action,
            "in_authorized_space": allowed,
            "decision": decision,
            "executed": executed,
            "authority_before": sorted(AUTHORITY),
            "authority_after": sorted(AUTHORITY),
            "authorized_transition": False,
            "evidence_seal": record["evidence_seal"],
            "record_hash": record["record_hash"],
            "previous_hash": record["previous_hash"],
        })
        previous_hash = record["record_hash"]

    aewa_events = sum(
        row["authority_before"] != row["authority_after"] and not row["authorized_transition"]
        for row in rows
    )
    records = [
        {k: row[k] for k in ("authority_before", "authority_after", "authorized_transition", "evidence_seal", "record_hash", "previous_hash")}
        for row in rows
    ]
    return {
        "experiment": experiment,
        "capabilities": sorted(capabilities),
        "authorized_actions": sorted(AUTHORITY),
        "reach_scope_divergence": sorted(divergence),
        "aewa": int(aewa_events),
        "authority_invariant": all(row["authority_before"] == row["authority_after"] for row in rows),
        "trajectory_reconstructable": reconstructable(records),
        "rows": rows,
    }


def main():
    experiments = [("Exp0", C0), ("Exp1", C1), ("Exp2", C2), ("Exp3", C3)]
    results = [evaluate(name, caps) for name, caps in experiments]
    payload = {
        "schema_version": "0.1",
        "apparatus": "governance-invariance-v0.1",
        "run_id": datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ"),
        "local_simulation_only": True,
        "results": results,
    }
    out = ROOT / "results" / f"run_{payload['run_id']}.jsonl"
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", encoding="utf-8") as handle:
        previous = "GENESIS"
        for result in results:
            record = {"previous_hash": previous, "result": result}
            record["record_hash"] = digest(record)
            handle.write(json.dumps(record, sort_keys=True) + "\n")
            previous = record["record_hash"]
    print(json.dumps({
        "run_file": str(out),
        "experiments": [
            {"experiment": r["experiment"], "aewa": r["aewa"], "authority_invariant": r["authority_invariant"], "trajectory_reconstructable": r["trajectory_reconstructable"]}
            for r in results
        ],
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
