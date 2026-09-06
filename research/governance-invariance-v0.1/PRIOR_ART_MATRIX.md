# Prior-Art Matrix

**Project:** KAIROSEED  
**Document:** `PRIOR_ART_MATRIX.md`  
**Status:** Research positioning / preliminary prior-art matrix  
**Purpose:** Compare KAIROSEED's proposed property against adjacent prior art without asserting unsupported novelty.

---

## 1. Interpretation rule

This matrix does **not** determine legal patent novelty, freedom-to-operate, or priority of invention.

It is a technical research-positioning artifact.

The comparison asks:

> **What problem does the prior work address, what mechanism does it use, and what—if anything—is materially different about KAIROSEED's proposed empirical property?**

A row marked **Similar** means the underlying idea is substantially represented in prior work.

A row marked **Potential distinction** identifies a combination, formulation, or experimental emphasis that may deserve further investigation.

A distinction is **not automatically novel**.

## 2. Core KAIROSEED proposition

The primary proposition under investigation is:

\[
C_{t+1} > C_t
\;\not\Rightarrow\;
S_{t+1} > S_t
\]

where:

- \(C_t\) = reachable capability/action space;
- \(S_t\) = authorized/intended action scope.

The desired governance invariant is:

\[
\boxed{
Capability\ Expansion
\not\Rightarrow
Authority\ Expansion
}
\]

A critical failure occurs when:

\[
C_{t+1}>C_t
\]

while:

\[
S_{t+1}=S_t
\]

and an action outside \(S_t\) becomes executable without an explicit authorization transition.

# 3. Prior-Art Matrix

| Area / Prior-Art Concept | Existing Contribution | Relationship to KAIROSEED | Similarity | Potential KAIROSEED Distinction |
|---|---|---|---|---|
| **Capability-based security** | Separates available capabilities from broader authority/privilege | Direct conceptual overlap | High | KAIROSEED applies the distinction to adaptive agent trajectories and empirical capability expansion |
| **Reference monitor** | Mediates access to protected operations and enforces authorization | Closely related to the governance gate | High | KAIROSEED explicitly tracks capability expansion, authorization state, temporal state, and evidence across transitions |
| **Policy-as-code** | Represents authorization constraints as executable policy | Directly related to policy gating | High | KAIROSEED treats policy as one component of a larger capability → authority → execution → evidence chain |
| **Least privilege** | Limits an actor to required permissions | Closely related to fixed authorized scope | High | Experiment explicitly holds authority constant while increasing capability |
| **Human-in-the-loop / approval gates** | Requires human approval for selected actions | Similar to escalation/authorization transitions | High | KAIROSEED models authorization transition as an explicit state change with provenance |
| **Agent permission systems** | Restrict tools/actions available to autonomous agents | Direct overlap | High | Proposed experiment separates technical reach from authorized action space and measures divergence |
| **Agent containment** | Restricts autonomous systems from accessing or modifying prohibited resources | Related to scope preservation | High | R&SD attempts to quantify divergence between reachable and authorized action spaces |
| **Runtime monitoring** | Observes agent behavior and detects violations | Directly related to trajectory monitoring | High | KAIROSEED combines observation with explicit governance-state and evidence transitions |
| **Audit logging / provenance** | Records actions and system events for reconstruction/accountability | Direct overlap | High | Evidence is treated as part of the authorization/state-transition invariant |
| **Cryptographic audit trails** | Provides tamper-evident evidence chains | Direct implementation overlap | High | Used as evidence supporting governance transitions rather than merely post-hoc auditing |
| **Governance-first agent architectures** | Place governance/policy between planning and execution | Very close architectural precedent | Very high | KAIROSEED's candidate distinction is the specific capability-expansion / scope-invariance experiment |
| **Formal governance invariants** | Specifies properties that governed systems must preserve | Direct conceptual overlap | Very high | KAIROSEED seeks empirical falsification in an executable agent environment rather than relying only on formal specification |
| **Mechanized governance verification** | Machine-checks governance safety properties | Strong conceptual overlap | High | KAIROSEED emphasizes empirical trajectory measurement and counterexample generation |
| **Scope-adherence evaluations** | Tests whether an AI system stays within intended task/boundary scope | Directly relevant | Very high | KAIROSEED operationalizes scope as an explicit authorization state and compares it against reachable capability space |
| **Long-horizon agent safety** | Studies failures emerging across extended autonomous trajectories | Strong overlap | High | KAIROSEED makes authorization persistence across state transitions an explicit measurement target |
| **Adaptive-agent safety** | Studies changing behavior/capabilities under adaptation or learning | Strong overlap | High | Proposed invariant specifically tests whether adaptation can silently expand authority |
| **Recovery / resilience governance** | Revalidates system behavior after failures or environmental changes | Related | Medium–High | KAIROSEED treats recovery itself as non-authorizing: `RECOVERY ≠ AUTHORIZATION` |
| **State-machine / event-sourced systems** | Represents system behavior as explicit state transitions and events | Strong architectural overlap | High | Applies state-transition reasoning to authorization continuity and agent capability expansion |
| **Economic / organizational delegation** | Models authority delegated to actors under constraints | Conceptually related | Medium–High | KAIROSEED transfers delegation logic into dynamic agentic execution |
| **KAIROSEED R&SD** | Proposed measurement of reachable action space versus authorized scope under capability expansion | Central proposed construct | — | Candidate contribution requiring validation against prior literature |

