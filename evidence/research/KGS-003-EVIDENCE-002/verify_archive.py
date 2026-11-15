#!/usr/bin/env python3
"""Validate archived KGS-003 synthetic files and their stored trial summary.

DOCUMENTATION / DATA-CONSISTENCY ONLY: this does not run the experiment,
evaluate a JIREH security boundary, or produce C3/C6 proof.
"""
import hashlib
import json
from collections import Counter
from pathlib import Path
from statistics import median

ROOT = Path(__file__).resolve().parent

def verify():
    m = json.loads((ROOT / "PROVENANCE.json").read_text(encoding="utf-8"))
    assert m["assurance"] == "NOT_VERIFIED"
    assert m["scope"] == "SYNTHETIC_ONLY"
    assert m["original_claim_freeze"] == "NOT_ESTABLISHED"

    for filename, expected in m["files"].items():
        file_bytes = (ROOT / filename).read_bytes()
        assert len(file_bytes) == expected["size_bytes"], filename
        assert hashlib.sha256(file_bytes).hexdigest() == expected["sha256"], filename

    result = json.loads((ROOT / "kgs_003_evidence_002_results.json").read_text(encoding="utf-8"))
    trials = result["trials"]
    s = result["summary"]
    config = result["config"]
    assert result["drill"] == "KGS-003-EVIDENCE-002"
    assert config == m["run"]["result_config"]
    assert len(trials) == config["trials"] == 1000
    assert [t["trial"] for t in trials] == list(range(1, 1001))
    assert all(
        t["snapshot_in_window"] ==
        (t["freeze_request_ns"] <= t["snapshot_ns"] <= t["stop_observed_ns"])
        for t in trials
    )
    inside = [t for t in trials if t["snapshot_in_window"]]
    counts = Counter(t["snapshot_class"] for t in inside)
    assert len(inside) == s["snapshot_in_window_count"] == m["measured_results"]["in_window"]
    assert len(trials) - len(inside) == s["snapshot_out_of_window_count"] == m["measured_results"]["out_of_window"]
    for key in ("clean", "mutated", "corrupted"):
        assert counts[key] == s[f"{key}_count"] == m["measured_results"][key]
    assert sum(t["counter_delta"] > 0 for t in trials) == s["trials_with_post_freeze_completed_writes"]
    assert sum(t["counter_delta"] for t in trials) == s["counter_delta_total"]
    assert max(t["counter_delta"] for t in trials) == s["counter_delta_max"]

    delays = sorted(t["freeze_to_stop_observed_ms"] for t in trials)
    recorded = s["freeze_request_to_stop_observed_ms"]
    assert abs(median(delays) - recorded["median"]) < 1e-8
    for percentile in ("p95", "p99"):
        pct = int(percentile[1:]) / 100
        assert abs(delays[int((len(delays) - 1) * pct)] - recorded[percentile]) < 1e-8
    assert delays[-1] == recorded["max"]
    print(
        "SYNTHETIC_DATA_CONSISTENCY_OK: files=3 trials=1000 "
        "in_window=971 mutated=737 corrupted=234 clean=0; "
        "NOT JIREH CONTAINMENT PROOF"
    )

if __name__ == "__main__":
    verify()
