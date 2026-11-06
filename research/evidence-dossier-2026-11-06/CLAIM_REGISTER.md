# Claim Register — Working Research Assertions

**Classification:** Non-canonical *draft registry*. This document has **not** been independently precommitted before historical tests and does not turn retrospective claims into frozen claims. The [freeze protocol](VERIFICATION_PROTOCOL.md) applies to future testing.

| ID | Frozen-worthy testable statement / research obligation | Current evidence | Current assurance |
|---|---|---|---|
| K-C01 | Within a specified protected-resource boundary, every protected effect is covered by a valid action-bound, unrevoked grant. | Source adapter checks a callback path; other paths remain unproven. | NOT VERIFIED |
| K-C02 | Enumerated unauthorized attempts produce zero prohibited effects *for the observed routes, fixtures, times and resources*. | Falsifier requirements in issue #30; no independent trace bundle from those tests here. | NOT VERIFIED |
| K-C03 | The independent observer covers intermediate state, direct paths and relevant external effects, with declared shared trust assumptions. | Design and review questions. | NOT VERIFIED |
| K-C04 | Grants cannot be replayed or consumed concurrently beyond policy-defined limits. | TS reference implementation has a non-atomic check→execute→save sequence; source documents risk. | NOT VERIFIED / known design gap |
| K-C05 | Revocation is enforced at the defined *effect boundary*, including TOCTOU semantics. | Callback-level checks are insufficient to establish in-flight revocation. | NOT VERIFIED |
| K-C06 | Evidence accurately represents committed protected effects, including partial tool failure, log outage and retries. | Source events record callback outcome; no independent effect observer. | NOT VERIFIED |
| K-C07 | JIREH can PAUSE/quarantine then witness and terminate without unauthorized effects in its stated boundary. | Ordered non-atomic design with known window; no verified kernel implementation. | NOT VERIFIED |
| K-C08 | An explicit Lyapunov functional `V(x)` and threshold are defined and enforced for a named system. | G1 unresolved; design intent only. | NOT VERIFIED |
| K-C09 | A specified spectral viability window and `delta_min` detect the declared property under a pinned test. | G2 unresolved; design intent only. | NOT VERIFIED |
| K-C10 | PTZ constraints are correctly compiled into an enforceable runtime policy artifact with checked semantics. | G3 unresolved; not a deployed compiler proof. | NOT VERIFIED |
| K-C11 | An independent per-claim verdict is tied to a verifiably pre-test frozen claim hash, execution and evidence bundle. | Proposed verdict contract; current documentary freeze does not prove historical precommitment. | NOT VERIFIED |
| K-C12 | Release is permitted only after all release gates and independently inspected protections have passed. | Policy requirement exists; current inspected GaaS CI failed. | RELEASE HOLD |

## Mandatory per-claim record for future test runs

For each claim: `claim_id`, unambiguous statement, owner, exact resources/actions, permitted/prohibited effects, assumptions, falsifier, scope, exclusions, version, deterministic encoding, SHA-256 commitment, and independently checkable evidence that the commitment predates execution.

For each result: `test_id`, `claim_hash`, code revision, test fixture, attempted action, observer and trust dependencies, raw trace hashes, effect attribution, coverage limitations, verdict, and independent reviewer assessment.

**Allowed per-claim verdicts:** CONFIRMED WITHIN SCOPE (only if all evidence gates are met), CONTRADICTED (counterexample established), INCONCLUSIVE. System-level statuses **PASS / FAIL / NOT VERIFIED** must be derived from the contract, not inferred from author labels.

No post-hoc scope movement. A narrower successor gets a **new** version; original claim, results and counterexample remain preserved. **No verified evidence → No PASS.**
