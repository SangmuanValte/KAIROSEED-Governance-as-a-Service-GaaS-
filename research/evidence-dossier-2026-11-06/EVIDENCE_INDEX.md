# Evidence Index — Inspected Artifacts and Provenance

**Baseline:** `9b846da128e2ff325297dfde4a0860267e545313` · **Reviewed:** 2026-11-06. Source existence/metadata is distinguishable from proof of correctness.

| ID | Evidence source (pinned) | What it establishes | What it does NOT establish |
|---|---|---|---|
| E01 | [Python GaaS prototype](https://github.com/SangmuanValte/KAIROSEED-Governance-as-a-Service-GaaS-/blob/9b846da128e2ff325297dfde4a0860267e545313/prototypes/kairoseed-gaas-v0.1/kairoseed_gaas.py) | Source has explicit predicates and a SHA-256-linked transactional SQLite ledger with process-local lock | Third-party authorization, external effect mediation, immutable storage, independent observer |
| E02 | [Python security tests](https://github.com/SangmuanValte/KAIROSEED-Governance-as-a-Service-GaaS-/blob/9b846da128e2ff325297dfde4a0860267e545313/prototypes/kairoseed-gaas-v0.1/test_security_invariants.py) | Eight named cases; one test mutates a detached `ledger.records` copy | That persisted tampering was simulated by that test, or a full suite passed |
| E03 | [GaaS Actions run 42264348902](https://github.com/SangmuanValte/KAIROSEED-Governance-as-a-Service-GaaS-/actions/runs/42264348902) | Completed workflow concluded **failure** at base revision; audit identifies 19 passed / one failed | Independent containment or release success |
| E04 | [TypeScript adapter](https://github.com/SangmuanValte/KAIROSEED-Governance-as-a-Service-GaaS-/blob/9b846da128e2ff325297dfde4a0860267e545313/src/kairoseed.ts) | Checks claim status, expiry, policy, subject/action/scope and optional parameter hash before invoking its callback | Atomic claim consumption, impossibility of direct tool bypass, zero external effects on error |
| E05 | [Adapter documentation](https://github.com/SangmuanValte/KAIROSEED-Governance-as-a-Service-GaaS-/blob/9b846da128e2ff325297dfde4a0860267e545313/docs/ADAPTER.md), [threat model](https://github.com/SangmuanValte/KAIROSEED-Governance-as-a-Service-GaaS-/blob/9b846da128e2ff325297dfde4a0860267e545313/docs/THREAT_MODEL.md) | Documents single-use concurrency risk and eight denial scenarios; names further out-of-scope paths | Those eight scenarios passed on the inspected commit or exhaust all bypasses |
| E06 | [Evidence format](https://github.com/SangmuanValte/KAIROSEED-Governance-as-a-Service-GaaS-/blob/9b846da128e2ff325297dfde4a0860267e545313/docs/EVIDENCE.md) | Defines reference adapter BLOCKED/EXECUTED/VERIFICATION event fields | Independent protected-state measurements or secure ledger provenance |
| E07 | [Abstract Lean source](https://github.com/SangmuanValte/KAIROSEED-Governance-as-a-Service-GaaS-/blob/9b846da128e2ff325297dfde4a0860267e545313/formal/verification.lean) | Defines abstract subset and epoch-based authority properties and theorem statements | Checked build in this review, correct real-world semantics, or refinement proof for runtime |
| E08 | [Kernel-binding design YAML](https://github.com/SangmuanValte/KAIROSEED-Governance-as-a-Service-GaaS-/blob/9b846da128e2ff325297dfde4a0860267e545313/governance/jireh_ebpf.yaml) | Explicitly says `SPECIFICATION_NOT_IMPLEMENTATION` and `NOT_IMPLEMENTED` eBPF adapter | Running kernel isolation |
| E09 | [Release workflow](https://github.com/SangmuanValte/KAIROSEED-Governance-as-a-Service-GaaS-/blob/9b846da128e2ff325297dfde4a0860267e545313/.github/workflows/kairoseed-gaas-release.yml) | Can build/attest an artifact when its checks run and pass; contains an echo of `INDEPENDENT_VERIFICATION=PASS` | Independent attestation, external production gate review or release authorization |
| E10 | [Production-readiness record](https://github.com/SangmuanValte/KAIROSEED-Governance-as-a-Service-GaaS-/blob/9b846da128e2ff325297dfde4a0860267e545313/prototypes/kairoseed-gaas-v0.1/PRODUCTION_READINESS.md) | Declares required readiness gates; some remain pending | Gate satisfaction without separately inspected evidence |
| E11 | [JIREH claim/design boundary](https://github.com/SangmuanValte/KAIROSEED-Governance-as-a-Service-GaaS-/blob/be03164e5768f2ae6a877efe3a8be647bb7bd757/docs/research/JIREH-v1.1-claim-boundary-and-design-intent.md) | Source-documented division between specified doctrine and proposed mechanisms | Operational JIREH v1.1 proof |
| E12 | [JIREH freeze declaration](https://github.com/SangmuanValte/KAIROSEED-Governance-as-a-Service-GaaS-/blob/9b846da128e2ff325297dfde4a0860267e545313/docs/research/freezes/JIREH-v1.1-design-intent-freeze-2026-11-06.md) | Commit and document SHA-256 recorded as a research documentation snapshot | Independently witnessed pre-test claim freeze or immutable storage |
| E13 | [Independent containment issue #30](https://github.com/SangmuanValte/KAIROSEED-Governance-as-a-Service-GaaS-/issues/30) | Scoped claim/test contract, falsifier matrix, verifier trust questions | Executed bypass tests or verified containment |

## Internal research records (held separately, **not** uploaded as raw evidence)

- **2026-10-04 research review:** Reports specific local finite tests (including selected ledger/counter results) and TypeScript adapter weaknesses at a historical pinned revision `384cc7025a07de8cab9dac4d5a0bfa3cc450d488`. This is a past review, not re-execution in this dossier.
- **2026-11-06 read-only integration audit:** Reports local reconstructed GaaS 7/8 failing then 8/8 after a test-only correction, while latest remote CI remained failed. It explicitly distinguishes a reconstructed subset from a byte-for-byte clone.
- **2026-11-06 JIREH lock record:** Preserves the non-atomicity correction, PTZ/Lyapunov/spectral/compiler gaps, and need for independently observed protected effects.
- **2025–2026 research history:** Retrospective chronology with gaps and separate code lineage; contemporary provenance is incomplete for some dates.

The contents of these separate research documents are summarized for review but **not** presented as uploaded raw traces, signed receipts, or independently reproduced evidence. Public release of private research records should be reviewed for confidentiality and provenance.

## Required metadata for any newly added evidence

Every result must link: (a) claim ID and exact pre-test hash; (b) repository revision, runtime/toolchain versions, fixture, adversary capability and observation window; (c) raw evidence digest and observer identity/trust boundary; (d) expected vs observed results; (e) completeness of instrumentation and effects; (f) per-claim verdict with signed/linked correction history where applicable.

Do not label a successful workflow, a signed hash, or a matching before/after snapshot as proof of unobserved effects being impossible.
