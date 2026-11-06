# Claim-to-Evidence Matrix

**Review basis:** GitHub source and workflows visible on 2026-11-06. **This is not an exhaustive audit of the entire repository**, nor proof of implementation correctness. All paths below refer to the public `SangmuanValte/KAIROSEED-Governance-as-a-Service-GaaS-` repository. Prefer exact commit/revision and raw logs to prose summaries.

| ID | Claim / proof obligation | Inspectable evidence | Defensible state | Missing evidence / falsifier |
|---|---|---|---|---|
| KGS-001 | Capability is distinct from authority | `README.md`, `docs/ARCHITECTURE.md` | SPECIFIED | Actual mandatory cross-path enforcement |
| KGS-002 | GaaS decision model and hash-linked SQLite ledger exist | `prototypes/kairoseed-gaas-v0.1/kairoseed_gaas.py` | CODE PRESENT; NOT INDEPENDENTLY VERIFIED | trusted observer, external effect correlation, durability and crash/concurrency test reproduction |
| KGS-003 | Current-head prototype test suite is green | `.github/workflows/kairoseed-gaas.yml`, [run 42264348902](https://github.com/SangmuanValte/KAIROSEED-Governance-as-a-Service-GaaS-/actions/runs/42264348902) | **CONTRADICTED for inspected commit**: 1 fail / 19 pass | fix flawed test setup and rerun; evidence must bind new SHA |
| KGS-004 | Older prototype workflow has passing tests | [run 37677125279](https://github.com/SangmuanValte/KAIROSEED-Governance-as-a-Service-GaaS-/actions/runs/37677125279) | OBSERVED CI SUCCESS on older revision only (26 tests) | Does not establish current-head CI or production readiness |
| KGS-005 | Adapter checks claim validity before its own callback | `src/kairoseed.ts`, `docs/ADAPTER.md` | CODE PRESENT; bounded adapter behavior only | direct callback path, atomic single-use, post-check revocation/TOCTOU, external effects |
| KGS-006 | GOVANA Rego enforces epoch and evidence scope | `governance/govana_core.rego` | CODE PRESENT; model policy only | real PEP integration, pinned OPA tests, deployment mediation |
| KGS-007 | Claim ≤ Evidence ≤ Scope is formally represented | `formal/verification.lean`, `lean-toolchain` | FORMAL SOURCE PRESENT | current clean-checkout Lean checker log; concrete runtime refinement proof |
| KGS-008 | JIREH v1.1 uses eBPF/seccomp as enforced boundary | `governance/jireh_ebpf.yaml`, `docs/research/JIREH-v1.1-claim-boundary-and-design-intent.md` | **NOT IMPLEMENTED / NOT VERIFIED** as specified by manifest | actual programs, kernel hook coverage, telemetry, independent effect measurements |
| KGS-009 | JIREH Lyapunov and spectral monitoring constrain effects | `docs/SIGMASTAR.md`, `governance/jireh_ebpf.yaml` | RESEARCH DIRECTION ONLY | defined V(x), derivative/threshold criteria, δ_min and viable state, G1/G2 evidence |
| KGS-010 | PTZ-to-JIREH compiler preserves checked constraints | JIREH master research requirements; related docs | NOT VERIFIED; G3 OPEN | compiler source, proof/semantics mapping, hash linkage, checked generated policy |
| KGS-011 | Complete mediation and unauthorized-effect containment | [issue #30](https://github.com/SangmuanValte/KAIROSEED-Governance-as-a-Service-GaaS-/issues/30), `docs/THREAT_MODEL.md` | TEST CONTRACT DOCUMENTED; PROPERTY NOT VERIFIED | independent protected-state observer, route coverage argument, raw effect traces, adversarial reproductions |
| KGS-012 | Signed and independently checked L6 finality | `governance/receipt_v1.schema.json`, `docs/EVIDENCE.md` | SCHEMA/DESIGN DOCUMENTED | real signed receipts, independent chronology, tamper-resistant retention, chain replay against observed state |
| KGS-013 | Atomic Freeze–Sign–Kill and race-proof containment | JIREH v1.1 classification and freeze records | **ATOMICITY NOT ESTABLISHED; NON-ATOMIC WINDOW ACKNOWLEDGED** | effect denial before signing, pause confirmation, measured termination races, reproducible C3/C6 tests |
| KGS-014 | A per-claim frozen verdict contract prevents post-hoc scope changes | Research documentation and claim-freeze discussions | PROPOSED CONTRACT; NOT VERIFIED AS ENFORCED | pre-test content hash, append-only commitments, test binding, per-claim verdicts, correction lineage |
| KGS-015 | Release-ready independent verification | `prototypes/kairoseed-gaas-v0.1/INDEPENDENT_VERIFICATION.md`, `PRODUCTION_READINESS.md` | NOT VERIFIED; release gate open | clean independent checkout, green exact-head CI, artifact provenance, independent reviewer and protected deployment controls |
| KGS-016 | Release CI proves independent verification | `.github/workflows/kairoseed-gaas-release.yml` | **NOT ESTABLISHED** | workflow currently prints `INDEPENDENT_VERIFICATION=PASS` as a literal string; must verify a separate verifier artifact or remove that assurance claim |

## Current source-specific defects / limitations

- `tests/test_core.py` and `tests/injection_tests.py` test bounded policy models; presence does not imply end-to-end observed execution effects.
- `tests/test_security_invariants.py` is under the prototype. Its tamper test mutates `ledger.records[0]`, but `EvidenceLedger.records` builds a fresh list of dictionaries from SQLite. The mutation does not alter stored data; `verify_chain()` therefore returns true. CI observes `assert not True`. See [CI_FINDINGS.md](CI_FINDINGS.md).
- `src/kairoseed.ts` accepts a caller-provided `tool` callback not cryptographically bound to a grant; it cannot by itself prove that all consequential effects are authorized or solely mediated by that adapter.
- The TypeScript adapter consumes `singleUse` after the callback; its own `docs/ADAPTER.md` discloses the concurrency gap.
- The Rego `allow` rule as written checks epoch/scope violations only; broader identity, signature, revocation and resource binding require separate mechanisms.
- `formal/verification.lean` proves implications **under model premises**; it does not show that a real executor satisfies those premises.

## Interpretation

A genuine counterexample contributes to the work. Source/code inspection can identify likely defects, but should not be confused with an executed adversarial test. Falsification must specify which frozen claim and implementation revision it actually contradicts. Do not silently narrow scope after observing results.

**Claim ≤ Evidence ≤ Established Scope. No verified evidence → No PASS.**