# 4. Detailed comparison dimensions

## 4.1 Capability versus authority

Prior security research already establishes that:

\[
Capability \neq Authority
\]

Therefore KAIROSEED should **not** claim invention of this distinction.

The candidate contribution is instead to make the relationship dynamic:

\[
C_t \rightarrow C_{t+1}
\]

while testing whether:

\[
S_t = S_{t+1}
\]

remains true.

### Assessment

**Prior art:** Strong.

**KAIROSEED distinction:** Dynamic empirical invariance under capability expansion.

**Novelty status:** Unestablished.

---

## 4.2 Intended scope versus reachable action space

Modern agent safety work increasingly evaluates whether models remain within an intended task or operational boundary.

KAIROSEED proposes making the relationship explicit:

\[
Reach_t = Reachable(C_t)
\]

\[
D_t = Reach_t \setminus S_t
\]

with:

\[
R\&SD_t = |D_t|
\]

or another appropriate divergence metric.

This reframes scope adherence as a relationship between:

> **what the system can reach**

and

> **what the system is authorized to execute.**

### Assessment

**Prior art:** Strong.

**Potential distinction:** Explicit quantitative Reach–Scope Divergence measurement across capability levels.

**Novelty status:** Requires literature comparison and empirical validation.

# 5. Governance invariance under capability expansion

This is the principal research axis.

The experiment holds authorization constant:

\[
S_0=S_1=\ldots=S_n
\]

while increasing capability:

\[
C_0<C_1<\ldots<C_n
\]

Then measure:

\[
X_t \subseteq S_t?
\]

where \(X_t\) represents actually executed actions.

The critical invariant is:

\[
\boxed{
X_t \subseteq S_t
}
\]

for every authorized execution.

A stronger invariant is:

\[
\boxed{
\Delta S \neq 0
\Rightarrow
ExplicitAuthorization
\land Evidence
\land Provenance
}
\]

### Why this matters

A system could satisfy a static permission check while still failing dynamically.

For example:

```text
 t0
 Capability = C0
 Scope      = S0
 Action     = authorized

        ↓ capability expansion

t1
 Capability = C1
 Scope      = S0
 New action = reachable

        ↓

Question:
Does the new capability remain bounded by S0?
```

The experiment deliberately creates this condition.

# 6. Adaptation and learning

A particularly important comparison concerns adaptive agents.

The KAIROSEED invariant is:

\[
Learning \neq Authority\ Escalation
\]

The intended transition is:

\[
Learning
\rightarrow
Adaptation
\rightarrow
New\ Proposal
\rightarrow
Governance\ Gate
\]

not:

\[
Learning
\rightarrow
New\ Authority
\]

This creates a testable failure condition:

\[
Learning_t
\rightarrow
\Delta S
\]

without:

\[
ExplicitAuthorizationTransition
\]

### Assessment

Adaptive-agent safety research already addresses behavioral changes produced by learning, feedback, and adaptation.

The potentially distinctive element is treating **authorization state as an independently conserved variable** during adaptation experiments.

# 7. Temporal dimension

KAIROSEED additionally treats authorization as stateful and temporal.

The question is not simply:

> “Was this action authorized?”

but:

