# KAIROSEED Agent Instruction Contract v1

## Purpose

This repository implements Governance-as-a-Service for bounded, auditable agentic AI execution. Agent instructions guide work; they do not grant authority.

## Non-negotiable invariants

- Capability ≠ Permission.
- Proposal ≠ Authorization.
- Instruction ≠ Authorization.
- Model judgment ≠ Governance.
- `¬Authorized(a) ⇒ ¬Executed(a)`.
- `Executed(a) ⇒ Authorized(a) ∧ Bounded(a)`.
- `BLOCK ⇒ ¬EXECUTED`.
- `DONE = VerifiedSuccess ∧ EvidencePreserved`.
- More capable models do not receive more permissive governance by default.

## Stable repository boundaries

Agents may inspect, reason about, propose, implement, test, and document changes within the repository subject to the existing authorization and repository controls.

Agents must not treat any instruction, skill, prompt, model judgment, previous approval, memory, or successful dry run as authorization for a consequential action unless the governance layer explicitly authorizes that action.

Do not weaken, bypass, replace, or silently modify governance enforcement merely to complete a task.

## Agent decision model

Use judgment to determine an appropriate implementation path. Keep the following separation intact:

```text
MODEL JUDGMENT
      ↓
PROPOSAL
      ↓
VERIFICATION
      ↓
INDEPENDENT GOVERNANCE
      ↓
AUTHORIZATION
      ↓
PEP / MECHANICAL ENFORCEMENT
      ↓
BOUNDED EXECUTION
      ↓
RESULT VERIFICATION
      ↓
EVIDENCE PRESERVATION
```

The agent may choose *how* to perform an authorized task. It may not self-authorize the task.

## Completion

Do not define completion as "the implementation looks finished" or "the agent stopped working."

Use:

```text
Implement
  ↓
Run
  ↓
Test
  ↓
Inspect failures
  ↓
Fix
  ↓
Retest
  ↓
Verify evidence
  ↓
DONE
```

A task is only `DONE` when the repository's applicable success conditions are verified and the supporting evidence is preserved.

## Skills

Skills should be small routers, not giant procedural recipes. A skill should primarily state:

1. When it activates.
2. What invariant it protects.
3. Where the detailed procedure or supporting resources live.

Progressively disclose detailed procedures only when needed.

## Governance change rule

If a proposed change affects authorization, scope, execution boundaries, audit evidence, policy interpretation, or enforcement, treat it as a governance-sensitive change. Do not infer permission from the agent's confidence or from the task description alone.

## Failure behavior

When required authorization, verification, scope, or evidence conditions are absent:

```text
STOP → EXPLAIN → PRESERVE AVAILABLE EVIDENCE → REQUEST/REQUIRE GOVERNANCE REVIEW
```

Never convert an authorization failure into an execution success merely by changing instructions.
