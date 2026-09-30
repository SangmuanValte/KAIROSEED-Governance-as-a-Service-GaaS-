# Release Status and Evidence Matrix

## Current status

This release-preparation branch is based on `main` and intentionally separates confirmed implementation from claims that still require evidence.

| Component / claim | Status | Verification evidence | Remaining boundary |
|---|---|---|---|
| ASTRA policy evaluator | CONFIRMED IMPLEMENTED | `astra/core.py`, `tests/test_core.py` | Evaluation is not enforcement of arbitrary external tools |
| Scope containment | CONFIRMED IMPLEMENTED | Core evaluator + adversarial tests | Mapping semantics must match deployment policy |
| Expiry enforcement | CONFIRMED IMPLEMENTED | Core evaluator + tests | Clock trust remains deployment responsibility |
| Review state | CONFIRMED IMPLEMENTED | Core evaluator + test | Caller must not map REVIEW to execution |
| Drone simulator gate | CONFIRMED IMPLEMENTED | `drone_simulator/`, tests | Simulation is not physical execution |
| TypeScript claim binding | CONFIRMED IMPLEMENTED | `src/kairoseed.ts` | Dedicated TypeScript test suite remains release work |
| Single-use claim transition | IMPLEMENTED, NOT CONCURRENCY-PROVEN | Source path | Atomic consume is not established |
| Evidence records | CONFIRMED IMPLEMENTED | Python decision records / TS evidence sink | Durable and tamper-resistant storage is not established |
| Independent verifier | PLANNED / UNVERIFIED | None | Must be external to proposer/executor trust domain |
| Production tool mediation | PLANNED / UNVERIFIED | None | Every consequential integration needs a real enforcement point |
| Supply-chain provenance | UNVERIFIED | No pinned JS lockfile on current main | Pin and audit dependencies before release |
| Production rollback controls | UNVERIFIED | Deployment-specific | Define and exercise rollback procedure |

## Release rule

Do not convert an implementation observation into a stronger guarantee without additional evidence.

```
implementation exists
    ≠
invariant tested
    ≠
integration enforced
    ≠
production verified
    ≠
universal guarantee
```

## Evidence required for a stronger release claim

Before calling the system production-ready, require evidence for:

- complete mediation at every consequential integration boundary;
- identity and authority provenance;
- atomic revocation/consumption where required;
- concurrency behavior;
- durable evidence retention and integrity;
- independent verification;
- dependency provenance and vulnerability review;
- CI reproducibility from a clean checkout;
- deployment admission and rollback controls;
- adversarial coverage mapped to every security invariant.
