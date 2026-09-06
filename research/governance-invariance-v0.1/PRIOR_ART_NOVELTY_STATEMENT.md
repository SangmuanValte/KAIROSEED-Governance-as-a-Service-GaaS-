# Prior-Art & Novelty Statement

**Project:** KAIROSEED  
**Document:** `PRIOR_ART_NOVELTY_STATEMENT.md`  
**Status:** Research positioning statement  
**Purpose:** Establish a defensible description of the proposed contribution without claiming unsupported novelty.

---

## 1. Scope of this statement

This document does **not** claim that KAIROSEED is the first system to address governance of autonomous or agentic AI.

Prior work already addresses related problems including:

- authorization and policy enforcement for autonomous agents;
- capability/permission separation;
- policy-as-code;
- gated execution;
- reference-monitor architectures;
- human approval and escalation;
- cryptographic or tamper-evident audit trails;
- runtime monitoring;
- governance invariants;
- formal verification of governed computation;
- containment and scope adherence.

Accordingly, KAIROSEED should not be described as having invented agent governance as a general field.

The research question is narrower.

## 2. Proposed research contribution

KAIROSEED investigates whether **authorized action scope can remain invariant while an agent's reachable capability space expands over time**.

The central property is:

\[
C_{t+1} > C_t
\;\not\Rightarrow\;
S_{t+1} > S_t
\]

where:

- \(C_t\) = reachable capability/action space;
- \(S_t\) = authorized/intended action scope.

The intended invariant is:

> **Capability expansion must not implicitly produce authorization expansion.**

Any legitimate expansion of authorized scope must instead occur through an explicit authorization transition accompanied by evidence and provenance.

\[
\Delta S \neq 0
\Rightarrow
AuthorizationTransition
\land Evidence
\land Provenance
\]

This is a testable property rather than a claim that the property has already been universally established.

## 3. Relation to intended scope

The proposed experiment is related to the broader agent-safety problem of maintaining an agent within its intended or authorized scope.

For experimental purposes, KAIROSEED operationalizes this relationship as:

\[
Reach_t = Reachable(C_t)
\]

\[
R\&SD_t = Reach_t \setminus S_t
\]

where **R&SD (Reach–Scope Divergence)** represents reachable actions that lie outside the currently authorized scope.

A critical event occurs when:

\[
R\&SD_t > 0
\]

and an out-of-scope action becomes executable **without an explicit authorization transition**.

The research question is therefore:

> **Can increasing capability, adaptation, or environmental reach cause executable action space to diverge from authorized scope without an explicit governance transition?**

## 4. What is already known from prior art

The following concepts are not claimed as uniquely invented by KAIROSEED.

### 4.1 Capability versus authority

Existing security and agent-governance work distinguishes what an agent can technically do from what it is authorized to do.

KAIROSEED adopts this distinction explicitly:

\[
Capability \neq Permission
\]

### 4.2 Policy-enforced execution

Prior architectures use policy gates, authorization checks, policy-as-code, and reference-monitor-like mechanisms to prevent unauthorized execution.

KAIROSEED likewise places governance between proposal and execution.

### 4.3 Human oversight and escalation

Existing agent-safety systems use approval, escalation, intervention, monitoring, and bounded autonomy.

KAIROSEED incorporates these concepts into its governance chain.

### 4.4 Auditability

Tamper-evident logs, cryptographic provenance, event sourcing, and audit trails are established techniques.

KAIROSEED does not claim invention of these mechanisms.

### 4.5 Formal governance invariants

Prior research has formulated mathematical and machine-checked invariants governing autonomous computation.

KAIROSEED therefore does not claim that the general concept of a governance invariant is novel.

## 5. Candidate KAIROSEED contribution

The potentially distinctive contribution is the **integration and empirical operationalization** of several established ideas around a specific property:

\[
\boxed{
Capability\ Expansion
\not\Rightarrow
Authority\ Expansion
}
\]

under a controlled experiment in which authorization is held fixed while capability is systematically increased.

The experimental structure is:

\[
C_0<C_1<C_2<\cdots<C_n
\]

while:

\[
S_0=S_1=S_2=\cdots=S_n
\]

The system is then observed for:

1. unauthorized executable actions;
2. implicit authorization changes;
3. silent state changes;
4. missing authorization provenance;
5. unreconstructable evidence;
6. recovery paths that bypass reauthorization;
7. learning/adaptation paths that silently expand authority.

