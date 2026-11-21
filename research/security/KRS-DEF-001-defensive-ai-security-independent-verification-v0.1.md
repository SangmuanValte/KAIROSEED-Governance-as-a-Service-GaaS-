# KAIROSEED — Defensive AI Security Assessment and Independent Verification

**Document ID:** KRS-DEF-001  
**Version:** 0.1  
**Status:** PROPOSED — not implemented, tested, independently verified, or authorized for production  
**Research domain:** AI-assisted defensive cybersecurity  
**Related methodology:** Principle of Independence  
**Branch:** `research/defensive-ai-security-krs-def-001`

> **AI can search. Independent verification must establish.**

## 1. Purpose and scope

This specification proposes a defensive workflow for investigating software weaknesses and evaluating corrections with explicit separation between discovery, evidence, testing, formal verification, and release authorization.

The initial research scope is limited to controlled software samples, synthetic test cases, public vulnerability records, and systems for which explicit authorization exists. It does not authorize testing third-party systems, production deployment, or use of restricted capabilities.

This document is an independent KAIROSEED research artifact. It does not claim affiliation, endorsement, access, or integration with OpenAI Daybreak Blue or Daybreak Red.

## 2. Principle of Independence

AI may:
- search source code and propose candidate weaknesses;
- generate hypotheses and reproduction plans;
- propose patches and kill conditions;
- assist with test design and evidence organization.

AI-generated claims do not establish vulnerability, patch correctness, independent verification, or release authorization.

The correctness of a finding or correction must remain independently inspectable and must not depend solely on the system that proposed it.

### Foundational invariants

1. Capability ≠ Permission.
2. Evidence ≠ Authorization.
3. Completion ≠ Verified Success.
4. AI Proposal ≠ Human Approval.
5. Reproduction ≠ General Proof.
6. Independent Testing ≠ Formal Verification.
7. Formal Verification ≠ Automatic Production Authorization.

## 3. Stage I — Candidate weakness discovery

**Output status:** PROPOSED

AI-assisted discovery may use static analysis, source-code review, taint analysis, controlled fuzzing, dependency analysis, pattern matching, and human-supplied hypotheses.

Every candidate must use a structured record:

| Field | Requirement |
|---|---|
| Weakness ID | Stable identifier, e.g. DEF-001 |
| Repository | Owner/repository and authorized scope |
| Location | File, function, line range |
| Source identity | Commit hash |
| Class | Candidate CWE or other taxonomy, if applicable |
| Hypothesis | Specific input or condition and expected unsafe behavior |
| Expected behavior | Defined safe behavior |
| Candidate behavior | Suspected behavior, not yet established |
| Discovery method | Tool, analysis method, or human report |
| Confidence | PROPOSED; confidence is not proof |
| Provenance | Model/tool/version and operator, where available |

A candidate is not an established vulnerability merely because an AI assigns it a high confidence score.

**Gate G1 — Candidate acceptance:** A human reviewer confirms that the candidate is sufficiently specified and within the authorized assessment scope. Acceptance permits investigation; it does not establish exploitability.

## 4. Stage II — Reproducible evidence

**Output status:** OBSERVED / REPRODUCED, only when supported

An evidence package should contain:

- Minimal reproducing input or test case, where safe and applicable.
- Cryptographic hash of the input and relevant artifacts.
- Source commit hash.
- Operating system and environment details.
- Compiler/interpreter, dependency versions, and build flags.
- Execution command and trace.
- Expected safe behavior and observed behavior.
- Reproduction script and instructions.
- Tool versions, timestamps, and known limitations.

A second environment should be able to reconstruct the relevant conditions and examine the reported behavior.

A failed reproduction is preserved as an obstruction. It may indicate an incorrect hypothesis, environmental differences, missing dependencies, non-determinism, or incomplete instructions. It is not automatically proof that the candidate is false.

