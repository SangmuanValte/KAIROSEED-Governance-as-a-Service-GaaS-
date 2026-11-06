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

These SHA-256 values were computed from the previously generated local artifacts. On **2026-11-07**, all three original files were archived byte-for-byte in [`evidence/research/KGS-003-EVIDENCE-002/`](../../../evidence/research/KGS-003-EVIDENCE-002/) on the research branch, and their GitHub read-back contents matched the supplied files.

- [Raw Python source](../../../evidence/research/KGS-003-EVIDENCE-002/kgs_003_evidence_002.py)
- [Raw 1,000-trial JSON](../../../evidence/research/KGS-003-EVIDENCE-002/kgs_003_evidence_002_results.json)
- [Original experiment README](../../../evidence/research/KGS-003-EVIDENCE-002/KGS-003-EVIDENCE-002-README.md)
- [Source, artifact and environment provenance manifest](../../../evidence/research/KGS-003-EVIDENCE-002/PROVENANCE.json)
- [Offline archive integrity checker](../../../evidence/research/KGS-003-EVIDENCE-002/verify_archive.py)

The source and result bytes are now inspectable, but the historical execution environment was **not fully recorded** and this GitHub revision was committed **after** the sample run. Neither this archive nor its hashes prove pre-test claim freezing, original runtime identity, independent reproduction, eBPF enforcement, or C3/C6.

## Inspectable sample summary

- Configured trials: **1,000**; random seed: **303**; requested window: **1,000 microseconds**.
- In-window snapshot samples: **971**; outside-window: **29**.
- Within the observed window: **0 clean**, **737 mutated**, **234 corrupted/torn**.
- Trials with post-request writes: **999/1,000**.
- Median synthetic request-to-cooperative-stop acknowledgement: **1.267 ms**; p95 **1.608 ms**; maximum **1,384.740 ms**, including the outlier.

The numbers were read from the preserved sample JSON; they are not a newly rerun experiment or a third-party reproduction.

## Valid inference

This synthetic setup exhibits concurrent changes despite a cooperative pause request. Its measurements **do not establish atomic Freeze–Sign–Kill behavior, real JIREH runtime performance, eBPF signal semantics, or independently verified C3/C6 containment**.

A peer reviewer can now inspect the archived source and raw bytes, but the original runtime environment remains incompletely recorded, and separate reproduction and observational trust review remain outstanding. No broad assurance can be upgraded.

**JIREH C3/C6 assurance remains NOT VERIFIED. No verified evidence → No PASS.**
