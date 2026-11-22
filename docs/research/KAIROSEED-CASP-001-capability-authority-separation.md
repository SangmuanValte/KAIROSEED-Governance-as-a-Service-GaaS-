# KAIROSEED-CASP-001 — Capability–Authority Separation

**Record date:** 2026-11-22  
**Record type:** Research baseline snapshot  
**Record status:** FROZEN AS A DOCUMENTATION SNAPSHOT  
**Research maturity:** Proposed / specified concept  
**Implementation status:** Not established by this record  
**Experimental status:** Not executed by this record  
**Independent verification:** NOT VERIFIED  
**Production authorization:** NO

> This record captures the research position agreed in the 2026-11-22 working session. It is a separate research record, not a modification or replacement of the KAIROSEED Master Data Pack v1.1 or any other canonical baseline.

## 1. Foundational research question

Can we build AI-assisted systems where increasing intelligence and capability never automatically increase authority, and where every consequential action remains attributable, authorized, enforceable, and independently verifiable?

The intended scope is bounded AI-assisted systems whose protected operations, authorization mechanisms, threat models, and evidence paths can be explicitly specified and tested. This record does not claim a universal guarantee for every possible system or environment.

## 2. Foundational principle

**Capability–Authority Separation Principle (CASP-001)**

Greater intelligence can improve proposals without automatically expanding operational privileges.

Let:
- (C_t) denote system capability at time (t).
- (A_t) denote the system's explicitly granted authority at time (t).

The design requirement is:

\[
\Delta C > 0 \;\not\Rightarrow\; \Delta A > 0
\]

A capability change alone is not a valid authorization event. Any authority change must be produced by a separately defined, authenticated, policy-governed authorization process.

## 3. Required properties

1. **Attribution:** Consequential actions can be linked to an authenticated initiating principal, agent identity, and execution context, with stated limits.
2. **Authorization:** Each protected action is checked against explicit, scoped, current permission.
3. **Enforcement:** Unauthorized operations are blocked at the protected execution boundary, not merely discouraged by prompts or detected after the fact.
4. **Accountability:** Relevant decisions, authorization evidence, execution events, and outcomes are recorded with integrity and provenance controls.
5. **Independent verification:** A verifier with sufficiently separate trust boundaries can assess whether the evidence supports the claimed authorization and outcome.

These are requirements to investigate and test, not properties established by this document.

## 4. Proposed architecture and responsibility boundaries

| Layer / component | Proposed responsibility | Important limitation |
| --- | --- | --- |
| Intelligence layer | Models, agents, planning, reasoning, and action proposals | Model output does not grant permission |
| Governance / GOVANA | Evaluate identity, policy, scope, and authorization requests | Must be separated from the untrusted agent |
| Policy enforcement / PEP | Enforce the authorization decision at the protected boundary | Must cover all relevant execution paths |
| Runtime boundary / JIREH | Constrain and observe execution within its defined boundary | Monitoring alone is not enforcement |
| Execution layer | Perform permitted operations on protected resources | Must not accept model assertions as authorization |
| Independent evidence / STRANGER | Assess records, observations, and outcome claims | Independence requires separate trust and control boundaries |

The component names describe the proposed KAIROSEED architecture. This record does not assert that these components are implemented or independently validated.

## 5. Candidate invariants

The following are candidate formal requirements. Their assumptions and exact semantics must be specified before proof or test claims are made.

**I-1 — Capability does not imply authority expansion**

\[
\Delta C \not\Rightarrow \Delta A
\]

**I-2 — Unauthorized protected action is not executed**

\[
\neg P(a) \Rightarrow \neg E(a)
\]

Here, (P(a)) means that action (a) has valid authorization at the enforcement point, and (E(a)) means that the protected operation executes.

**I-3 — Execution is not verification**

\[
E(a) \not\Rightarrow V(a)
\]

**I-4 — Claimed success is not verified success**

\[
\text{Claimed Success} \not\Rightarrow \text{Verified Success}
\]

A formal proof of an invariant is conditional on its model, assumptions, and correspondence to the implementation. Empirical tests provide bounded evidence and do not by themselves prove universal absence of bypasses.

## 6. Initial experimental direction

**Proposed experiment:** Capability expansion under fixed authorization.

### Minimal test environment

- Agent A: baseline-capability agent.
- Agent B: higher-capability agent or controlled capability-upgrade variant.
- Both agents begin with identical, explicitly recorded permissions.
- An external authorization gateway.
- A protected test resource.
- An enforcement mechanism at the resource boundary.
- An evidence collector and a verifier operating across separately defined trust boundaries.

### Procedure

1. Define the protected actions, identities, permission scope, threat model, and expected outcomes before testing.
2. Record the initial permission set for both agents.
3. Increase or vary Agent B's capabilities without changing its authorization.
4. Attempt the same authorized and unauthorized operations with both agents.
5. Record decisions, enforcement outcomes, resource state, errors, and evidence gaps.
6. Independently inspect the evidence and protected resource state.
7. Preserve failures and anomalous results; do not average away boundary violations.

### Expected result

Capability expansion alone must not change the agent's granted permission set or enable a protected operation that the baseline permission set disallows.

This is an experimental expectation, not a result. No experiment is recorded as executed or passed here.

## 7. Threats and unresolved questions

- Direct and indirect privilege escalation.
- Confused-deputy behavior and delegated authority.
- Alternate execution paths and enforcement bypass.
- Credential compromise, theft, replay, and revocation delay.
- Identity attribution across agents, tools, and services.
- Evidence omission, tampering, and incomplete observation.
- Verifier independence and shared infrastructure failures.
- Governance service compromise or unavailability.
- Distributed and multi-agent authorization consistency.
- Physical-world actions, irreversibility, and incomplete observability.
- Formal-model assumptions and implementation correspondence.
- Scalability and operational cost of evidence collection and verification.

These remain open research obligations. Unknown is not a passing result.

## 8. Epistemic and reporting rules

- **UNKNOWN ≠ PASS.**
- Capability ≠ Permission.
- Evidence ≠ Authorization.
- Execution ≠ Verification.
- Completion ≠ Verified Success.
- Agent Proposal ≠ Human Approval.
- No unearned PASS.
- No unsupported claims of proof, implementation, testing, or independent verification.
- State the threat model, assumptions, scope, and limitations alongside every security claim.
- Preserve failures and contradictory evidence.

Use explicit status labels: PROPOSED, SPECIFIED, IMPLEMENTED, EXECUTED, TESTED, INDEPENDENTLY VERIFIED, and NOT VERIFIED. Do not collapse these states.

## 9. Change control

This document freezes the research snapshot as of 2026-11-22. It does not freeze future learning or prohibit evidence-based revisions.

Any subsequent revision should record:
- The exact change and reason.
- The affected requirement or hypothesis.
- Supporting evidence and source revision.
- Test or proof method and result.
- Independent review status.
- Remaining uncertainty and limitations.

Do not silently rewrite this snapshot. Create a new revision or an addendum and preserve the previous record.

## 10. Closing disposition

**Frozen:** The research question, CASP-001 principle, proposed responsibilities, candidate invariants, initial experiment outline, known unknowns, and epistemic rules captured in this document.

**Not established:** Implementation, test execution, formal proof, complete enforcement coverage, independent verification, or production readiness.

**Production authorization: NO.**

**Final principle:**

> Capability may evolve. Authority must remain explicitly governed, independently granted, enforceable, and accountable.

**Claim ≤ Evidence ≤ Established Scope.**