**Gate G2 — Evidence acceptance:** Evidence is accepted for further evaluation only when its provenance, scope, and reproduction conditions are sufficiently complete.

A cryptographic hash supports artifact identity and integrity relative to a recorded digest. A hash does not prove that the artifact's contents are true.

## 5. Stage III — Correction proposal

**Output status:** PROPOSED

An AI-generated correction is a proposal, not a proof.

Each patch package should include:

- Patch ID and source commit.
- Proposed diff and patch hash.
- Technical rationale.
- Intended security property.
- Scope: what changes and what does not.
- Expected behavior after correction.
- Regression risks and known limitations.
- Kill condition: a test or observation that would show the correction is incomplete or harmful.

Examples of kill conditions include:
- the original unsafe behavior remains reproducible;
- an independent test identifies another violating input;
- a regression test fails;
- the correction breaks a required behavior;
- the patch introduces a new security weakness.

AI must not approve, merge, or release its own patch. A responsible human reviewer must authorize progression to testing.

**Gate G3 — Human review:** The patch, rationale, scope, and kill condition are reviewed before author-controlled tests begin.

## 6. Stage IV — Three distinct assurance levels

### Level A — Tested correction

**Permitted claim:** The patch passed the specified author-controlled tests.

Evidence may include unit tests, regression tests, build records, test configuration, and bounded fuzzing results.

Interpretation: no failure was found within the tested conditions. This does not prove that all relevant failures have been eliminated.

### Level B — Independently tested correction

**Permitted claim:** An independent evaluator examined the patch using independently selected tests and a separately prepared environment.

Evidence should include:
- evaluator identity and declared independence;
- separately designed test cases;
- test tools and versions;
- independent environment/build record;
- source commit and patch identity;
- results, reproduction records, and all discovered failures.

Independence is substantive, not nominal. A different model name or agent is not sufficient if evaluators share the same credentials, test suite, assumptions, data, or control boundary without disclosure.

If Level A passes and Level B fails, the correction must not retain an independently tested status. The failure and obstruction are preserved.

### Level C — Independently verified bounded property

**Permitted claim:** A precisely stated property has been established within an explicit formal model and verification boundary.

Required evidence:
- formal property and specification;
- explicit assumptions and preconditions;
- defined implementation and system boundary;
- proof artifact and proof-checking environment;
- proof-checker result;
- independent review of the specification-to-implementation correspondence.

Examples include a formal memory-safety property for a defined component, a soundly established data-flow property for a bounded query-construction path, or a verified correspondence between a cryptographic implementation and its specification.

A successful compiler check, Rust borrow checking, static-analysis result, or proof-assistant session does not automatically establish every security property of an entire deployed system.

Formal verification supports only the properties actually covered by the model, assumptions, and checked artifact. Level C must therefore be stated as a bounded claim.

## 7. Separation of responsibilities

The workflow should separate, as far as practicable:

1. Discovery.
2. Authorization.
3. Execution.
4. Evidence collection.
5. Independent evaluation.
6. Formal proof checking.
7. Release authorization.

Different model names or agent identities do not establish independence if credentials, data, assumptions, or control boundaries remain shared.

Where full separation is not feasible, the limitation must be declared.

## 8. Proposed workflow

```text
AI SEARCH
   |
   v
CANDIDATE WEAKNESS (PROPOSED)
   |
  G1: scope and human review
   v
REPRODUCTION ENGINE
   |
   v
EVIDENCE PACKAGE (OBSERVED / REPRODUCED)
   |
  G2: provenance and reproducibility review
   v
AI PATCH PROPOSER
   |
   v
PATCH + KILL CONDITION (PROPOSED)
   |
  G3: human patch review
   v
AUTHOR-CONTROLLED TESTS
   |
   v
LEVEL A — TESTED
   |
   v
INDEPENDENT EVALUATION
   |
   v
LEVEL B — INDEPENDENTLY TESTED
   |
   v
FORMAL SPECIFICATION + PROOF CHECKING
   |
   v
LEVEL C — INDEPENDENTLY VERIFIED, ONLY IF ESTABLISHED
   |
   v
SEPARATE HUMAN RELEASE AUTHORIZATION
```

