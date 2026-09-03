# automate.prototype

**Capability ≠ Permission**

A minimal reference implementation of governed agentic execution:

`CAPABILITY → SCOPE → PROPOSAL → AUTHORIZATION → CONTROLLED EXECUTION → VALIDATION → EVIDENCE`

## Runtime contract

- The agent may be capable of proposing an action without being authorized to perform it.
- Authorization is decided at a deterministic governance boundary, not by the model.
- A denied request returns `403 AUTHORIZATION_DENIED` before a protected state change.
- A denial is a successful enforcement event and produces evidence.
- A successful outcome is independently validated before it can emit `OUTCOME_VERIFIED`.
- The agent cannot grant itself permission or declare its own success.

## Canonical flow

```text
Agent
  ↓
Proposal
  ↓
JIREH Authorization
  ├── DENY → 403 → Evidence
  └── ADMIT
       ↓
     AST-01
       ↓
 Controlled Execution
       ↓
   Validation
       ↓
 OUTCOME_VERIFIED
       ↓
 Billing Event
```

## Evidence semantics

`REQUESTED ≠ AUTHORIZED ≠ EXECUTED ≠ COMMITTED`

For outcome settlement:

`VALIDATED SUCCESS → OUTCOME_VERIFIED → BILLING EVENT`

## Prototype scope

This directory is intentionally small. It establishes the governance contract and leaves application-specific policy, authentication, tool adapters, persistence, and production security hardening to later layers.

## Security boundary

Catching a `403` is **not** the enforcement mechanism. The protected executor must consult the deterministic authorization decision before applying a state-changing operation. The runtime handler exists to stop the current path and record the denial.

## Status

Experimental reference implementation. Not a production security boundary and not a claim of universal protection against agent failures or prompt injection.
