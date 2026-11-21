# KAIROSEED — Independent Testing Protocol

**Document ID:** KRS-DEF-003  
**Version:** 0.1  
**Status:** PROPOSED — protocol specification only; not implemented, exercised, independently reviewed, or authorized for production  
**Research domain:** AI-assisted defensive cybersecurity  
**Related specifications:** KRS-DEF-001 — Defensive AI Security Assessment and Independent Verification; KRS-DEF-002 — Vulnerability Evidence Record Schema  
**Branch:** `research/defensive-ai-security-krs-def-003`

> **AI may assist with search. Independent verification must establish correctness.**
>
> **The evidence differs. The independence requirement remains.**

## 1. Purpose

This document proposes a controlled protocol for evaluating candidate software weaknesses and proposed corrections through author-controlled testing and independent evaluation.

It defines:
- roles and separation of responsibilities;
- the minimum independence disclosures for Level B evaluation;
- test selection and environment separation;
- handling of deterministic and randomized tests;
- kill conditions and stop decisions;
- preservation of failures, contradictions, and inconclusive outcomes;
- evidence required for assurance-status decisions.

The protocol is intended for controlled software samples, synthetic cases, and systems for which explicit written authorization exists. It does not authorize testing third-party systems, production systems, or systems outside the stated scope. Test execution must remain within a bounded, approved environment.

This document specifies a research process. It does not claim that the process has been implemented, validated, or shown to improve security outcomes.

## 2. Governing principles

1. **The proposer is not the independent checker.** The person or system proposing a weakness or patch cannot independently certify that same claim.
2. **A second run is not automatically independent.** Repeating an author's procedure may confirm repeatability, but does not by itself establish independent test design or assessment.
3. **Different identities do not guarantee independence.** Different people, models, machines, or organizations may still share decisive assumptions, tools, credentials, test data, or control.
4. **Independence is evidenced, not asserted.** The evaluator must disclose relevant dependencies and explain which parts of the evaluation were independently selected and controlled.
5. **Failures are first-class evidence.** A failed or contradictory result must not be deleted, hidden, averaged away, or overwritten by a later pass.
6. **Authorization precedes execution.** No test begins without a valid scope, accountable owner, and permitted test conditions.
7. **Assurance claims are bounded.** A result applies only to the exact artifact, configuration, property, and conditions recorded.
8. **Level C is not an automatic reward for Level B.** Formal verification is a distinct evidence path requiring a defined formal property and checked proof artifact.
9. **No result grants release authority.** Testing and verification evidence do not themselves authorize deployment or other consequential action.

## 3. Scope and non-goals

### 3.1 In scope

- author-controlled tests on a candidate correction;
- independent review and testing in a separate, authorized environment;
- test selection and execution records;
- deterministic and randomized test reproducibility;
- kill-condition evaluation;
- assurance-status decisions and evidence preservation;
- bounded coordination with formal verification.

### 3.2 Out of scope

- testing systems without explicit authorization;
- production penetration testing or operational security actions;
- instructions for exploiting real systems;
- claims that a test suite proves a system is secure;
- claims that independence eliminates all evaluator error;
- automatic patch approval, merge, deployment, or release;
- treating an AI-generated score or summary as an assurance decision.

## 4. Roles and separation of responsibilities

The following roles are logical responsibilities. One individual may hold multiple roles only where the combination does not compromise the required independence of a decision. Any role combination and its limitations must be disclosed.

| Role | Responsibility | Must not claim |
|---|---|---|
| Proposer | Submits candidate weakness or correction proposal | Independent confirmation of own proposal |
| Author test operator | Runs and records Level A tests | Independent Level B result |
| Independent evaluator | Selects or materially adapts tests and evaluates the exact candidate artifact | Independence without disclosure of dependencies |
| Evidence custodian | Preserves records, artifacts, versions, and access history | Truth of the underlying technical claim merely from custody |
| Formal verifier | Checks a bounded formal property and proof artifact | Properties outside the declared model and proof boundary |
| Human decision authority | Makes explicit decisions on progression and release | Technical proof beyond the evidence reviewed |

