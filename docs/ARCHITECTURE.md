# KAIROSEED Governance Architecture

![KAIROSEED governance chain](images/governance-chain.png)

> **Core invariant:** Capability != Permission.

## Governance chain

```
CAPABILITY -> AUTHORITY -> CHOICE -> SAFE? -> EXECUTE -> EVIDENCE -> ACCOUNTABILITY
   Can it?     May it?      Should it?   Safe?      Act        Bounds?       Responsible?
```

### 1. Capability — Can it?

The reference core can observe state through the observation/truth path and construct an ActionProposal.

Capability is not permission.

### 2. Authority — May it?

AuthorizationEvidence and the PolicyEnforcementPoint establish the authorization boundary.

The PEP requires external authorization evidence and checks authorization binding conditions such as issuer, audience, decision binding, validity, and replay protection.

A missing or replayed authorization is a **BLOCK** condition.

### 3. Choice — Should it?

KAIROSEEDGovernance.govern() evaluates the versioned PolicyRegistry and produces a structured PASS, WARN, or BLOCK.

A WARN is audited and is not mapped into an executable directive in the tested reference behavior.

### 4. Safe? — Is it safe under these conditions?

The post-authorization runtime layer evaluates runtime viability.

The reference tests cover observation integrity and freshness, verified versus unverified context, youth-safety complexity constraints, and CONTINUE/THROTTLE runtime responses.

**Boundary:** JIREH is post-authorization. It does not create permission when authorization is absent.

### 5. Execute — Act

The reference governance core deliberately does **not** implement a production execution layer.

This is an architectural boundary, not evidence that arbitrary production execution is already governed.

A production deployment must place the enforcement boundary at the actual consequential tool/deployment operation.

### 6. Evidence — Did it stay within bounds?

The reference implementation records governance and authorization outcomes in an audit ledger.

Tested behavior includes PASS and BLOCK audit outcomes, audit-write failure causing fail-closed behavior, replay attempts producing a BLOCK, and no mapping after governance WARN/BLOCK.

Durability, tamper resistance, independent retention, and production audit infrastructure remain separate evidence requirements.

### 7. Accountability — Who is responsible?

Authorization and audit records bind accountability-relevant fields such as issuer, grant_id, observation_id, policy version, authorization decision binding, and provenance/context.

These fields support traceability; their presence is not by itself proof of a complete production provenance system.

## Deployment gates

For a real deployment, the governance chain must connect to independent infrastructure controls.

```
[1] INTEGRITY / SIGNATURE
          |
          v
[2] TRUSTED IDENTITY
          |
          v
[3] KAIROSEED AUTHORIZATION
          |
          v
[4] RUNTIME / ADMISSION CONTROL
          |
          v
       DEPLOY
```

### Gate 1 — Integrity

The reference tests require verified observation integrity. An unverified integrity condition produces BLOCK.

This should not be described as a cryptographic signature verifier unless the deployment actually verifies a cryptographic signature or equivalent attestation.

### Gate 2 — Trusted identity

The governance path requires verified context and trusted authorization provenance under the tested policy model.

Production identity controls must be independently verified.

### Gate 3 — KAIROSEED authorization

The PEP requires external AuthorizationEvidence.

Relevant tested failure modes include missing authorization, invalid authorization binding, replayed or missing nonce, and audit failure.

Only valid, non-replayed authorization can proceed to the post-authorization runtime layer.

### Gate 4 — Runtime/admission control

KAIROSEED runtime assessment can return BLOCK or THROTTLE for unsafe runtime state.

If Kubernetes admission tooling such as Kyverno is used, it is a **separate deployment control**. Kyverno is not implemented by the Python reference core itself and must be independently verified in the target cluster.

## Fail-closed rule

```
required gate missing / invalid / unverifiable
                |
                v
             BLOCK
                |
                v
       record governance evidence
```

The tested reference behavior includes fail-closed handling for malformed or unverifiable context, failed audit writes, missing authorization, replay, disallowed mappings, and unsafe policy/runtime conditions.

## Evidence boundary

This document describes architecture and tested behavior. It does **not** certify production readiness.

Issue #10 defines the release invariant:

```
RELEASE_ALLOWED
  <=> CI_GREEN
   && SECURITY_INVARIANTS
   && DURABLE_EVIDENCE
   && CONCURRENCY_SAFE
   && FAILURE_SAFE
   && DEPLOYMENT_CONTROLS
   && PROVENANCE
```

The governance diagram does not, by itself, establish those predicates.

In particular, documentation and a diagram do not establish current-head CI success, independent clean-checkout reproduction, durable evidence retention, concurrency safety, complete chaos/resilience coverage, current-head artifact provenance, production environment protection/review/rollback controls, or production certification.

Therefore **Issue #10 remains an evidence tracker until those gates are independently evidenced**.

## Epistemic rule

```
Implementation behavior != formal proof != production certification != universal security guarantee
```

A passing test establishes behavior under the tested conditions. It does not establish a universal invariant outside those conditions.

If an artifact cannot be accessed or reproduced, its status is **UNVERIFIED / INDETERMINATE**, not automatically FAIL.

> **Unknown != False.**

> **Artifact accessibility is a verification precondition, not a correctness conclusion.**

## Reference test mapping

The current reference test suite provides implementation-level evidence for several parts of this architecture, including audited PASS and allowlisted mapping; immutable observation payloads; fail-closed context validation; youth-safety boundary behavior; stale/unverified observation blocking; structured WARN without mapping; frozen/versioned policy registry behavior; audit-failure fail-closed behavior; disallowed mapping blocking; external authorization requirement; replay blocking; and post-authorization JIREH behavior.

The suite should be treated as **implementation-level verification evidence under its stated test conditions**, not as evidence for every predicate in Issue #10.

## Core doctrine

**Capability is not permission.**

**More capability requires more explicit governance.**

**Define -> Enforce -> Falsify -> Evidence.**

## Governed Autonomy

**Governed Autonomy** is the architectural principle that an AI system may expand its capability and autonomy without automatically expanding its authority to take consequential action.

### Canonical chain

```
AI Capability
    → Agentic Capability
    → Consequential Action
    → Authorization
    → Execution
    → Verification
    → Evidence
```

### Core invariant

```
Capability ↑  does not imply  Authority ↑
```

Autonomous operation therefore remains inside an explicit governance boundary. Consequential execution must be attributable to an authorization decision and produce inspectable evidence.

### Execution boundary

```
        AI / AGENT
            │
       Capability
            ↓
        Proposal
            ↓
       Governance
            ↓
      Authorization
            │
       ┌────┴────┐
       │         │
     DENY       ALLOW
       │         │
      BLOCK      ↓
              EXECUTE
                 │
                 ↓
             VERIFY
                 │
                 ↓
              EVIDENCE
```

### Evidence status

Governed Autonomy is a **KAIROSEED architectural principle/proposal**. It is not presented as a universal theorem, formal proof, production certification, or security guarantee.

> **Governed Autonomy:** autonomy is permitted to operate within an explicit authorization and enforcement boundary; increased capability does not constitute increased authority, and consequential execution must remain attributable to an authorization decision and produce inspectable evidence.

**Capability ≠ Permission.**  
**Autonomy ≠ Authority.**  
**Execution ≠ Evidence.**  
**Evidence ≠ Authorization.**