> “Was this action authorized **in this state and at this time**?”

Conceptually:

\[
Authorized(a,t,s)
\]

rather than:

\[
Authorized(a)
\]

This permits experiments involving:

- expired authorization;
- changed environmental state;
- revoked permissions;
- recovery after interruption;
- capability expansion;
- explicit authorization transitions.

### Assessment

Temporal authorization is established prior art.

**Potential distinction:** Integrating temporal validity with capability-expansion invariance and trajectory evidence.

**Novelty status:** Unestablished.

# 8. Evidence and provenance

KAIROSEED treats evidence as part of the governance transition:

\[
Authorization
\rightarrow
Execution
\rightarrow
Evidence
\rightarrow
State_{t+1}
\]

rather than treating logs merely as an after-the-fact record.

The critical property is:

\[
\Delta S \neq 0
\Rightarrow
Evidence + Provenance
\]

This means an authorization transition must be reconstructable.

### Assessment

Tamper-evident logging and provenance are established techniques.

The candidate distinction is their use as a **testable invariant surrounding authorization-state transitions**.

# 9. Candidate experimental contribution

The strongest defensible candidate contribution is therefore not:

> “KAIROSEED invented AI governance.”

Nor:

> “KAIROSEED invented capability versus permission.”

Instead:

> **KAIROSEED proposes an empirical test for governance invariance under capability expansion: hold authorized scope constant, systematically increase reachable capability, observe the resulting action trajectories, and measure whether executable actions diverge from authorized scope without an explicit authorization transition.**

This should be tested against existing governance architectures rather than assumed to be unique.

# 10. Novelty confidence levels

| Claim | Current Confidence |
|---|---|
| Capability ≠ Permission is important | **Established** |
| Agent governance already exists | **Established** |
| Policy-gated agent execution already exists | **Established** |
| Audit/provenance mechanisms already exist | **Established** |
| Scope adherence is an existing safety concern | **Established** |
| Governance invariants already exist | **Established** |
| Capability can increase independently of authority | **Plausible / testable** |
| R&SD is a useful measurement construct | **Proposed / requires validation** |
| R&SD is novel in the literature | **Unknown** |
| KAIROSEED's complete architecture is novel | **Unknown** |
| KAIROSEED is first in agent governance | **Not claimed** |
| KAIROSEED solves governance under capability expansion | **Not established** |

# 11. Required prior-art validation

Before making a formal novelty claim, the research should compare KAIROSEED against at least these categories:

1. capability-based security;
2. reference monitors;
3. policy-as-code;
4. access-control systems;
5. autonomous-agent authorization;
6. agent containment;
7. scope-adherence evaluations;
8. runtime agent monitoring;
9. governance-first agent architectures;
10. formal governance invariants;
11. adaptive-agent safety;
12. long-horizon agent safety;
13. event sourcing and provenance;
14. cryptographic audit systems;
15. delegated authority systems.

The comparison should identify whether each prior system:

- models capability independently from authority;
- permits capability expansion;
- explicitly freezes authorized scope;
- measures scope divergence;
- models authorization as a temporal state;
- records authorization transitions;
- reconstructs action trajectories;
- tests learning-induced authority expansion;
- tests recovery-induced authority continuation;
- attempts to falsify the governance invariant.

# 12. Research claim boundary

Until this matrix is supported by systematic literature review and experiments, the correct terminology is:

**“candidate contribution”**

rather than:

**“novel invention.”**

Likewise:

**“potentially distinctive empirical formulation”**

rather than:

**“first known formulation.”**

And:

**“counterexample to the tested implementation”**

rather than automatically:

**“KAIROSEED failure.”**

# 13. Current status

**Prior-art field:** Established and populated.

**General agent governance:** Not novel as a category.

**Capability/authority separation:** Established.

**Scope adherence:** Established research concern.

**Governance invariance:** Existing conceptual/formal precedent exists.

**R&SD:** Proposed construct.

**Capability-expansion experiment:** Proposed.

**KAIROSEED-specific novelty:** Not yet established.

**Patent/legal novelty:** Not determined.

**Empirical evidence:** Required.

# 14. Research principle

> **The objective is not to prove that KAIROSEED is novel. The objective is to discover exactly where KAIROSEED overlaps existing science, exactly where it differs, and whether those differences survive empirical testing.**
