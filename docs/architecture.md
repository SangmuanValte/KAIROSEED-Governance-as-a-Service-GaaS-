# GaaS Architecture

## Purpose

GaaS provides an autonomous research capability operating inside an independently governed authority boundary.

## Control flow

```text
Persistent Objective
        ↓
Plan / Decompose
        ↓
Action Proposal
        ↓
Independent Authorization
        ↓
Controlled Execution
        ↓
Observe Result
        ↓
Evidence + Provenance
        ↓
Update State / Replan
        ↓
Continue or Stop
```

## Authority boundary

Authority is an explicit envelope over identity, action, resource, scope, and time. Capability does not grant permission.

```text
CAN ≠ MAY
```

An authorization decision should be independently attributable and should produce an auditable record.

## Assurance properties

1. **Bounded** — actions are constrained by explicit policy.
2. **Independent** — the capability layer cannot authorize itself.
3. **Observable** — proposals, authorizations, executions, outcomes, and failures are recorded.
4. **Reconstructible** — a reviewer can reconstruct the relevant decision and execution chain.
5. **Revocable** — authority can be withdrawn without changing the agent's underlying capability.

## Verification target

The first implementation should prove the control boundary before maximizing autonomy.

Minimum evidence for a governed action:

- objective identifier
- action proposal
- policy/authority decision
- authorization identity
- execution event
- result/outcome
- provenance
- timestamp
- final disposition

## Research question

Can autonomous capability and operational independence increase while the authority envelope remains explicitly bounded, independently authorized, observable, and reconstructible?
