# META.RUN — Features — ASTRA Boundary

> **Status:** Proposed architecture / feature specification (v0). **Not** an implementation report, test result, security attestation, or deployment authorization.
>
> **Invariants:** Capability ≠ Authority · Execution ≠ Admission · SDK participation ≠ Authority · Proposal ≠ Authorization · Verifier ≠ Authority · Actor ≠ Verifier · Claim ≤ Evidence ≤ Established Scope.
>
> **Scope:** A bounded, auditable API/orchestration prototype for research and controlled execution. ASTRA means a *delegated-policy authorization and enforcement boundary*, not independent authority to grant its own permissions. Legitimate human/operator authority must be established externally.

## 1. Unified API

- Present LLM calls, workflows, and agents through a single `runMetaTask` entrypoint.
- `@openai/agents` supplies orchestration primitives only; it does not confer authorization.
- Confine `Agent`, `run`, `tool`, and `handoffs` integration to `adapters/openai-agents.adapter.ts`.
- All consequential operations must traverse an independently enforced ASTRA/ScopeGateway authorization boundary.

## 2. Compare Models (SCORE)

Evaluate each model **per workload**, recording a vector instead of collapsing performance into one scalar:

```text
f(x) = [quality, latency, tokens/sec, cost, h7]
x ≻_δ y ⇔ (∀i f_i(x) ≥ f_i(y) + δ_i) ∧ (∃j f_j(x) > f_j(y) + δ_j)
F_δ = {x : ∄y ≻_δ x}
```

- Record tokens/sec, wall-clock latency, and total cost of execution (TCE) **per run**.
- **Directionality prerequisite:** The mathematical dominance predicate assumes every dimension is **higher-is-better**. Transform lower-is-better dimensions before applying it (e.g., normalized negative latency and negative cost). Preserve raw measurements in the evidence ledger.
- **Specification detail:** The stated `≻_δ` rule requires at least `δ_i` improvement in **every** dimension, and strict improvement beyond `δ_j` in at least one. This is more restrictive than conventional Pareto dominance; retain it as the user-specified rule unless separately revised.
- `h7` is intentionally **undefined pending a measurable definition**; no implementation should score, rank, or claim that dimension until it is specified.
- Publish workload details, direction/normalization rules, `δ`, sample counts, variation, and model/pricing versions with each frontier.

## 3. Ship First Integration (EXECUTE)

- Proposed workers: `image`, `video`, `voice`, `file`.
- Minimize infrastructure for v0: no Kubernetes cluster or container-image build pipeline required for the prototype; provider APIs, credentials, runtime and an evidence store may still be required.
- State progression: `BOUND → EXECUTE → VERIFY → SCORE → ADMIT`.
- The `ScopeGateway` evaluates `identity`, `scope`, `tool`, `payload`, `recursion`, and `mutation_bounds`, producing `ALLOW` or `DENY` **before** any side effect.
- The trusted Executor must re-check the applicable decision at the protected effect boundary, reject mismatches/stale permits, and log the outcome.
- `agent_can_issue=false`; `self_authorization=DENY`; `Proposal≠Authorization`.
- `EXECUTE` means a specifically permitted bounded task or sandbox operation, not approval to deploy, publish, promote, or mutate unrelated external systems.

## 4. Task History (EVIDENCE)

Every task history entry includes:

```text
task_id, input_files, output_refs, webhook_id
```

The audit bundle includes:

```text
artifacts, hashes, config, command_outputs, test_results, verification_records
```

- Canonicalize JSON per JCS (RFC 8785) before computing SHA-256: `SHA256(JCS(record))`.
- Store a sequence number and previous-record hash if a verifiable append-only hash chain is intended. A collection of independent hashes is **not** itself a chain.
- An integrity hash is not proof of authorship, authorization, freshness, completeness, or independent verification. Those require separate trusted identity/signature, timestamp, access-control, and verification checks.
- Proposed inspection command for a JSONL manifest:

```sh
cat manifest.v1.jsonl | jq -s
```

