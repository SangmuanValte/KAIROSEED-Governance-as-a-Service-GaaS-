# KGS-003-EVIDENCE-002 — Synthetic Race Experiment Provenance

**Classification:** local synthetic experiment; **NOT** JIREH/eBPF/seccomp/kernel containment verification.  
**Relationship:** non-canonical educational research supporting questions raised by issue #30.

A prior local experiment used three Python child processes and a harmless shared-memory buffer. One process requested a cooperative pause, a second modified its authorized shared test buffer, and a third observed snapshots. **No Linux kernel freeze, privileged memory access, real external effects, or production JIREH service was exercised.**

## Preserved local artifacts inspected for this dossier

| Artifact | SHA-256 |
|---|---|
| `kgs_003_evidence_002.py` | `1e33fed887deca926b8478dc6bb4cb4eb1c6f28852bb5dbf7a5c2727af22bbf8` |
| `kgs_003_evidence_002_results.json` | `5d7f708db495e6a22310a80c490e72195f430ff4d2846b3c3abdf9671b85a03f` |
| `KGS-003-EVIDENCE-002-README.md` | `4a366d821c88dc5a892af332797ddac2b6cde2db7966e3575f269884e53742f4` |

These are hashes of local conversation artifacts **observed during dossier preparation**. The underlying source script and raw 1,000-trial JSON are **not uploaded into this GitHub branch**. Therefore the digest entries are provenance pointers, not GitHub-accessible independent reproduction evidence.

## Inspectable sample summary

- Configured trials: **1,000**; random seed: **303**; requested window: **1,000 microseconds**.
- In-window snapshot samples: **971**; outside-window: **29**.
- Within the observed window: **0 clean**, **737 mutated**, **234 corrupted/torn**.
- Trials with post-request writes: **999/1,000**.
- Median synthetic request-to-cooperative-stop acknowledgement: **1.267 ms**; p95 **1.608 ms**; maximum **1,384.740 ms**, including the outlier.

The numbers were read from the preserved sample JSON; they are not a newly rerun experiment or a third-party reproduction.

## Valid inference

This synthetic setup exhibits concurrent changes despite a cooperative pause request. Its measurements **do not establish atomic Freeze–Sign–Kill behavior, real JIREH runtime performance, eBPF signal semantics, or independently verified C3/C6 containment**.

A peer reviewer needs the exact raw bytes, execution environment, validated code, and separate reproduction before upgrading even the synthetic empirical claim.

**JIREH C3/C6 assurance remains NOT VERIFIED. No verified evidence → No PASS.**
