# KAIROSEED August Pipeline Prototype v0.2 — State Lineage

Status: prototype / evidence-generating, not production assurance.

## Purpose

Advance the August 2026 governed agent pipeline from stage-only events to explicit state lineage:

`CAPABILITY ≠ PERMISSION ≠ AUTHORIZATION ≠ EXECUTION ≠ VERIFICATION`

Pipeline:

`INGEST → INTERPRET → PROPOSE → AUTHORIZE → EXECUTE → VERIFY → EVIDENCE`

## Explicit lineage

Each run carries a traceable chain:

`proposal_id → interpretation_id → authorization_id → execution_id → verification_id → evidence_id`

The core executable invariant is:

> **No execution exists without a traceable authorization.**

An unauthorized proposal receives an authorization decision and is halted before execution. Its verification state is `NOT_RUN` because no execution occurred.

## August project inputs represented

- OpenAI Developers / API integration
- Manus → GitHub → GitHub Actions → GitHub Pages / deployment flow
- WebMCP / agent-native web exploration
- KAIROSEED governance and evidence controls
- Research connectors / sources discussed for healthcare and public-data workflows

These are represented as pipeline inputs for testing, not as claims that every integration was implemented during August.

## Credential boundary

The OpenAI API key is an authentication credential. It is not itself a governance permission or authorization token. The prototype does not place API secrets in evidence, logs, proposal objects, or source code.

## Safety boundary

This prototype uses deterministic local policy checks and simulated bounded execution. It does not make external production changes, publish secrets, or claim security certification.

The SHA-256 value is an evidence integrity digest. It is **not by itself an immutable ledger**; true immutability requires an append-only or otherwise tamper-resistant persistence layer.

## Verification boundary

Verification is modeled as a distinct stage after execution. PTZ-CORE spectral/Laplacian checks are intentionally treated as future verification plugins rather than silently claimed as implemented in this prototype.

## Expected result

The prototype should:

1. accept a task proposal;
2. assign explicit lineage identifiers;
3. classify risk and required authority;
4. deny execution when authorization is absent or invalid;
5. execute only bounded, authorized simulations;
6. verify only executions that actually occurred;
7. preserve an auditable event chain and integrity digest.
