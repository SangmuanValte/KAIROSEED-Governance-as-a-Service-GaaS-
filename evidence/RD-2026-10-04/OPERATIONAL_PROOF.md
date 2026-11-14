# KAIROSEED — Independent-Style R&D Operational Proof

**Record date:** 2026-10-04  
**Baseline:** `main@384cc7025a07de8cab9dac4d5a0bfa3cc450d488`  
**Discipline:** `Claim <= Evidence <= Established Scope`

## Purpose

This record converts the Independent-Style R&D critique into an operational gate. It preserves unresolved findings instead of promoting them to PASS.

## Observed baseline

GitHub Actions run `36940347874` completed with **failure** on the baseline commit.

Observed step state:

- checkout: PASS
- Python setup: PASS
- dependency installation: PASS
- source compilation: PASS
- full test suite: **FAIL**
- production gate metadata: SKIPPED
- immutable run identity: SKIPPED

Therefore:

```text
SPECIFICATION: PRESENT
SOURCE COMPILATION: PASS (for observed CI run)
FULL TEST SUITE: FAIL
PRODUCTION GATE: NOT REACHED
INDEPENDENT VERIFICATION: PENDING
DEPLOYMENT: BLOCKED
```

No stronger claim is authorized by this record.

## Unresolved judgments

### UJ-01 — Full test-suite failure

**State:** OPEN / BLOCKING

The latest observed CI run did not pass the full test suite. The exact failing assertion or test must be recovered from CI output or reproduced in a controlled environment before repair.

**Closure evidence required:** failing test identity, reproduction command, observed failure, corrective change, regression test, and a subsequent passing run.

### UJ-02 — Single-use authorization concurrency

**State:** OPEN / BLOCKING FOR PRODUCTION CLAIMS

The reference adapter's in-memory claim consumption is not atomic. Concurrent requests may observe the same ACTIVE claim before either persists USED.

**Closure evidence required:** an atomic consume/lease mechanism plus a concurrency test showing at most one protected effect for one single-use authorization under the stated test conditions.

### UJ-03 — Tool error vs protected-state outcome

**State:** OPEN

A consequential tool can potentially change external state and then throw. An `executed: false` result is therefore not sufficient evidence that protected state remained unchanged.

**Closure evidence required:** independent before/after observation of a harmless protected test resource, operation identity, and explicit UNKNOWN handling when final state cannot be established.

## Proof target P1

For a defined harmless protected resource and bounded threat model:

```text
NOT Authorized(action)
    => no protected state delta attributable to that action
```

This is a test target, not a universal guarantee.

## Acceptance matrix

| Test | Expected observation |
|---|---|
| Missing claim | BLOCK; protected state unchanged |
| Revoked claim | BLOCK; protected state unchanged |
| Expired claim | BLOCK; protected state unchanged |
| Subject/action/scope substitution | BLOCK; protected state unchanged |
| Parameter substitution | BLOCK; protected state unchanged |
| Single-use replay | second request BLOCK; one protected effect maximum |
| Concurrent single-use requests | at most one protected effect |
| Tool throws after attempted effect | final state independently observed; never infer unchanged state from exception alone |

## Evidence bundle required for PASS

A PASS must identify:

1. exact commit SHA;
2. runtime and dependency versions;
3. test command;
4. raw test output;
5. protected-state before/after observations;
6. authorization decision evidence;
7. unresolved limitations;
8. CI run identity.

If any mandatory item is unavailable, classification remains **UNVERIFIED**, **WARN**, or **BLOCK**, as appropriate.

## Current verdict

```text
KAIROSEED R&D PHASE: ACTIVE
OPERATIONAL PROOF: IN PROGRESS
LATEST OBSERVED CI: FAIL
UNRESOLVED JUDGMENTS: PRESERVED
PRODUCTION CLAIM: BLOCKED
NEXT ACTION: reproduce the failing suite before architecture expansion
```

The ecosystem remains preserved; failure evidence is retained rather than overwritten by a success narrative.
