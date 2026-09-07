# KAIROSEED Agentic Failure Observatory

Observation-first tooling for monitoring public RSS/open-data signals about agentic AI failures and emerging technology.

## Boundary

```text
PUBLIC DATA -> INGEST -> NORMALIZE -> MODEL PROPOSAL -> KAIROSEED VERIFY -> EVIDENCE
```

The system is deliberately **non-agentic at the execution boundary**. It observes and classifies public information; it does not autonomously execute external actions.

## Governance model

The MVP implements:

`Gravity = Authority × Action × Time × Consequence × Evidence`

Each vector is explicit and independently inspectable. Evidence requires both a cryptographic proof reference and a raw telemetry/log reference before the evidence vector becomes `1.0`.

### Important interpretation

A zero gravity score does **not** mean an incident did not happen. It can mean that authority or evidence is unverified, or that consequence is classified as zero. The observatory therefore keeps `verification_status` separate from `gravity_index`.

## Model boundary

Hugging Face models are treated as **classification proposal generators**, not authorities. Multiple models can be evaluated against the same corpus. Their outputs should be retained with model IDs and confidence values so that disagreement and drift can be measured.

Suggested failure taxonomy:

- `UNAUTHORIZED_ACTION`
- `SCOPE_EXPANSION`
- `TOOL_MISUSE`
- `PRIVILEGE_ESCALATION`
- `GOAL_PATH_CONFUSION`
- `INSTRUCTION_CONFLICT`
- `DELEGATION_FAILURE`
- `MISSING_HUMAN_APPROVAL`
- `VERIFICATION_FAILURE`
- `AUDIT_EVIDENCE_FAILURE`
- `RUNTIME_CONTAINMENT_FAILURE`
- `FALSE_BELIEF_OR_HALLUCINATION`

## Run locally

```bash
python -m pytest
```

The RSS parser uses Python's standard library and does not execute article links. A production deployment should add feed allowlists, rate limits, content-size limits, retries, provenance storage, and immutable evidence retention.
