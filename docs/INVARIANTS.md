# Security Invariants

These invariants are written as testable statements. Each one must have an implementation point and an adversarial test before being described as enforced.

| ID | Invariant | Current status |
|---|---|---|
| INV-01 | Capability alone cannot authorize an action | CONFIRMED at ASTRA policy boundary |
| INV-02 | Unauthorized actor is blocked | CONFIRMED |
| INV-03 | Unauthorized capability is blocked | CONFIRMED |
| INV-04 | Unauthorized action is blocked | CONFIRMED |
| INV-05 | Unauthorized resource is blocked | CONFIRMED |
| INV-06 | Requested scope must be contained by authority scope | CONFIRMED |
| INV-07 | Expired authority is blocked | CONFIRMED |
| INV-08 | Review does not equal automatic execution | CONFIRMED at evaluator boundary |
| INV-09 | Parameter-bound TypeScript claims reject changed parameters | IMPLEMENTED; dedicated automated evidence pending |
| INV-10 | Single-use authorization cannot be replayed | IMPLEMENTED sequentially; concurrency safety UNVERIFIED |
| INV-11 | Blocked governed action causes no simulated state transition | CONFIRMED in drone simulator tests |
| INV-12 | Evidence is independently trustworthy and durable | UNVERIFIED / PLANNED |
| INV-13 | Every consequential integration is completely mediated | UNVERIFIED / DEPLOYMENT-SPECIFIC |

## Formal boundary

For a governed transition `T`:

```
Execute(T) only if Authorization(T) = ALLOW
```

and for a blocked request:

```
Authorization(T) != ALLOW
⇒
T must not be performed through the governed execution path
```

The second statement is a system property only when the execution boundary is actually enforced.

## Verification discipline

A test can establish:

> Under the test's inputs and execution path, the expected transition did or did not occur.

It cannot establish:

> No other path can ever perform the transition.

That stronger statement requires complete mediation evidence, integration testing, deployment controls, and independent verification.
