# Governable Agency

## Architectural Term Establishment

**Status:** Proposed architectural term established independently in the KAIROSEED repository.

**Term:** Governable Agency

### Definition

**Governable Agency** is an architectural property in which an agent retains autonomy over reasoning, proposal generation, and bounded action selection—including novel actions—while consequential execution remains constrained by an explicitly authorized autonomy envelope that is observable, auditable, and revocable.

### Core distinction

Governable Agency does not require every possible action to be pre-written. Instead, governance authorizes the conditions and boundaries within which the agent may exercise discretion.

Therefore:

- Reasoning may remain autonomous.
- Proposals may be novel.
- Novel actions may be executable when covered by the authorized autonomy envelope.
- Novelty does not create authority.
- Authorization remains action-, scope-, condition-, and validity-bound.
- Runtime revocation remains available.
- Actual effects require verification.
- Evidence is preserved.

### Governing invariant

> **The agent may exercise agency within an authorized autonomy envelope; it may not silently expand the authority that defines that envelope.**

### Agency boundary

```text
Capability
    ↓
Authority
    ↓
Authorization Envelope
    ↓
Autonomous Reasoning
    ↓
Novel Proposal / Action Selection
    ↓
Bounded Execution
    ↓
Observation
    ↓
Verification
    ↓
Evidence

                 ↘ REVOCATION ↗
```

### Emergency and recovery behavior

An unresolved incident may produce a novel recovery proposal. ASTRA may execute that proposal autonomously only when the proposal satisfies the currently valid autonomy envelope. If it does not, execution is blocked or escalated.

A pre-validated fallback is therefore not the only possible autonomous path. The governance boundary can authorize a **bounded class of recovery behavior**, while preserving runtime revocation.

### First-class revocation

Revocation is a deployment primitive, not merely an emergency afterthought. It may invalidate authorization, terminate an execution lease, withdraw delegated authority, quarantine a capability, or force execution into a governed safe state.

### Non-equivalence rules

- Capability ≠ Permission
- Permission ≠ Authorization
- Instruction ≠ Authority
- Reasoning ≠ Authorization
- Authorization ≠ Execution
- Execution ≠ Success
- Success ≠ Verification
- Novelty ≠ Authority
- Autonomy ≠ Irrevocability

### Design principle

> **Autonomy of reasoning. Agency of action. Governance of authority. Revocation of autonomy. Verification of effect.**

### Terminology note

“Governable Agency” is used here as a KAIROSEED architectural term. It should not be represented as an established standards-body term unless independently demonstrated by authoritative sources.

### Evidence boundary

This document establishes the term and its intended architectural meaning in this repository. It does **not** by itself establish empirical safety, production readiness, universal applicability, or compliance with any external standard.

**Capability must be explicit. Authority must justify action. Execution must remain bounded. Effects must be verified.**
