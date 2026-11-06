# CI Observations — Pinned Candidate Head, 2026-11-06

**Review branch:** `research/evidence-package-20261106-verified-scope`  
**Observed head commit:** `28e745d12e4d1de484630e90ae1d1a8fd2ea4c18`  
**Observed environment:** GitHub Actions (Ubuntu runners, Python 3.12 where configured).  
**Scope:** Repository tests of prototypes and document consistency, **not** an independent protected-effect audit.

| Workflow / run | Actual GitHub outcome | What passed or failed | Assurance boundary |
|---|---|---|---|
| [KAIROSEED-GaaS run 42272229544](https://github.com/SangmuanValte/KAIROSEED-Governance-as-a-Service-GaaS-/actions/runs/42272229544) | **success** | Full Python prototype suite: **20 passed**; compile/metadata/identity steps succeeded. Test-only stored-SQLite negative-control repair included. | Supports test suite at this PR head; **does not** prove complete mediation or deployed JIREH containment. |
| [Evidence Dossier run 42272229614](https://github.com/SangmuanValte/KAIROSEED-Governance-as-a-Service-GaaS-/actions/runs/42272229614) | **success** | Python compile and **11 structural tests passed**. | Validates local bundle structure/hash/reference checks, **not** evidence truth, independent chronology or security. |
| [August Pipeline run 42272229660](https://github.com/SangmuanValte/KAIROSEED-Governance-as-a-Service-GaaS-/actions/runs/42272229660) | **failure** | Five tests: four passed, one failed; expected `BLOCKED` but got `HALTED`. | A separate, unresolved status-contract mismatch. Not caused by the dossier's SQLite test-only change based on the inspected code scope, but root cause was not independently traced here. |

## Baseline comparison

[Main GaaS workflow run 42264348902](https://github.com/SangmuanValte/KAIROSEED-Governance-as-a-Service-GaaS-/actions/runs/42264348902), commit `9b846da128e2ff325297dfde4a0860267e545313`: **19 passed, one failed** in the full Python suite. The negative-control test was corrected on the research branch and the branch suite passed 20/20. These are **different** revisions; the failed main result remains historical truth until a separately authorized change is merged and a new main run succeeds.

## Evidence rules

- Workflow success verifies only the steps that actually ran, at their pinned revision and environment.
- An observed `INDEPENDENT_VERIFICATION=PASS` string in a release workflow is not an independent attestation.
- The remaining August Pipeline failure means **overall repository CI is not green** at the observed PR head.
- No runtime kernel, Lyapunov, PTZ compiler, external-effect observer, independent review or L6 WORM integrity was demonstrated by these CI jobs.
- No draft PR is merged or authorized for production by these runs.

**Disposition:** Structural verifier tests **PASS within their narrow test scope**; GaaS Python suite **PASS for proposed branch revision**; August Pipeline **FAIL**; end-to-end governance assurance **NOT VERIFIED**; production release **BLOCKED**.

**No verified evidence → No broad PASS.**
