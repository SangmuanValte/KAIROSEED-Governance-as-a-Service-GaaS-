# Security Model

## Security objective

Prevent an AI agent's available capability from being mistaken for authority to cause a consequential side effect.

## Trust boundaries

```
[Agent / Model]
    untrusted as authority
          |
          v
[Proposal / Request]
          |
          v
[Policy + Authorization]
    trusted decision boundary
          |
          v
[Execution Gate]
    enforcement boundary
          |
          v
[Tool / External System]
    side effect
          |
          v
[Independent Verification]
    observation boundary
          |
          v
[Evidence]
```

The exact deployment may split these components across processes or services. The security property is the separation of authority, execution, and observation—not the names of the components.

## Authority model

Authority must be:

- explicit;
- bounded by actor, action, resource, and scope;
- time-bounded where appropriate;
- bound to the policy version or equivalent policy identity;
- revocable where required;
- independently attributable.

The model/agent may propose an action. It does not create its own authorization.

## Enforcement requirement

A policy evaluator alone is insufficient if an agent can invoke the underlying tool through another path.

Therefore a production integration must enforce:

```
ALLOW
  ↓
actual tool boundary
  ↓
side effect
```

and must ensure:

```
BLOCK
  ↓
no consequential side effect through that governed path
```

## Fail-closed conditions

The reference ASTRA evaluator blocks when mandatory actor, capability, action, resource, expiry, scope, resource-limit, or purpose constraints fail.

Production systems must also define fail-closed behavior for:

- unavailable authorization service;
- stale policy;
- unverifiable identity;
- malformed authorization;
- replay;
- evidence-write failure;
- verifier disagreement;
- integration timeout;
- partial execution.

## Security claims

**Confirmed:** the reference evaluator implements deterministic authorization predicates.

**Unverified:** that those predicates protect every possible integration path.

**Unverified:** that the evidence path is tamper-resistant or independently trustworthy.

**Unverified:** that concurrency, process isolation, credentials, network controls, or deployment admission are secure in a production environment.
