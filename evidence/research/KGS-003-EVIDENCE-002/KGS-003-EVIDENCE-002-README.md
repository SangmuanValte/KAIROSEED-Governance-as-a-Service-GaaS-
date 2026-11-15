# KGS-003-EVIDENCE-002 — Synthetic race-window measurement

**RED DRILL — SYNTHETIC ONLY. NOT A CLAIM ABOUT JIREH v0.4 PERFORMANCE. NOT A CLAIM ABOUT eBPF, SECCOMP, OR REAL KERNEL ISOLATION.**

This is an illustrative three-child-process, standard-library Python experiment. A simulated agent acknowledges PAUSE, a separate mutator edits a harmless shared buffer in parallel, and a separate observer samples the buffer. The parent requests PAUSE and later requests the mutator to stop. The mutator's acknowledgement of a *cooperative stop* is not a Linux SIGKILL observation. No process is frozen by a kernel mechanism; this does not simulate how `bpf_send_signal` works.

## Run

```bash
python kgs_003_evidence_002.py --trials 1000 --window-us 1000 --seed 303 --output results.json
```

The script needs Python 3.9+ and uses only the standard library. The configured delay is a requested wait, **not** a guaranteed real-time interval; actual timings vary widely with system scheduling and load. Run on a machine you control. Each trial records a monotonic user-space timestamp sequence, an observer snapshot hash/class, and completed mutator writes. These observations are not independently authenticated.

## Sample run (this environment)

- Trial count: **1,000**; usable in-window snapshots: **971**; samples outside the requested window: **29**.
- Among in-window snapshots: **0 clean**, **737 mutated**, **234 corrupted/torn**.
- Trials with one or more completed post-request mutations: **999/1,000**.
- Completed write cycles between synthetic freeze request and cooperative-stop acknowledgement: **10,254**, maximum **22** in a trial.
- Freeze request → cooperative stop acknowledged, milliseconds: median **1.267**, p95 **1.608**, p99 **2.255**, maximum **1384.740** (large scheduling outlier, retained).

These numbers measure **only this synthetic program and environment**. Reproduction on different systems will vary. The one outlier must not be silently removed.

## Correct interpretation

**MEASURED — synthetic cooperative-stop race.** This makes visible that a pause *request or acknowledgement* from one process does not prevent a different process with shared write access from modifying the buffer. It **does not prove JIREH non-atomicity, kernel freezer latency, seccomp behavior, SIGSTOP semantics, full protected-state containment, or C3/C6 assurance**.

The mock observer runs as a separate process but shares the same OS, clock, and memory trust boundary. Snapshot equality alone cannot rule out transient writes that were later reversed. The record has no kernel-generated timestamps, signed L6 attestations, independent deployment, or comprehensive path inventory.

## Verdict rule

No PASS / FAIL for real JIREH is justified from these samples. **C3/C6 remains NOT VERIFIED**. Actual C3/C6 testing requires an explicitly scoped and authorized kernel-instrumented implementation, trustworthy protected-effect observations, and independently reproducible evidence. A real result may be PASS / FAIL / NOT VERIFIED only for a pre-frozen claim under stated assumptions.
