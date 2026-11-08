# KAIROSEED — Small Working Context

**Purpose:** use this page to resume one bounded task in code, documentation, preparation, memory, or release. This is a working aid outside the frozen canonical specification.

## Foundation

“Kairoseed is my seed; God waters it; I plant.”

Start from [Created Time and Appointed Arrival](docs/foundations/created-time-and-appointed-arrival.md), under **KAIROSEED Master Data Pack v1.1 — frozen conceptual baseline**. Faith grounds purpose; inspected evidence supports technical claims. This context does not reproduce or verify the complete Master Data Pack.

## Non-negotiable distinctions

- Interpretation ≠ Authorization ≠ Execution.
- Capability ≠ Permission; Completion ≠ Verified Success.
- Claim ≤ Evidence ≤ Established Scope.
- Memory can inform a task; it cannot grant permission.
- A test run, formal proof, implementation review, and independent reproduction establish different things.

## Load only what this task needs

| Work | Start here | Check before claiming success |
| --- | --- | --- |
| Code | `src/kairoseed.ts`, `docs/ADAPTER.md`; or the chosen prototype directory | Exact revision, relevant contracts, actual tests and effects |
| Documentation | Foundation above and `docs/EVIDENCE.md` | Claim, supporting source, limits, intended reader |
| Preparation | [Workflow](docs/workflow/context-to-release.md) | Scope, destination, risks, acceptance criteria, rollback |
| Memory | [Session handoff](docs/workflow/session-handoff-template.md) | Evidence references, freshness, uncertainty, next action |
| Release | `release/context-release.json` and its named release notes | Exact contents, checksums, permission, published result |

Repository paths are navigation aids, not proof that their implementations work. Inspect relevant files at the task's commit; do not load the entire project by default.

## One-task loop

Define the outcome → inspect sources → implement the smallest change → run relevant checks → review claims and scope → release the permitted artifact → inspect the delivered result → record a short handoff.

Keep the canonical baseline frozen. Record proposed improvements separately. A documentation release does not authorize production operation.

## Resume prompt

> Read WORKING_CONTEXT.md and the latest relevant handoff. My outcome is [one sentence]. Work in [paths/repository]. The allowed action and destination are [scope]. Success means [observable result]. Inspect current artifacts, make the smallest useful change, test it, and report what actually happened with evidence. Ask only for information that blocks the next consequential step.

**Current release scope:** foundation documentation and a local packaging workflow. Independent review: **NOT ASSESSED**. Runtime containment and production readiness are not evaluated by this workflow.
