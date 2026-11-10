# KAIROSEED Five-Seat Authorization Model

**Artifact ID:** KAIROSEED-FIVE-SEAT-MODEL-001  
**Status:** PROPOSED RESEARCH SPECIFICATION  
**Canonical status:** NON-CANONICAL; no canonical invariant is amended  
**Verification status:** NOT VERIFIED  
**O0 disposition:** WITHHELD  
**Production authorization:** NO  
**Deployment authorization:** NO

## 1. Purpose and scope

This document specifies a five-seat separation-of-duties model for the authorization-to-execution lifecycle. It defines role boundaries, prohibited operations, evidence expectations, and formal proof obligations suitable for a future Lean 4 model.

The model is a research specification. It is not an implementation, security certification, proof of runtime isolation, or evidence that any existing KAIROSEED component enforces these boundaries.

The governing meta-rule is:

> If any two seats collapse to one authenticated principal, the separation-of-duties claim is not established.

A diagram, role label, separate software module, or separate API endpoint does not by itself establish distinct principals or independent authority.

## 2. Five seats

### 2.1 Propose

**Responsibility:** Emit a candidate proposal containing at least:
- proposal identifier and content digest;
- target resource and requested operation;
- claimed effect and scope;
- references to claimed supporting evidence.

**Must refuse:**
- writing to the protected store;
- issuing or signing a validation result;
- ratifying or granting authority;
- applying a protected change;
- assigning or asserting its own authenticated role.

**Output authority:** NONE. A proposal is a request for consideration, not permission.

### 2.2 Validate

**Responsibility:** Independently evaluate a proposal against a host-controlled registry, frozen test corpus, and declared validation policy in an isolated validation context.

**Result:** One of PASS, FAIL, or UNRESOLVED, bound to:
- proposal digest;
- corpus and policy identifiers;
- evaluator identity/key identifier;
- result and relevant evidence references.

**Must refuse:**
- validating a proposal under proposer-controlled identity or keys;
- ratifying or issuing a grant;
- applying a protected change;
- altering the frozen corpus or policy as part of the evaluation being judged.

A self-signed or proposer-controlled validation receipt is not accepted as independent validation. PASS is scoped to the stated corpus and assumptions; it is not a universal security claim.

### 2.3 Ratify

**Responsibility:** The sole seat permitted to change the applicable policy or issue a scoped authorization grant.

Before granting, Ratify must inspect the proposal and its validation result, authenticate the relevant principals, and enforce proposer/ratifier separation.

**Must refuse:**
- relying on caller-supplied identity strings as proof of identity;
- ratifying its own proposal where separation is required;
- treating silence, timeout, or missing evidence as consent;
- issuing a grant for a failed, unresolved, stale, mismatched, or out-of-scope validation result.

A grant must bind the proposal digest, target, permitted operation, scope, validity interval or freshness rule, and ratifier identity.

### 2.4 Apply

**Responsibility:** Apply one valid, fresh, scoped grant to its named resource and produce an application receipt.

**Must refuse:**
- direct protected writes without a valid grant;
- stale, revoked, mismatched, replayed, or out-of-scope grants;
- caller-supplied identity in place of authenticated identity;
- bypass paths that do not pass through the authorization boundary;
- validating or ratifying its own action.

The protected-state safety target is:

\[
\neg Authorized(a) \Rightarrow \Delta S_{protected}=0
\]

The model must define what counts as a protected state, an action, a valid grant, and an observable state transition. A refusal response alone does not prove that no mutation occurred.

### 2.5 Audit

**Responsibility:** Act as a read-only witness of the complete chain:
- authenticated proposer identity and proposal digest;
- validator identity/key, corpus, policy, and result;
- ratifier identity and grant;
- application identity, action digest, and receipt;
- independently observed post-state.

**Must refuse:**
- writing or repairing the protected state;
- issuing grants or validation results;
- accepting a self-reported success as proof of the resulting state;
- silently discarding missing, mismatched, or contradictory evidence.

A chain mismatch, missing link, or post-state discrepancy must produce an explicit, recorded failure or unresolved outcome. Audit independence requires evidence access and observation paths that the other seats cannot rewrite or suppress.

## 3. Separation requirements

The five seats must be represented by five distinct authenticated principals and five distinct capability/key spaces. Distinct labels, objects, modules, or processes are insufficient unless the runtime identity and access boundaries are actually enforced.