AI systems may assist any role with permitted analysis, documentation, or test-design support. AI output is advisory. An AI system must not be the sole authority for independence determinations, assurance decisions, or release authorization.

## 5. Independence model for Level B

### 5.1 Independence dimensions

The evaluator must declare the degree of separation across the following dimensions:

| Dimension | Question to answer | Evidence to record |
|---|---|---|
| Personnel | Is the evaluator separate from the proposer and patch author? | Roles, relationships, conflicts, prior involvement |
| Test design | Did the evaluator independently select or materially adapt tests? | Test-plan origin, selection rationale, author-provided test overlap |
| Assumptions | Were key assumptions challenged independently? | Assumption register and evaluator comments |
| Environment | Was the evaluation environment separately prepared or controlled? | Environment manifest and digest |
| Tooling | Were tools or configurations independently selected or checked? | Tool versions, configurations, shared tooling disclosures |
| Data and seeds | Were test inputs and random seeds independently controlled or selected? | Input provenance, seed policy, overlap disclosure |
| Credentials and control | Did the evaluator operate under distinct access and control boundaries? | Access-control description and audit evidence |
| Decision | Was the result assessed without the proposer controlling the decision? | Reviewer identity, decision record, conflict statement |

### 5.2 Independence classification

The evaluator must classify each dimension as one of:

- `SEPARATE` — materially independent for the stated evaluation;
- `SHARED_DISCLOSED` — shared dependency exists and is documented;
- `NOT_INDEPENDENT` — the dimension is not independent;
- `UNKNOWN` — evidence is insufficient to determine independence;
- `NOT_APPLICABLE` — the dimension does not apply, with rationale.

A Level B claim must not be made when a material dependency is unknown or when a conflict undermines the evaluator's ability to reach an independent judgment. Shared dependencies do not automatically invalidate every evaluation, but their effect must be assessed and stated.

### 5.3 Minimum Level B conditions

Before an evaluation can be labeled Level B, the record must show:

1. the evaluator is not the proposer or patch author for the artifact under review;
2. conflicts and prior involvement are disclosed;
3. the evaluator has authority to report a failure without approval from the proposer;
4. the evaluator independently selects or materially adapts at least part of the test plan;
5. the exact source revision, patch identity, and environment are recorded;
6. results and artifacts are preserved under evaluator accountability;
7. shared tools, data, assumptions, credentials, and control boundaries are disclosed;
8. a reviewer assesses whether the disclosed dependencies materially undermine independence.

A separate machine or model alone does not satisfy these conditions.

## 6. Test planning and selection

### 6.1 Test-plan record

Each evaluation must have a versioned test plan containing:

- evaluation ID and target record ID;
- exact source revision and patch digest;
- authorized scope and stop conditions;
- property or behavior being examined;
- test categories and selection rationale;
- expected safe behavior;
- acceptance and kill conditions;
- environment and tooling requirements;
- time and resource limits;
- randomization and seed policy, if applicable;
- known exclusions and anticipated blind spots;
- evaluator identity and independence declaration.

### 6.2 Independent test selection

The independent evaluator should derive tests from the stated property, relevant requirements, and an independent review of the change. The evaluator may inspect author tests, but must record which tests were reused, adapted, supplemented, or excluded.

The evaluation should not be limited to demonstrating that the author's expected scenario passes. It should consider whether:
- the original reported behavior remains present;
- nearby boundary conditions violate the same property;
- the correction changes required behavior;
- the patch introduces regressions within the authorized test scope;
- assumptions about inputs, state, dependencies, and execution order are justified.

These are test-design considerations, not instructions to target external systems.

### 6.3 Test-plan freeze

Before execution, the evaluator records a plan version and its digest. Changes after execution begins require a new plan version or a documented amendment. Results from different plan versions must remain distinguishable.

A frozen plan supports auditability; it does not prove the plan is complete or technically adequate.