- Record immutable run configuration, version identifiers, policy decision and provenance, observed effects, and verification disposition. Missing records must not be treated as evidence of success.

## 5. Files and Output References

- Hash input files and deduplicate repeated assets by content, subject to access-control and privacy boundaries.
- Attach output references using bounded schemes: `s3://`, `file://`, `https://`.
- Webhooks carry `output_ref + evidence` after the relevant execution and verification checks.
- Treat references and webhook payloads as untrusted until authenticated and validated; protect against path traversal, unauthorized reads, and cross-tenant asset reuse.
- No agent performs direct mutation. All side effects are issued by the trusted Executor after authorization.

## 6. Pricing Signals and Cost Visibility

```text
TCE = token charges + compute charges + external API charges
```

- Record both raw token counts and applicable versioned input/output token rates; do not multiply a mixed token count by one price if different token classes are billed differently.
- Expose `cost_usd` in **every** `meta-run-evidence` record, including zero or explicitly estimated costs with provenance.
- Keep per-task and per-run pricing visible rather than relying solely on aggregated totals.
- Feed cost-aware measurements into `SCORE` and the workload-specific `F_δ`.

## 7. Repeated Assets, Images, Video, and Voice

- Reuse hash-deduplicated artifacts and prior frontier evidence only when the input, model, version, parameters, policy, verification, price assumptions, and validity window are equivalent and the evidence remains `VALID`.
- One `runMetaTask` abstraction; model selection remains workload-specific using the measurement vector.
- Voice: `STT → LLM → TTS`, with separate evidence and permissions at each stage.
- Video: bounded frame generation/composition; image: bounded generation/editing; file: bounded transformations.
- Apply content, consent, retention, privacy, and output-validation constraints to each worker.

## 8. Governance (ASTRA)

- `Capability != Authority`
- `Execution != Admission`
- `SDK participation != Authority`
- `Verifier != Authority`
- `Actor != Verifier`

```text
DEPLOY_GATE = ALLOW iff independent_verification == VALID
              and all applicable external authorization requirements hold
              else DENY → NO_DEPLOY
```

- `independent_verification == VALID` is **necessary, not sufficient** for deployment. The authorized operator, policy, scope, and environment must also permit deployment.
- Fail closed on missing, invalid, incomplete, stale, or non-attributable evidence.
- The verifier reports evidence validity but cannot confer authority. The actor may propose work but cannot approve itself.
- Promotion and production deployment remain blocked by default; test execution never grants promotion rights.

## 9. Production Prototype (v0 plan; not verified)

Proposed commands once the corresponding files and scripts have been implemented:

```sh
npm run type-check
node --env-file=.env fleet/workers.ts
```

- Target: no Kubernetes, no `image_digest` build, no sandbox image build for v0.
- Allow the prototype to operate in `NO_DEPLOY` mode for permitted local/synthetic task history, pricing, and evaluation; **promotion stays blocked** until the independent verification and deployment authorization gates pass.
- **Current repository compatibility note (2026-11-01):** At the time this specification was pinned, the repository's root `package.json` had no `type-check` script, and the root listing did not show a `fleet/` directory. The commands above are **proposed**, not confirmed runnable. No tests or deploys are claimed.

## Acceptance criteria for a later implementation

1. Every attempted side effect is mediated by a separately trusted ScopeGateway/Executor boundary and is denied without valid delegated authority.
2. Every executed task emits attributable, replayable evidence with explicit verification status; hashes alone do not satisfy attribution.
3. The SCORE engine preserves raw metrics, dimension directionality, costs, uncertainty, and the specified workload-specific dominance rule.
4. Workers do not bypass the boundary via agent handoffs, webhooks, output references, cached assets, or recursion.
5. `NO_DEPLOY` mode can record permitted synthetic/local results while all production admission remains blocked.
6. Independent reviews and relevant tests are recorded **before** any proposal to widen execution or deployment scope.

**Current disposition:** `SPECIFIED / UNVERIFIED / NO_DEPLOY`. Pinning this document is a documentation change only; it does not establish functioning workers, pricing data, test success, independent verification, or production permission.
