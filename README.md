# KAIROSEED Governance-as-a-Service (GaaS)

Verification-first reference architecture for governing consequential actions by AI agents.

> **Capability is not permission.**
>
> **Authorization is not execution.**
>
> **Execution is not evidence.**
>
> **A passing test is evidence under tested conditions, not a universal security guarantee.**

## Release status

**Release-preparation branch:** `release/verification-first-v0.1`

This repository currently contains **reference implementations and research artifacts**. It is not a production-certified authorization service.

| Area | Status | Evidence boundary |
|---|---|---|
| ASTRA deterministic policy evaluation | **CONFIRMED IMPLEMENTED** | `astra/core.py` + `tests/test_core.py` |
| ASTRA governed drone simulator | **CONFIRMED IMPLEMENTED** | `drone_simulator/` + `tests/test_drone_simulator.py` |
| TypeScript claim/execution adapter | **CONFIRMED IMPLEMENTED** | `src/kairoseed.ts` |
| Authorization-before-callback behavior in TypeScript adapter | **IMPLEMENTATION CLAIM — TEST COVERAGE REQUIRED** | Source inspection; dedicated automated suite is a release requirement |
| Adversarial authorization-boundary tests | **CONFIRMED IMPLEMENTED IN RELEASE PREP** | `tests/adversarial/` |
| Independent verification of real external side effects | **PLANNED / UNVERIFIED** | No production executor or independent verifier is established here |
| Durable, tamper-resistant evidence | **PLANNED / UNVERIFIED** | In-memory evidence is reference-only |
| Concurrency-safe single-use authorization | **UNVERIFIED / KNOWN LIMITATION** | Current TypeScript and Python reference paths do not establish atomic consumption |
| Production identity, deployment admission, rollback, and supply-chain controls | **PLANNED / UNVERIFIED** | Deployment-specific |

Do not read a **PLANNED**, **UNVERIFIED**, or **KNOWN LIMITATION** item as implemented.

## Purpose

KAIROSEED separates:

```
Agent capability
      ↓
Proposal / request
      ↓
Policy + authorization
      ↓
Execution gate
      ↓
Consequential operation
      ↓
Independent verification
      ↓
Evidence
```

The central design requirement is that **the component that can perform an action must not be the sole authority deciding that the action is permitted**.

The repository demonstrates this boundary with deterministic policy evaluation and simulated execution. Production integrations must place an enforcement point immediately before the actual consequential side effect.

## Trust model

The reference model treats:

- the **agent/model** as a proposer, not an authority;
- **policy/authorization** as the source of permission;
- the **execution gate** as the enforcement boundary;
- the **executor/tool** as capable of causing the side effect;
- **verification/evidence** as a separate observation path.

Trust is therefore explicit and bounded:

```
Capability ≠ Permission ≠ Authorization ≠ Execution ≠ Evidence
```

A policy decision is not evidence that the side effect occurred. An observed side effect is not evidence that it was authorized.

## Authorization boundary

A request is eligible to execute only when all required authorization predicates hold.

For the ASTRA reference implementation:

- actor is allowed;
- capability is allowed;
- action is allowed;
- resource is allowed;
- authorization is not expired;
- requested scope is contained by authority scope;
- requested resources remain within limits;
- required purpose is present;
- review-only actions do not become automatic execution.

If any mandatory predicate fails, ASTRA returns **BLOCK**.

The TypeScript adapter additionally checks claim state, expiry, policy-version binding, subject/action/scope binding, and optional parameter binding before invoking the tool callback.

## Core invariants

### I1 — Capability does not imply permission

A capability alone cannot produce an authorization decision.

### I2 — No authorization, no governed execution

A request lacking valid authority must be blocked before the governed execution callback.

### I3 — Scope cannot expand through the request

```
requested_scope ⊆ authority_scope
```

### I4 — Expired authority is invalid

An authorization outside its validity window cannot authorize execution.

### I5 — Review is not allow

`REVIEW` is a non-execution state in the reference model.

### I6 — Evidence does not retroactively authorize

An audit record is evidence of what was recorded; it does not create permission.

### I7 — Fail closed at mandatory authorization boundaries

Missing, invalid, expired, or unverifiable mandatory authorization is a block condition.

These are **implementation-level invariants under the stated test conditions**, not universal security theorems.

## Verification approach

KAIROSEED uses:

**Claim → Implementation → Test → Observation → Evidence → Bounded claim**

Verification is split into:

1. **Unit tests** — deterministic policy predicates.
2. **Adversarial tests** — deliberate boundary substitutions and invalid authorization.
3. **Execution tests** — demonstrate that governed simulation state changes only after an allow decision.
4. **Independent verification** — planned for production integrations and must be outside the proposing agent's control.

Run the reference Python suite:

```bash
python -m pytest -q
```

Run adversarial tests explicitly:

```bash
python -m pytest -q tests/adversarial
```

TypeScript compilation/build is a separate repository concern because the current repository does not yet contain a pinned npm lockfile for reproducible dependency installation.

## Example

Authorized:

```text
actor=agent-1
capability=compute
action=mine
resource=worker-1
scope.environment=authorized
cpu=2
→ ALLOW
```

Unauthorized scope expansion:

```text
same authorization
scope.environment=untrusted
→ BLOCK
reason=scope_outside_authority
```

The critical property is not the text of the decision. The test must establish that the consequential callback/state transition is not performed on the blocked path.

See `examples/authorized_unauthorized.py`.

## Failure handling

Mandatory authorization failures are fail-closed in the ASTRA evaluator.

Known reference limitations remain:

- in-memory state is not durable;
- claim consumption is not proven atomic under concurrency;
- evidence is not an immutable ledger;
- the reference evaluator does not itself isolate arbitrary tools;
- no production identity provider is assumed;
- no universal guarantee is claimed for integration boundaries.

## Repository map

```text
astra/                  Confirmed Python authorization reference
src/                    TypeScript reference adapter
drone_simulator/        Simulated consequential execution
tests/                  Verification tests
tests/adversarial/      Adversarial boundary tests
examples/               Reproducible reference examples
docs/                   Architecture, security, verification, operations
governance/             Governance/reference boundary artifacts
evidence/               Evidence fixtures/artifacts; not a production ledger
planned/                Explicitly unimplemented future work
.github/workflows/      CI/release verification
```

See `docs/RELEASE_STATUS.md` for the detailed evidence matrix.

## What this release does not claim

This release does **not** claim:

- production security certification;
- complete mediation of every tool or integration;
- cryptographic attestation of arbitrary execution;
- tamper-proof evidence storage;
- concurrency-safe single-use authorization;
- immunity to compromised infrastructure;
- absence of bypasses outside tested paths;
- a universal proof of the stated invariants.

## Release principle

```text
DESIGN → BUILD → VERIFY → PUBLISH
```

Public claims must track implementation evidence. If an artifact cannot be reproduced or inspected, mark it **UNVERIFIED** rather than silently treating it as true or false.

**Unknown ≠ False.**
