#!/usr/bin/env python3
"""KGS-003-EVIDENCE-002: local synthetic concurrent-mutation window measurement.

RED DRILL — SYNTHETIC ONLY.
NOT A CLAIM ABOUT JIREH v0.4 PERFORMANCE.
NOT A CLAIM ABOUT eBPF, SECCOMP, OR REAL KERNEL ISOLATION.
NO ATOMICITY PROOF. NO C3/C6 ASSURANCE VERDICT.

Three persistent child processes:
  - agent: acknowledges a synthetic pause request (does not freeze memory)
  - mutator: writes only to a deliberately shared, harmless byte buffer
  - observer: independently samples the buffer at a chosen moment

The parent coordinates the trial, measures the requested-to-observed stop window,
and writes per-trial JSON evidence. 'stop' is a cooperative instruction to the
synthetic mutator, NOT a kernel kill or security boundary.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import multiprocessing as mp
import random
import statistics
import time
from pathlib import Path
from typing import Any

CLEAN = 0x00
PATTERNS = (0xA5, 0x5A)


def agent_main(conn: Any) -> None:
    while True:
        msg = conn.recv()
        if msg == "shutdown":
            break
        if msg == "pause":
            conn.send({"pause_ack_ns": time.perf_counter_ns()})
        else:
            raise RuntimeError(f"agent: unexpected {msg}")


def mutator_main(conn: Any, memory: Any, writes_counter: Any, length: int) -> None:
    while True:
        msg = conn.recv()
        if msg == "shutdown":
            break
        if msg != "mutate":
            raise RuntimeError(f"mutator: unexpected {msg}")
        idx = 0
        # Only mutator writes to this buffer during the active trial.
        # A partially copied buffer is intentionally classified as torn/corrupted.
        while not conn.poll():
            value = PATTERNS[idx % 2]
            for i in range(length):
                memory[i] = value
            writes_counter.value += 1
            idx += 1
            # Cooperative yield prevents a busy-loop from monopolizing the CPU.
            time.sleep(0)
        stop = conn.recv()
        if stop != "stop":
            raise RuntimeError(f"mutator: expected stop, received {stop}")
        conn.send({
            "stop_observed_ns": time.perf_counter_ns(),
            "completed_writes": int(writes_counter.value),
        })


def observer_main(conn: Any, memory: Any, length: int) -> None:
    while True:
        message = conn.recv()
        if message == "shutdown":
            break
        if not (isinstance(message, tuple) and message[0] == "snapshot"):
            raise RuntimeError(f"observer: unexpected {message}")
        delay_us = message[1]
        if delay_us:
            time.sleep(delay_us / 1_000_000)
        snapshot = bytes(memory[:length])
        observed_ns = time.perf_counter_ns()
        if all(b == CLEAN for b in snapshot):
            category = "clean"
        elif all(b == PATTERNS[0] for b in snapshot) or all(b == PATTERNS[1] for b in snapshot):
            category = "mutated"
        else:
            category = "corrupted"
        conn.send({
            "snapshot_ns": observed_ns,
            "snapshot_hash_sha256": hashlib.sha256(snapshot).hexdigest(),
            "snapshot_class": category,
        })


def quantile(sorted_values: list[float], pct: float) -> float:
    if not sorted_values:
        return 0.0
    return sorted_values[int((len(sorted_values) - 1) * pct)]


def run(trials: int, window_us: int, size: int, seed: int) -> dict[str, Any]:
    ctx = mp.get_context("spawn")  # portable, no inherited process state
    memory = ctx.RawArray("B", size)
    writes_counter = ctx.RawValue("Q", 0)
    agents_parent, agents_child = ctx.Pipe()
    mutator_parent, mutator_child = ctx.Pipe()
    observer_parent, observer_child = ctx.Pipe()
    processes = [
        ctx.Process(target=agent_main, args=(agents_child,), name="synthetic-agent"),
        ctx.Process(target=mutator_main, args=(mutator_child, memory, writes_counter, size), name="synthetic-mutator"),
        ctx.Process(target=observer_main, args=(observer_child, memory, size), name="synthetic-observer"),
    ]
    for proc in processes:
        proc.start()
    agents_child.close()
    mutator_child.close()
    observer_child.close()

    rng = random.Random(seed)
    results: list[dict[str, Any]] = []
    try:
        for n in range(1, trials + 1):
            # Parent resets the harmless test fixture only between trials.
            for i in range(size):
                memory[i] = CLEAN
            writes_counter.value = 0
            freeze_request_ns = time.perf_counter_ns()
            agents_parent.send("pause")
            mutator_parent.send("mutate")
            observer_parent.send(("snapshot", rng.randrange(max(1, window_us))))
            # Deliberately allow a race window; this is NOT a scheduler guarantee.
            time.sleep(window_us / 1_000_000)
            stop_request_ns = time.perf_counter_ns()
            mutator_parent.send("stop")

            agent_report = agents_parent.recv()
            observer_report = observer_parent.recv()
            mutator_report = mutator_parent.recv()
            stop_observed_ns = mutator_report["stop_observed_ns"]
            snapshot_ns = observer_report["snapshot_ns"]
            observed_in_window = freeze_request_ns <= snapshot_ns <= stop_observed_ns
            results.append({
                "trial": n,
                "freeze_request_ns": freeze_request_ns,
                "pause_ack_ns": agent_report["pause_ack_ns"],
                "snapshot_ns": snapshot_ns,
                "stop_request_ns": stop_request_ns,
                "stop_observed_ns": stop_observed_ns,
                "snapshot_in_window": observed_in_window,
                "snapshot_class": observer_report["snapshot_class"],
                "snapshot_hash_sha256": observer_report["snapshot_hash_sha256"],
                "counter_delta": mutator_report["completed_writes"],
                "freeze_to_stop_observed_ms": round((stop_observed_ns - freeze_request_ns) / 1e6, 6),
                "stop_request_to_stop_observed_ms": round((stop_observed_ns - stop_request_ns) / 1e6, 6),
            })
    finally:
        for conn in (agents_parent, mutator_parent, observer_parent):
            try:
                conn.send("shutdown")
            except (OSError, BrokenPipeError):
                pass
        for proc in processes:
            proc.join(timeout=3)
            if proc.is_alive():
                proc.terminate()
                proc.join(timeout=2)
        for conn in (agents_parent, mutator_parent, observer_parent):
            conn.close()

    in_window = [r for r in results if r["snapshot_in_window"]]
    counts = {k: sum(r["snapshot_class"] == k for r in in_window) for k in ("clean", "mutated", "corrupted")}
    delays = sorted(r["freeze_to_stop_observed_ms"] for r in results)
    delta = [r["counter_delta"] for r in results]
    return {
        "drill": "KGS-003-EVIDENCE-002",
        "label": "RED DRILL — SYNTHETIC ONLY. NOT A CLAIM ABOUT JIREH v0.4 PERFORMANCE. NOT A CLAIM ABOUT eBPF, SECCOMP, OR REAL KERNEL ISOLATION.",
        "claim": "Synthetic cooperative-stop race measurement only; NOT an atomicity proof or C3/C6 verification.",
        "config": {"trials": trials, "race_window_us": window_us, "buffer_bytes": size, "random_seed": seed},
        "summary": {
            "snapshot_in_window_count": len(in_window),
            "snapshot_out_of_window_count": len(results) - len(in_window),
            "clean_count": counts["clean"],
            "mutated_count": counts["mutated"],
            "corrupted_count": counts["corrupted"],
            "trials_with_post_freeze_completed_writes": sum(x > 0 for x in delta),
            "counter_delta_total": sum(delta),
            "counter_delta_max": max(delta, default=0),
            "freeze_request_to_stop_observed_ms": {
                "min": min(delays, default=0),
                "median": statistics.median(delays) if delays else 0,
                "p95": quantile(delays, 0.95),
                "p99": quantile(delays, 0.99),
                "max": max(delays, default=0),
            },
        },
        "limitations": [
            "No eBPF, seccomp, signals, cgroups, process_vm_writev or kernel enforcement is exercised.",
            "The agent pause acknowledgment is simulated and does not freeze shared memory or external writers.",
            "The mutator is cooperative; stop_observed means it read the stop command, not that a kernel kill completed.",
            "The observer is a distinct process but shares the operating system, memory, timebase, and test operator.",
            "User-space perf_counter_ns readings, buffer reads and write counts are not externally attested.",
            "Finite trials cannot establish universal prevention of prohibited effects or atomicity.",
            "The intended experiment is designed to detect races, not certify containment.",
        ],
        "verdict": "MEASURED — synthetic only; C3/C6 remains NOT VERIFIED",
        "trials": results,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--trials", type=int, default=1000)
    parser.add_argument("--window-us", type=int, default=1000)
    parser.add_argument("--buffer-bytes", type=int, default=512)
    parser.add_argument("--seed", type=int, default=303)
    parser.add_argument("--output", type=Path, default=Path("kgs_003_evidence_002_results.json"))
    args = parser.parse_args()
    if not 1 <= args.trials <= 20000:
        parser.error("--trials must be in 1..20000")
    if not 100 <= args.window_us <= 100000:
        parser.error("--window-us must be in 100..100000")
    if not 16 <= args.buffer_bytes <= 4096:
        parser.error("--buffer-bytes must be in 16..4096")
    outcome = run(args.trials, args.window_us, args.buffer_bytes, args.seed)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(outcome, indent=2), encoding="utf-8")
    print(outcome["label"])
    print(json.dumps(outcome["summary"], indent=2))
    print("Verdict:", outcome["verdict"])
    print("Saved:", args.output)


if __name__ == "__main__":
    main()
