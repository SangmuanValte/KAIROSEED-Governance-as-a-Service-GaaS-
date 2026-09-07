# ASTRA Autonomy Law

## Status

Research hypothesis / control specification. This document does not claim empirical validation.

## Law

> Agentic capability and autonomy may increase without automatically increasing authority. Consequential authority remains bounded by explicit authorization.

Formally:

`Authority <= Explicitly Authorized Boundary`

The target control hypothesis is:

`Capability ↑ + Autonomy ↑ + Governance Constraints = Invariant`

## Core Separation

`Capability != Authorization != Execution != Verification != Commit`

An agent may possess a technical capability without possessing permission to exercise it against a protected state.

## Required Gate

```text
REQUEST
  ↓
SCOPE
  ↓
PROPOSAL
  ↓
AUTHORITY / POLICY
  ├── DENY → STOP → EVIDENCE
  └── ALLOW → CONTROLLED EXECUTION → VALIDATION → EVIDENCE
```

## Falsification Condition

The hypothesis is weakened or falsified if an agent can increase capability or autonomy and thereby obtain a consequential effect outside its explicitly authorized boundary.

## Evidence Rule

No test → no observation → no evidence → no verified result → no security/control claim.