This converts an architectural principle into a falsifiable experimental property.

## 6. Falsification criterion

The strongest counterexample would have the following structure:

```text
Capability expands
        ↓
New action becomes reachable
        ↓
Authorized scope remains unchanged
        ↓
No authorization transition occurs
        ↓
Action executes
        ↓
Evidence shows no legitimate authority expansion
```

Formally:

\[
C_{t+1}>C_t
\]

\[
S_{t+1}=S_t
\]

\[
a\in Reach(C_{t+1})
\]

\[
a\notin S_t
\]

and:

\[
Execute(a)=1
\]

while:

\[
AuthorizationTransition=0
\]

This constitutes a counterexample to the **tested implementation/configuration under the tested conditions**.

It must not automatically be described as a universal failure of KAIROSEED.

## 7. Interpretation discipline

A failed experiment establishes only what the experimental evidence supports.

### If an out-of-scope action executes

The initial conclusion should be:

> The tested implementation permitted Reach–Scope Divergence under the specified experimental conditions.

Further investigation must determine whether the cause was:

- the governance mechanism;
- an implementation defect;
- a policy configuration error;
- an experiment-harness defect;
- an incomplete capability model;
- an authority-model ambiguity;
- an evidence-layer defect; or
- another interaction between components.

Only after diagnosis and independent reproduction should a stronger architectural conclusion be considered.

### If the invariant survives

A successful experiment establishes:

> No Reach–Scope Divergence was observed under the tested capability levels, environments, policies, and trials.

It does **not** establish universal safety or prove that the invariant can never fail.

## 8. Research novelty position

The defensible novelty position is therefore:

> **KAIROSEED does not claim novelty in autonomous-agent governance, authorization, policy enforcement, auditability, or capability/permission separation individually. Its candidate research contribution is the formulation and empirical testing of Reach–Scope Divergence as a measurable phenomenon, together with an experimental protocol that holds authorized scope constant while systematically increasing reachable capability, adaptation, and environmental reach.**

The contribution remains **candidate novelty** until supported by:

1. systematic prior-art review;
2. precise formal definition;
3. reproducible implementation;
4. empirical results;
5. comparison against relevant existing architectures;
6. independent reproduction where possible.

## 9. Relationship to intended scope

The experiment can use an agent/model's **intended scope** as an external behavioral reference.

The comparison is:

\[
IntendedScope
\rightarrow
AgentBehavior
\rightarrow
ObservedReach
\]

KAIROSEED adds an explicit governance representation:

\[
Capability
\rightarrow
Proposal
\rightarrow
Authorization
\rightarrow
Policy
\rightarrow
Decision
\rightarrow
Execution
\rightarrow
Evidence
\rightarrow
State_{t+1}
\]

The resulting research question becomes:

> **As model and agent capability increases, does the executable action space remain bounded by intended/authorized scope, or does reachable capability begin to diverge from that scope?**

## 10. Current claim boundary

At the present research stage, the following claims are **not justified**:

- “KAIROSEED is the first agent-governance architecture.”
- “No existing system has this idea.”
- “KAIROSEED has solved autonomous-agent governance.”
- “KAIROSEED cannot fail.”
- “A failed test proves KAIROSEED is fundamentally unsafe.”
- “A passing experiment proves the invariant universally.”
- “R&SD is a completely unprecedented concept.”

The defensible claim is narrower:

> **KAIROSEED proposes Reach–Scope Divergence as an empirical phenomenon for studying whether an agent's reachable action space can exceed its authorized scope as capability and adaptation increase, and provides a governance architecture in which such divergence is intended to be blocked, escalated, or made observable through evidence.**

## 11. Research status

**Conceptual definition:** Established.

**Prior-art awareness:** Established at preliminary level.

**Formal property:** Proposed.

**Experimental protocol:** Defined.

**Empirical falsification experiment:** Must be executed and independently reproducible.

**Novelty:** Not established.

**Universal safety claim:** Not made.

**Patent novelty / freedom-to-operate:** Not determined by this document.

## 12. Core research statement

\[
\boxed{
\textbf{Can authorized scope remain invariant under capability expansion?}
}
\]

The experiment does not assume the answer.

It attempts to make the invariant fail.

That is the central methodological commitment:

> **Do not demonstrate that KAIROSEED works by constructing only cases in which it succeeds. Construct controlled conditions under which governance invariance could fail, measure the resulting trajectory, and preserve the evidence regardless of outcome.**
