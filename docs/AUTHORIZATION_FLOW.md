# Authorization Flow

## Canonical flow

```
1. Agent proposes action
2. Construct execution request
3. Resolve authority
4. Validate identity/binding
5. Evaluate policy
6. Check scope/resources/time
7. Decide ALLOW / BLOCK / REVIEW
8. Enforce decision at execution boundary
9. Execute only after ALLOW
10. Verify resulting state independently
11. Record evidence
```

## ASTRA reference flow

```text
ExecutionRequest
      |
      +-- actor allowed? -------- no --> BLOCK
      +-- capability allowed? --- no --> BLOCK
      +-- action allowed? ------- no --> BLOCK
      +-- resource allowed? ----- no --> BLOCK
      +-- not expired? ---------- no --> BLOCK
      +-- scope contained? ------ no --> BLOCK
      +-- resource limits? ------ no --> BLOCK
      +-- purpose present? ------ no --> BLOCK
      +-- review-only action? --- yes -> REVIEW
      |
     ALLOW
```

The evaluator returns a decision and reasons. The drone simulator demonstrates the next enforcement step by refusing to perform the simulated state transition when the decision is BLOCK.

## Important distinction

`evaluate()` is not itself a universal execution gate.

A deployment must place the final authorization check at the actual side-effect boundary.

## Failure handling

A blocked request should preserve:

- request identity/correlation;
- decision;
- reason;
- policy/version identity where available;
- timestamp;
- relevant evidence.

A failed evidence write should not be treated as proof of safe execution. Production policy should explicitly define whether inability to record required evidence blocks the side effect.

## Authorization lifecycle

```
ISSUED → ACTIVE → USED / REVOKED / EXPIRED
```

The TypeScript reference adapter implements these claim states, but atomic state transitions under concurrent workers are **not established**.