| Seat | Permitted responsibility | Explicitly prohibited responsibilities |
|---|---|---|
| Propose | Create candidate | Validate, ratify, apply, audit, protected write |
| Validate | Evaluate candidate | Propose as same principal, ratify, apply, protected write |
| Ratify | Change policy; issue scoped grant | Apply, audit, self-validation |
| Apply | Execute valid grant | Propose, validate, ratify, audit |
| Audit | Read and inspect evidence/state | Protected write, validate, ratify, apply |

The implementation must reject role collapse based on authenticated principal identity and capability possession, not caller-controlled role names.

## 4. Lean 4 formalization target

The Lean model should make forbidden operations unrepresentable where practical, using distinct capability types, private constructors, and explicit state-transition functions.

Suggested module decomposition:

```text
Kairoseed/
└── Verification/
    ├── Identity.lean
    ├── Capabilities.lean
    ├── Proposal.lean
    ├── Validation.lean
    ├── Ratification.lean
    ├── Application.lean
    ├── Audit.lean
    └── Theorems.lean
```

The model should define:
- authenticated principal identity and pairwise seat distinction;
- seat-specific capabilities and constructors;
- proposal and validation-result bindings;
- grant scope, freshness, revocation, and resource binding;
- protected state and observable state transitions;
- application receipts and audit observations;
- explicit failure and unresolved outcomes.

### 4.1 Proof obligations

| ID | Obligation | Required property |
|---|---|---|
| P1 | Seat distinction | The five authenticated principals are pairwise distinct under the model assumptions. |
| P2 | Capability separation | No seat capability grants another seat's prohibited operation. |
| P3 | Proposer restriction | Propose cannot validate, ratify, apply, audit, or mutate protected state. |
| P4 | Validation independence | Accepted validation binds to an evaluator distinct from the proposer and to the declared corpus/policy. |
| P5 | Ratification exclusivity | Only Ratify can construct a valid grant; missing or invalid evidence cannot produce one. |
| P6 | Grant freshness and scope | Stale, revoked, replayed, mismatched, or out-of-scope grants cannot authorize application. |
| P7 | Protected-state safety | Without a valid grant, no modeled protected-state transition is possible. |
| P8 | Audit completeness | Missing or mismatched chain evidence and post-state produce detectable failure or unresolved status. |
| P9 | Audit read-only | Audit operations cannot mutate protected state or grant authority. |
| P10 | Non-collapse | If role identities or capability spaces collapse, the separation predicate is false and the acceptance theorem cannot be applied. |

No theorem should assume the desired result in a way that makes the proof circular. Each theorem must state its assumptions explicitly.

## 5. Runtime evidence required beyond Lean

A Lean theorem establishes a mathematical property of the formal model under its assumptions. It does not establish that deployed software, operating-system controls, key custody, or hardware behave according to that model.

A runtime demonstration must separately provide evidence for:

1. Five distinct authenticated principals.
2. Five distinct capability and key spaces, with access controls inspected.
3. Observable refusal tests for each prohibited cross-seat operation.
4. A protected-state before/after observation showing no mutation after unauthorized attempts.
5. Rejection tests for stale, revoked, replayed, mismatched, and out-of-scope grants.
6. Audit detection of deliberately missing or mismatched evidence.
7. Independent inspection of the resulting state and evidence chain.

The test harness, logs, and application receipts must not be the sole source of truth for their own correctness. Independent observation and provenance must be specified for each claim.

## 6. Acceptance gate and disposition

**O0 remains WITHHELD** until the formal model and the required runtime evidence are reviewed against the obligations above.

The following are not interchangeable:
- a diagram and a formal model;
- a formal model and a compiled artifact;
- a compiled artifact and a proved theorem;
- a proved theorem and runtime isolation;
- runtime tests and independent assurance;
- a passing test and production authorization.

### Current disposition

- Research specification: PROPOSED.
- Lean implementation: NOT PROVIDED BY THIS DOCUMENT.
- Lean theorem results: NOT VERIFIED.
- Five-principal runtime demonstration: NOT PROVIDED.
- Independent audit evidence: NOT PROVIDED.
- Production authorization: NO.
- Deployment authorization: NO.
- O0 acceptance: WITHHELD.

## 7. Governing statement

**Five seats must remain five independently authenticated authorities.** Propose requests; Validate evaluates; Ratify grants; Apply executes within the grant; Audit observes and challenges the evidence chain. No seat may silently inherit another seat's authority.

Claim ≤ Evidence ≤ Established Scope.

Soli Deo Gloria.
