# KAIROSEED — Evidence and Verification Dossier (2026-11-06)

**Scope:** public repository `SangmuanValte/KAIROSEED-Governance-as-a-Service-GaaS-`, inspected at base revision `9b846da128e2ff325297dfde4a0860267e545313`.  
**Classification:** non-canonical research documentation / evidence inventory.  
**Authoring:** assisted documentation; not an independent audit or external certification.  
**Assurance:** **NOT VERIFIED** for end-to-end protected-effect mediation, JIREH runtime containment, independent L6 assurance, and production release.  
**Canonical specification:** **FROZEN — UNCHANGED**. This dossier adds no permission, deployment, or approval.

## What the repository establishes

The repository contains meaningful *inspectable artifacts*: a Python GaaS prototype with a SQLite hash-linked event ledger and tests; a TypeScript reference adapter; Rego governance policy; an abstract Lean 4 formal model; JIREH configuration/specification; research documentation and versioned Git history. These are **different forms of evidence** with different claim limits. Files appearing in Git do not establish that the actual enforcement boundary is complete or deployed.

- [Per-claim evidence matrix](CLAIM_EVIDENCE_MATRIX.md)
- [Current-head CI finding and reproducible failure](CI_FINDINGS.md)
- [Verification and evidence-collection requirements](VERIFICATION_PROTOCOL.md)
- [Machine-readable research claim inventory](claims.json)
- [Self-contained metadata preflight checker](../../../research/evidence_dossier/preflight.py) — validates dossier metadata **only**, does not issue security PASS.
- [Existing independent containment research issue #30](https://github.com/SangmuanValte/KAIROSEED-Governance-as-a-Service-GaaS-/issues/30)
- [Existing release gate issue #10](https://github.com/SangmuanValte/KAIROSEED-Governance-as-a-Service-GaaS-/issues/10)
- [Pinned JIREH v1.1 non-canonical classification](https://github.com/SangmuanValte/KAIROSEED-Governance-as-a-Service-GaaS-/blob/be03164e5768f2ae6a877efe3a8be647bb7bd757/docs/research/JIREH-v1.1-claim-boundary-and-design-intent.md)
- [JIREH documentation freeze record](https://github.com/SangmuanValte/KAIROSEED-Governance-as-a-Service-GaaS-/blob/9b846da128e2ff325297dfde4a0860267e545313/docs/research/freezes/JIREH-v1.1-design-intent-freeze-2026-11-06.md)

## Evidence ladder and mandatory distinctions

| Level | Question | Valid evidence | What it does NOT establish |
|---|---|---|---|
| D0 — Research notes | Has a testable hypothesis been stated? | dated, versioned scoped specification | implementation |
| D1 — Code present | Is there inspectable code? | exact repository path and commit | executed behavior |
| D2 — Test observed | Was a test actually run? | workflow ID/log, pinned revision, environment, outcome | broader coverage or third-party replication |
| D3 — Behavior under test | Did expected protected effects occur or not occur? | independent effect measurements, causal traces, negative controls | universal absence of bypass |
| D4 — Formal model | Does a theorem hold in its exact model? | checked theorem, assumptions, prover/toolchain | deployed implementation correspondence |
| D5 — Independent replication | Did a separate verifier reproduce claims? | separate identity, pinned artifacts, raw observations and adjudication | production authorization |
| D6 — Production authorization | Are all operational, legal, security and human approvals satisfied? | separately authorized release and operational gates | permanent safety guarantee |

**No verified evidence → No PASS.** `NOT VERIFIED` is not `FAIL`. `FAIL` requires a demonstrated contradiction or failed specified test; `NOT VERIFIED` means coverage, observations, reproducibility, or independent trust is insufficient. A CI `success` is a workflow result for one revision, not a production certification.

## Internal research findings incorporated carefully

Earlier internal KAIROSEED sessions described the capability/authorization distinction, separate GOVANA and JIREH responsibilities, versioned frozen claims, evidence-ledger constraints, restoration/replay boundaries, anti-bypass tests, and non-atomic Sign → Kill. These are recorded here as **research provenance**, not as externally verified code executions.

Some prior discussions recorded local synthetic or educational tests. Without the original exact runnable source, environment, raw trace and independent reproduction, they are **not imported as proof of kernel enforcement, a Lyapunov bound, or C3/C6**. Private working records, personal data, credentials, correspondence and unreviewed private repositories are not copied into this public dossier.

## Assurance constraints

1. **Freeze claims before tests**, using canonical bytes and independently checkable commitment chronology; a later Git commit cannot retroactively establish a pre-test freeze.
2. **Bind the actual effect to the grant**, including actor, operation, resource, bounds, policy, TTL/revocation semantics and causal identifiers.
3. **Inspect effects independently**, including intermediate and external effects, direct tool paths and observation coverage.
4. **Preserve counterexamples and previous claim versions**. Narrowing a contradicted claim creates a new version; it cannot overwrite the earlier assertion.
5. **Never infer containment from audit logs or equal endpoint hashes**. Avoid labels such as *atomic*, *non-preemptible*, *proven safe* absent claim-specific evidence.
6. **Keep implementation repair and production authorization separate** from this documentation.

## Current overall result

**Research and implementation artifacts: DOCUMENTED.**  
**Current-head GaaS workflow: FAILED (specific test defect documented).**  
**Independent JIREH containment, external-effect noninterference and release assurance: NOT VERIFIED.**  
**Production deployment: NOT AUTHORIZED.**
