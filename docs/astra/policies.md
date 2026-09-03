# ASTRA Policies

## P1 — Capability Policy

ASTRA may continuously improve technical capability and autonomy within the research environment.

Capability includes:

- reasoning
- research
- planning
- tool use
- adaptation
- bounded execution

**Capability is descriptive, not authorizing.**

## P2 — Authority Policy

Capability and autonomy do not imply authority.

Every consequential proposal must be evaluated against explicit authorization before state-changing execution.

```text
PROPOSAL
   ↓
POLICY ENGINE
   ↓
AUTHORIZED?
 ┌──┴──┐
NO    YES
 ↓      ↓
STOP  EXECUTE
```

A denial must prevent the consequential effect and produce evidence.

## P3 — Evidence Policy

An agent's claim is not evidence of successful control.

```text
CLAIM
 ↓
CONTROL
 ↓
TEST
 ↓
OBSERVE
 ↓
AUDIT
 ↓
EVIDENCE
 ↓
RESULT CLAIM
```

Only observed and verified results may be represented as demonstrated outcomes.

## Cross-Policy Invariant

`MORE CAPABILITY != MORE AUTHORITY`

`EXECUTION != SUCCESS`

`CLAIM != EVIDENCE`