## 7. Environment separation and artifact identity

The evaluator must identify the exact artifact tested.

Required records include:
- source repository and immutable revision;
- patch or build artifact digest;
- dependency lockfile or relevant dependency manifest;
- operating system and architecture;
- compiler, interpreter, runtime, and tool versions;
- build configuration;
- test harness version;
- environment manifest digest;
- deviations from the planned environment.

A separately prepared environment is preferred. Where a shared image, runner, cache, or infrastructure is used, record the shared elements and explain why they do or do not affect independence.

If the tested artifact differs from the artifact proposed for review, the result must not be transferred silently. The difference must be reconciled and the applicable tests rerun.

## 8. Deterministic and randomized tests

### 8.1 Deterministic tests

For deterministic tests, record:
- exact test inputs;
- procedure and harness versions;
- execution command or secure reference;
- environment identity;
- expected result;
- observed result;
- run count and timestamps.

Repeated deterministic results under the same conditions support repeatability only within those conditions.

### 8.2 Randomized tests

Where randomness is used, record:
- pseudorandom generator or randomness source;
- generator and tool versions;
- seed or seed-generation method;
- number of trials;
- test input-generation configuration;
- resource and time limits;
- failing seed and minimized reproducer, if safely available;
- whether the evaluator independently selected seeds or input-generation parameters.

Do not disclose secrets or sensitive entropy material. A public reproducibility seed should be used only when safe and appropriate. If a seed cannot be retained, record why and state the resulting reproducibility limitation.

A finite number of randomized trials does not establish that untested cases are safe. Passing trials must not be reported as exhaustive proof.

### 8.3 Reproduction of failures

When a failure occurs:
1. preserve the original failing run and its artifacts;
2. record the exact artifact and environment identity;
3. attempt a bounded reproduction within the approved scope;
4. retain the original seed and input where safe;
5. record any minimized or transformed reproducer as a separate linked artifact;
6. do not replace the original failure record with the minimized case.

If a failure cannot be reproduced later, retain both outcomes and explain the discrepancy.

## 9. Kill conditions and stop decisions

### 9.1 Purpose

A kill condition is a predeclared observation or event that requires the current claim, patch, test run, or progression decision to stop or be reconsidered.

Kill conditions must be defined before the relevant test whenever reasonably possible. A newly discovered failure condition may be added later, but must be timestamped and linked to the observation that motivated it.

### 9.2 Kill-condition categories

| Category | Example condition | Required response |
|---|---|---|
| Scope violation | Execution would exceed approved scope | Stop execution; preserve the event |
| Authorization failure | Authorization is absent, expired, or ambiguous | Do not begin or continue the test |
| Original behavior persists | The reported unsafe behavior remains observable | Mark correction as failed for that property |
| New counterexample | An evaluator finds another input or state violating the declared property | Preserve evidence; block a passing claim pending review |
| Regression | Required behavior fails after the correction | Record regression; block correction acceptance |
| Artifact mismatch | Tested source or patch differs from the declared artifact | Mark run invalid for the intended claim; reconcile identity |
| Evidence integrity issue | Required artifact is missing, altered, or cannot be authenticated against its record | Mark evidence obstructed or inconclusive |
| Resource boundary | Test reaches an approved time, resource, or safety limit | Stop according to the plan; preserve partial result |
| Trace incompleteness | Required event coverage is missing | Do not claim a complete trace |
| Independence conflict | Undisclosed or material dependency undermines evaluator independence | Withhold Level B status; escalate for review |

### 9.3 Stop semantics

A kill condition does not always mean the entire research project is terminated. It means the affected run or claim cannot proceed as if the condition had not occurred.

The response must identify:
- what was stopped;
- who or what initiated the stop;
- the triggering observation;
- the time and artifact references;
- whether the stop was successfully enforced;
- what review is required before any restart.

Restart requires a new or amended plan, documented authorization where applicable, and preserved linkage to the stopped run. A restart must not erase the original obstruction.

### 9.4 No silent override