A failed gate stops progression. The relevant artifact, evidence, and obstruction are retained; failure is not silently converted into PASS.

## 9. KAIROSEED architecture mapping

| Component | Proposed responsibility |
|---|---|
| GOVANA | Evaluate authorization requests and issue bounded permissions |
| PEP | Enforce approved task permissions |
| JIREH | Monitor and constrain execution within its defined runtime boundary |
| STRANGER | Independently evaluate evidence |
| AURORA | Reflect on results and propose improvements |
| Human authority | Approve consequential actions and release |

This is a proposed mapping, not evidence that these components currently implement or enforce the listed properties.

The target execution invariant is:

`¬Authorized ⇒ ΔS_protected = 0`

This invariant requires a precise definition of protected state, authorized transition, enforcement boundary, and observable evidence before it can be tested or claimed.

## 10. Evidence, provenance, and obstruction preservation

Each assessment should preserve:
- original candidate and source revision;
- input, environment, and tool identities;
- reproduction outcomes;
- proposed patches and patch hashes;
- author test results;
- independent test results;
- formal specifications and proof artifacts, if any;
- failed attempts and unresolved assumptions;
- verification decisions and release authorization records.

New corrections create new identifiable artifacts linked to prior versions. Previous evidence must not be overwritten by later PASS results.

### Controlled status vocabulary

`PROPOSED`, `OBSERVED`, `REPRODUCED`, `TESTED`, `INDEPENDENTLY TESTED`, `FORMALLY VERIFIED`, `AUTHORIZED`, `REJECTED`, `FAILED`, `OBSTRUCTED`, `NOT VERIFIED`.

These statuses are not interchangeable.

## 11. Falsification criteria

The research hypothesis may be rejected or materially weakened if:
1. governance controls do not measurably improve scope compliance;
2. evidence completeness does not improve;
3. independent evaluators cannot reproduce accepted findings;
4. formal checking fails to establish the declared property;
5. unauthorized consequential execution is possible within the tested boundary;
6. evidence provenance cannot be reconstructed;
7. claimed independence is undermined by undisclosed shared dependencies.

A successful experiment is not defined as obtaining a PASS result. Negative and inconclusive results are retained.

## 12. Research limitations

This specification does not establish that:
- AI can discover every vulnerability;
- passing tests prove software security;
- independent testing guarantees correctness;
- formal verification eliminates all implementation or operational risk;
- KAIROSEED components currently enforce these properties;
- this architecture is production-ready.

Initial work should use controlled samples, synthetic test cases, and authorized datasets. No third-party testing without explicit authorization is included.

## 13. Initial deliverables

1. Literature review and source register.
2. Candidate weakness record schema.
3. Reproducible evidence package schema.
4. Patch proposal and kill-condition schema.
5. Three-level assurance protocol.
6. Independent evaluation methodology.
7. KAIROSEED architecture mapping.
8. Falsification criteria.
9. Controlled prototype evaluation report.
10. Independent review dossier.

## 14. Relationship to the Riemann Hypothesis investigation

The investigations share a methodological principle, not a subject matter or evidence standard.

**Mathematical research:** AI may assist exploration; independent mathematics must establish whether a proposed proof is correct.

**Defensive software research:** AI may assist discovery and correction; independent testing and formal verification must establish bounded security claims.

The evidence differs. The independence requirement remains.

## 15. Governing method

**Build privately. Challenge rigorously. Verify independently. Release responsibly.**

**Claim ≤ Evidence ≤ Established Scope.**

**Capability ≠ Permission.**

**AI can search. Independent verification must establish.**

Soli Deo Gloria.
