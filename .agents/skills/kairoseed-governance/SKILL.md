---
name: kairoseed-governance
description: Use when a task touches KAIROSEED governance, authorization, execution boundaries, verification, audit evidence, or governance-sensitive repository changes.
---

# KAIROSEED Governance Skill

## Activate when

Use this skill for work involving:

- authorization or permission boundaries;
- governance policy or enforcement;
- PEP/runtime execution controls;
- verification or evidence requirements;
- auditability or execution traces;
- changes that could alter the capability/permission boundary.

## Core invariant

```text
¬Authorized(a) ⇒ ¬Executed(a)
```

Supporting invariants:

```text
Capability ≠ Permission
Proposal ≠ Authorization
Instruction ≠ Authorization
Model judgment ≠ Governance
DONE = VerifiedSuccess ∧ EvidencePreserved
```

## Workflow

Keep the root skill lightweight. Route to the repository's detailed governance specifications, tests, schemas, and implementation artifacts as required by the task.

```text
Understand task
    ↓
Identify governance-sensitive boundary
    ↓
Propose change
    ↓
Verify applicable invariants
    ↓
Use independent authorization where execution is consequential
    ↓
Apply bounded change
    ↓
Run relevant tests
    ↓
Inspect failures
    ↓
Preserve evidence
```

## Do not infer authority

A model's confidence, reasoning quality, prior context, skill activation, AGENTS.md instruction, or user-facing description of a desired action does not itself constitute authorization.

## Completion

Report `DONE` only when the applicable success condition has been verified and evidence is preserved. Otherwise report the precise remaining condition as unverified or blocked.

## Detailed resources

Consult repository-specific governance specifications and test artifacts when the task requires implementation detail. Do not duplicate large procedures here.
