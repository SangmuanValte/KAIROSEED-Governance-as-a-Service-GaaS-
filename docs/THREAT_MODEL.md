# Threat Model

The authorization-to-execution boundary is the primary security boundary of the reference system.

| Threat | Expected control | Current status |
|---|---|---|
| Capability confused with authority | Explicit authorization | CONFIRMED in reference evaluator |
| Actor substitution | Actor binding | CONFIRMED |
| Capability substitution | Capability binding | CONFIRMED |
| Action substitution | Action binding | CONFIRMED |
| Resource substitution | Resource binding | CONFIRMED |
| Scope expansion | Scope containment | CONFIRMED |
| Expired authority | Time check | CONFIRMED |
| Review bypass | REVIEW remains non-allow | CONFIRMED at evaluator |
| Parameter substitution | Parameter hash binding | IMPLEMENTED in TS; automated TS evidence pending |
| Sequential replay | Single-use claim state | IMPLEMENTED sequentially |
| Concurrent replay | Atomic consumption | UNVERIFIED |
| Direct tool bypass | Complete mediation | UNVERIFIED |
| Policy-service compromise | Independent policy trust root | UNVERIFIED |
| Evidence tampering | Durable integrity controls | UNVERIFIED |
| Identity compromise | External identity controls | UNVERIFIED |
| Dependency compromise | Pinned/audited supply chain | UNVERIFIED |
| Sensitive data exposure | Secret/data handling controls | UNVERIFIED |
| Serialization disagreement | Canonical request representation | Partially addressed; integration-specific |
| Partial execution | Transaction/compensation semantics | UNVERIFIED |

## Adversarial principle

Do not only test:

```
valid request → ALLOW
```

Test mutations:

```
valid request
  → change actor
  → change capability
  → change action
  → change resource
  → expand scope
  → exceed resource limit
  → expire authorization
  → request review-only action
  → mutate parameters
  → replay authorization
```

Each mutation should produce the expected boundary behavior and, where execution is simulated, prove protected state did not change.

## Release boundary

This threat model is a test plan, not evidence that every threat is solved. Threats marked **UNVERIFIED** remain release risks and must not be converted into security claims.