A proposer or AI assistant may not silently waive a kill condition. Any authorized disposition must be made by an accountable human reviewer, with rationale and evidence. A scope or authorization violation cannot be retroactively legitimized by a successful technical result.

## 10. Failure, contradiction, and inconclusive-result preservation

Every run must produce a record, including runs that do not complete.

Required outcome categories include:
- `PASS_WITHIN_DECLARED_TESTS`
- `FAIL`
- `COUNTEREXAMPLE_FOUND`
- `BLOCKED`
- `INCONCLUSIVE`
- `INVALID_RUN`
- `STOPPED_BY_KILL_CONDITION)

These labels describe test outcomes, not global security states.

Rules:
1. Never delete a failed result because a later run passes.
2. Never average a critical failure into an aggregate score that hides it.
3. Preserve contradictory results and investigate differences in artifact, environment, procedure, and randomness.
4. Do not convert missing evidence into a pass.
5. Do not treat a blocked or invalid run as a successful test.
6. Link corrections and retests to prior records; preserve the history.
7. Record whether a failure is unresolved, explained, corrected, or superseded by a new artifact.

A correction may be proposed after a failure, but the revised patch receives a new identity and must be evaluated as a new artifact.

## 11. Assurance levels and transitions

### 11.1 Level A — TESTED

Permitted claim:

> The identified artifact passed the specified author-controlled tests under the recorded conditions.

Minimum evidence:
- exact source and patch identity;
- author test plan and version;
- environment and tool manifest;
- complete run records;
- expected and observed behavior;
- all failures, blocked runs, and deviations;
- accountable author-test review.

Level A does not establish independence or universal correctness.

### 11.2 Level B — INDEPENDENTLY TESTED

Permitted claim:

> The identified artifact was evaluated by a separately accountable evaluator using independently selected or materially adapted tests, within the declared scope and recorded conditions.

Minimum evidence:
- all relevant Level A artifact-identity information;
- evaluator independence declaration across Section 5 dimensions;
- conflict and shared-dependency assessment;
- independently derived test-plan elements;
- separate or disclosed environment controls;
- complete results, including negative and inconclusive outcomes;
- evidence review by an accountable decision-maker.

Level B does not establish formal proof or prove that all vulnerabilities have been eliminated.

### 11.3 Level C — FORMALLY VERIFIED BOUNDED PROPERTY

Level C is a distinct formal-evidence path, not an automatic next stage after Level B.

Permitted claim:

> The specified property was established for the declared model and assumptions, and the proof artifact was checked using the recorded verification process.

Minimum evidence:
- formal property and specification;
- assumptions, preconditions, and environmental model;
- explicit implementation boundary;
- proof artifact;
- proof-checker and toolchain identity;
- independent proof-checking result;
- review of correspondence between the specification and implementation;
- limitations and excluded properties.

Level C applies only to the stated property and proof boundary. It does not imply that the complete software system, deployment environment, or operational process is secure.

### 11.4 Transition rules

- Level A may be recorded only after the author-controlled test evidence is reviewed.
- Level B may be recorded only after the independence conditions and independent evaluation evidence are reviewed.
- Level C may be recorded only for a bounded property with a checked proof artifact and reviewed correspondence.
- A Level B failure blocks a claim that the tested correction passed independent evaluation for the affected property.
- A Level C proof failure, missing proof artifact, or unresolved correspondence gap blocks the Level C claim.
- A later pass does not erase an earlier failure; the final record must show the complete history.
- None of these levels grants production or release authorization.

## 12. Decision authority and separation from release

The evaluator reports evidence and a bounded conclusion. A separate accountable human authority decides whether the evidence is sufficient for the next research stage.

The decision record must state:
- decision-maker and role;
- exact artifact and evidence reviewed;
- scope of the decision;
- decision and rationale;
- unresolved risks and dissenting findings;
- any conditions or restrictions;
- date and record references.

Testing, independent evaluation, and formal verification must not be conflated with approval to merge, deploy, or operate. Release authorization is a separate decision governed by its own policy and evidence requirements.

## 13. Required record linkage to KRS-DEF-002

Each evaluation should link to the evidence record using stable identifiers and versions.

At minimum, the linked records should identify:
- candidate weakness record;
- source revision;
- patch proposal and patch digest;
- evidence record and version;
- test plan and version;
- environment manifest;
- each execution attempt;
- each artifact and digest;
- evaluator declaration;
- review and assurance decision;
- related kill conditions and obstructions.

A record that cannot be linked to the exact artifact tested must not support an assurance claim for a different artifact.

## 14. Proposed evaluation measures

A future controlled study may assess the protocol using measures such as:

- proportion of evaluations with complete artifact identity;
- proportion of test plans with disclosed provenance;
- number and type of independent counterexamples;
- evaluator agreement and disagreement;
- reproducibility of recorded outcomes;
- frequency of scope or authorization violations;
- proportion of failures preserved and correctly linked;
- rate of artifact mismatch;
- time and effort required for independent review;
- frequency of assurance claims corrected after review.

Metrics must be interpreted with their denominators, definitions, sample sizes, and limitations. A higher pass rate is not, by itself, evidence of a better security process.

## 15. Falsification and protocol challenge criteria

The proposed protocol should be challenged and may be rejected or revised if controlled evaluation shows that:

1. evaluators labeled independent share undisclosed dependencies that materially determine outcomes;
2. independent test selection does not produce meaningful scrutiny beyond author-controlled tests;
3. the protocol permits failures to be hidden, overwritten, or misclassified;
4. artifact identity cannot be reliably tied to the evaluated result;
5. kill conditions do not stop progression when their trigger is observed;
6. authorization boundaries cannot be checked before execution;
7. Level A, B, and C claims remain ambiguous or are routinely conflated;
8. the documentation burden makes evidence less reliable or less usable without a justified benefit;
9. reviewers cannot reconstruct why a decision was made from the retained records.

Negative and inconclusive results must be reported. The protocol is not successful merely because it produces a pass.

## 16. Open questions for independent review

The following issues remain open and must not be treated as settled by this draft:

- What minimum personnel separation is practical for a small independent research project?
- Which shared tools or infrastructure materially undermine independence in different evaluation contexts?
- How should evaluator independence be assessed where the project has only one maintainer?
- What evidence is sufficient to establish environment separation?
- How should flaky or nondeterministic failures be classified without discarding them?
- What level of test-plan disclosure preserves auditability without exposing sensitive information?
- Which decision authority should resolve disagreements between evaluators?
- How should the protocol handle a valid finding that cannot safely be reproduced outside a protected environment?

These questions require review and may result in schema or protocol changes.

## 17. Current status and non-claims

**Status: PROPOSED.**

At this stage:
- the protocol has not been implemented;
- no independent evaluator has exercised it;
- no controlled experiment has measured its effectiveness;
- no independence classification has been independently validated;
- no test result or vulnerability is established by this document;
- no Level A, Level B, or Level C assurance is granted;
- no production or release authorization is granted.

## 18. Relationship to companion specifications

- **KRS-DEF-001** defines the proposed defensive workflow and assurance distinctions.
- **KRS-DEF-002** defines the proposed vulnerability evidence record and artifact manifest.
- **KRS-DEF-003** proposes how independent evaluation, test selection, kill conditions, and failure preservation should be documented.
- **KRS-DEF-004** should define the formal verification boundary and the limits of Level C claims.

KRS-DEF-003 does not replace KRS-DEF-002's evidence record. It specifies how evaluation evidence should be generated, assessed, and linked. It also does not establish formal correctness; that boundary belongs to KRS-DEF-004.

## 19. Governing method

**Build privately. Challenge rigorously. Verify independently. Release responsibly.**

**Claim ≤ Evidence ≤ Established Scope.**

**Capability ≠ Permission.**

**AI may assist with search. Independent verification must establish correctness.**

Soli Deo Gloria.
