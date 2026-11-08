# KAIROSEED — Governance-as-a-Service (GaaS)

**Human-centered AI innovation with verifiable governance.**

KAIROSEED is an experimental, verification-first governance framework for AI-assisted systems, developed by **Sangmuan Valte**. This repository focuses on a **Governance-as-a-Service (GaaS) reference adapter** for defining, enforcing, and evaluating delegated authority for AI agents through executable policies, authorization boundaries, runtime controls, and auditable evidence.

> **Embrace intelligence. Preserve human authority. Build responsibly. Verify what you claim.**

> **Repository boundary:** This is a reference implementation and research workspace, **not proof of a production security deployment**.


## Verification status vocabulary

**Dated: 2026-11-09**

Use the following four statuses when recording the verification state of a component, interface, seam, or security requirement. Record the status against a defined claim, scope, and evidence set; do not use a status as a substitute for those details.

| Status | Definition | Minimum basis |
|---|---|---|
| **NOT VERIFIED** | Available evidence does not establish whether the requirement is satisfied. | No sufficient verification evidence. This includes an interface with no named owner or no documented seam contract. |
| **VERIFIED** | The specified requirement passed its defined acceptance tests within the recorded scope and assumptions. | Reproducible test results and inspectable evidence. This does not imply universal security. |
| **FAILED** | Evidence demonstrates that the specified requirement was violated. | An observed counterexample or failed acceptance criterion, with supporting evidence. |
| **BLOCKED** | Verification or acceptance cannot proceed because a required prerequisite is unavailable or unmet. | A named blocking prerequisite and its effect on the verification activity. |

**Inventory rule:** A seam with no named owner is recorded as **NOT VERIFIED**, with owner **UNASSIGNED** and evidence **NONE**. Missing ownership or missing evidence is not, by itself, proof that the seam is technically broken and must not automatically be recorded as **FAILED** or assigned an unsupported risk rating.

**Status discipline:** **NOT VERIFIED** means the claim remains unestablished; **FAILED** means a violation has been observed; **BLOCKED** means a required step cannot proceed. Do not collapse these states. Record exclusions separately as **OUT OF SCOPE**; this is a scope designation, not a fifth verification status.


## Start a bounded task

Use [WORKING_CONTEXT.md](WORKING_CONTEXT.md) for a small starting context covering code, documentation, preparation, memory, and releases. The [context-to-release workflow](docs/workflow/context-to-release.md) includes reproducible packaging and a short session handoff. Its documentation prerelease does not establish application or production readiness.

## Vision

AI offers students, graduates, researchers, and builders opportunities to learn practical skills, create useful tools, and improve productivity. KAIROSEED encourages adapting to technological change while taking risks of errors, misuse, displacement, and loss of control seriously.

The goal is not to replace legitimate human judgment with model output. It is to investigate systems in which probabilistic agents can **propose** actions without independently granting themselves **permission** to execute consequential actions.

## Core principles

1. **Human agency:** Legitimate authority and accountability remain with people and authorized institutions.
2. **Capability is not permission:** Access to an API, tool, or model capability is not authorization to use it.
3. **Fail-closed governance:** Missing, expired, invalid, or unverifiable mandatory authorization must block protected actions.
4. **Bounded execution:** Authorized operations remain within approved resources, conditions, and time windows.
5. **Independent verification:** An agent's success statement cannot substitute for checking the actual protected state.
6. **Evidence preservation:** Keep reproducible records of decisions, observations, failures, and limitations.
7. **Honest claims:** State only what observed evidence supports within the established testing scope.

## Decision pipeline

```text
Validate
   ↓
Filter (admissibility)
   ↓
δ-Pareto Frontier
   ↓
Scalar Preference
   ↓
Independent Authorization
```

- **Validate:** Assess candidate inputs, provenance, evidence, and constraints.
- **Filter:** Remove candidates that violate non-negotiable admissibility requirements.
- **δ-Pareto frontier:** Consider trade-offs under declared objectives, tolerances, and precisely specified comparison semantics. Tolerance-based dominance may be non-transitive; implementations must define cycle and empty-frontier handling.
- **Scalar preference:** Choose among admissible candidates using an explicitly declared preference function.
- **Independent authorization:** Separately check identity, authority, resource scope, policy, expiry, and relevant conditions before execution.

**Invariants:** Optimization cannot override admissibility. Preference cannot create authority.

## Canonical governed execution

```text
Probabilistic agent / PROPOSE
           ↓
Capability / CAN
           ↓
GOVANA / MAY (independent authorization)
           ↓
JIREH / ENFORCE (runtime boundaries)
           ↓
Bounded transition / S₀ → S₁
           ↓
Independent verifier
           ↓
Evidence preservation
           ↓
DONE (verified finality)
```

The intended fail-closed property for a defined protected resource and threat model is:

```text
NOT Authorized(action) ⇒ No protected state change caused by that action
```

This is a **testable design requirement**, not an established universal guarantee. It depends on explicit assumptions about the protected state, adversary capabilities, enforcement completeness, and observer independence.

A proposed finality rule is:

```text
DONE =
  Authorized Transition
  AND Bounded Execution
  AND Independent Verification
  AND Evidence Preserved
```

## Verification-first execution adapter

This repository's reference adapter makes the path from agent capability to consequential action explicit:

```text
Agent → Adapter → Policy / Authorization → Execution Gate
      → Tool → Verification → Evidence
```

The minimal reference sequence is:

```text
Capability → Authorization → Enforcement → Execution → Verification → Evidence
```

### Repository artifacts

- `src/kairoseed.ts` — TypeScript reference adapter.
- `docs/ADAPTER.md` — adapter contracts and production-boundary notes.
- `docs/EVIDENCE.md` — evidence schema and independent-observer procedure.
- `docs/THREAT_MODEL.md` — adversarial execution-boundary cases.
- `GaaS-Safety-Framework/Foundation/` — prior Agent Circumvention Test and WebMCP prototype materials.

These paths describe repository materials; their presence alone does not establish that tests passed.

### 20-second conceptual demo

```text
ACTIVE claim
    ↓
authorized action / permitted execution
    ↓
revoke claim
    ↓
same proposed action
    ↓
deny / protected execution blocked
    ↓
verify actual state and inspect preserved evidence
```

**Evaluation question:** Does revocation prevent consequential state changes when checked independently, including the specified edge cases?

## Evidence standard

> **Claim ≤ Evidence ≤ Established Scope**

For every meaningful security or safety assertion, record:

- Precisely defined property, assumptions, scope, and acceptance criteria.
- Repository revision, dependency and runtime versions, and environment.
- Tests **actually run**, observed results, and timestamps.
- Independent observation of protected state and authorization decisions.
- Negative results, unresolved risks, untested cases, and limitations.

Use **PASS** only for demonstrated properties within the tested scope; **WARN** for incomplete or inconclusive evidence; and **BLOCK** when a critical requirement is violated. Inaccessible evidence is **UNVERIFIED**, not automatically FAIL.

> **Unknown ≠ False.** A planned test is not an executed test.

### Example evidence collection for a deployment-backed implementation

Where the indicated database tables and credentials are available and collecting these records is authorized:

```bash
mkdir -p evidence

psql "$DB_URL" -c "
SELECT * FROM governance_events
ORDER BY created_at DESC LIMIT 100;
" > evidence/governance_events.txt

psql "$DB_URL" -c "
SELECT * FROM authorization_decisions
ORDER BY created_at DESC LIMIT 100;
" > evidence/authorization_decisions.txt

psql "$DB_URL" -c "
SELECT * FROM executions
ORDER BY created_at DESC LIMIT 100;
" > evidence/executions.txt
```

If a suitable authorized health/invariant endpoint exists:

```bash
curl -s "$HEALTH_URL" | jq > evidence/invariants_snapshot.json
```

Avoid committing credentials, personal information, or confidential logs to public repositories. Evidence collection commands are **examples**, not proof they have run successfully.

## Safety-case research direction

KAIROSEED can express scoped assurance arguments as **claim → supporting reasoning → observations → independent review → authorized decision**. A safety case is not itself proof of secure operation.

**Next falsifiable milestone:** In a local, isolated test harness, check whether an untrusted agent can modify a harmless, defined protected resource when an independent authorization evaluator denies the request. Test expiry, replay, resource scope, and evidence integrity only in the authorized environment; retain both successes and failures.

## Production boundary

The in-memory stores and adapter are research/reference components. Production use would require separately implemented and verified controls appropriate to its threat model, including:

- Authoritative, durable policy and authorization state.
- Concurrency safety and single-use authorization handling.
- Replay prevention and identity/resource/scope binding.
- Policy-version checks, expiry enforcement, and execution isolation.
- Tamper-evident evidence storage and independent verification.
- Operational incident review and documented response procedures.

**None of these requirements is claimed to be universally sufficient or already verified in production.**

## Responsible experimentation

Conduct cybersecurity evaluations only against environments you own or have explicit permission to test. Prefer isolated test fixtures and harmless protected resources. Establish scope and stopping conditions beforehand, and preserve evidence without exposing secrets.

## Project status

**Research / experimental reference adapter.** This README specifies intended architecture and verification practices. It does not assert a successful independent audit, complete safety case, or production-grade enforcement. Implementation outcomes must be established using linked revisions, reproducible tests, and independent observations.

---

**Project:** KAIROSEED · Governance-as-a-Service (GaaS)  
**Author:** Sangmuan Valte  
**Guiding principle:** **Proposal ≠ Permission ≠ Verified Success.**
