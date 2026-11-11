# Check/Action Representation Mismatch: Four Git Security Vulnerabilities

**Research artefact:** KAIROSEED-GIT-REP-001  
**Version:** 0.1-draft  
**Author:** Sangmuan Valte  
**Research date:** 2026-11-11  
**Publication target:** `SangmuanValte/KAIROSEED-Governance-as-a-Service-GaaS-`  
**Proposed path:** `research/security/git-check-action-representation-mismatch-2026-11-11.md`  
**Status:** SOURCE-GROUNDED RESEARCH DRAFT — NOT INDEPENDENTLY REPRODUCED  
**Production relevance:** No KAIROSEED production claim or authorization is made.

---

## Abstract

Four Git security vulnerabilities disclosed on 10 November 2026 provide concrete examples of security checks and later operations disagreeing about the meaning, representation, or trust status of input. The cases concern recursive-clone path handling (CVE-2026-111760), an unvalidated server-advertised unborn `HEAD` (CVE-2026-113408), binary-patch size validation (CVE-2026-114469), and unsafe `fast-import` features accepted from an untrusted command stream (CVE-2026-114466).

This paper groups them under the research lens **check/action representation mismatch**. The grouping is conceptual, not a claim that all four defects share one root cause, exploit primitive, severity, or remediation. In particular, the `fast-import` case is more directly a trust/provenance-boundary failure than an object-identity defect.

The central thesis is:

> **Object identity and input meaning must be established—not assumed—where the check and the action can disagree.**

The cases support the value of validating the representation that will actually be consumed, binding validation to the later operation, and preserving trust context across parsing and execution boundaries. They do not prove that every software enforcement boundary fails in the same way, nor do they prove that KAIROSEED prevents these classes of defects.

## 1. Scope and method

This is a desk-research synthesis based primarily on the GitHub security release announcement dated 10 November 2026 and the linked vulnerability records. The announcement is authored by Elijah Newren, a GitHub Staff Software Engineer, and describes the Git project’s release of fixes. The four CVEs were selected because their published descriptions expose a meaningful difference between an input’s checked representation and its later interpretation or effect.

This paper does **not**:
- reproduce the vulnerabilities or provide exploit procedures;
- independently inspect or execute the corresponding patches;
- establish affected-version boundaries for every distributor or downstream package;
- claim that the four defects are technically equivalent;
- establish a general theorem about software security; or
- claim that KAIROSEED, GOVANA, or JIREH detects or prevents these vulnerabilities.

The evidence level is therefore **source-reported**. Independent reproduction and patch-level review remain open.

## 2. Case studies

### 2.1 CVE-2026-111760 — recursive-clone path handling

The GitHub release announcement describes an integer-truncation issue in Git index path handling. A path could be checked under a long representation and subsequently written using a shorter representation. The published impact chain involves submodule metadata and a symbolic link that can direct Git toward a directory containing attacker-controlled configuration or hooks during recursive clone processing.

**Mismatch lens:** the path representation accepted by validation is not necessarily the path representation used by the later write.

**Reported remediation:** reject excessively long index-entry paths before their lengths can be truncated.

**Research question:** Does the implementation ensure that the exact normalized path used for the write is the same path whose safety properties were checked, including across integer conversions and filesystem resolution?

**Evidence limitation:** the GitHub advisory page available during this review lists affected versions as “all,” patched versions as “none,” and says patches are being discussed, while the GitHub release announcement says fixes are included in Git 2.56.1 and several maintenance backports. This is a source-state discrepancy that must be reconciled against the canonical release and patch records before making a definitive patched-version statement.

### 2.2 CVE-2026-113408 — server-advertised unborn `HEAD`

The release announcement describes cloning an empty repository over Git protocol v2. A server can advertise a symbolic `HEAD` target for an unborn branch. The target was not validated before being stored locally; with the files reference backend, a later ref update could write outside the intended reference directory.

**Mismatch lens:** a remotely supplied symbolic reference is accepted into local state before its target is validated against the constraints required by the later filesystem-backed ref update.

**Reported remediation:** validate the advertised target before accepting it, and validate other reference names and symbolic-reference targets received through protocol v2.

**Research question:** Are all remotely supplied reference names and symbolic targets validated at the point of ingestion and again, where needed, at the effect boundary using the same canonical rules?

### 2.3 CVE-2026-114469 — binary-patch size validation

The release announcement says Git imposed an approximately 1 GiB patch-size limit, but the check considered the supplied encoded patch size. Binary patches can be compressed and encoded; their declared uncompressed size can be much larger. A patch that appears small at the input boundary can therefore exceed the intended processing bound after expansion, resulting in an out-of-bounds read and crash.

**Mismatch lens:** the resource check measures the encoded representation while processing consumes the expanded representation.

**Reported remediation:** check the declared uncompressed size before processing the binary patch.

**Research question:** Are limits applied to the representation that consumes memory and processing resources, with safe handling of declarations, arithmetic, and actual expansion?

### 2.4 CVE-2026-114466 — `fast-import` stream features

The release announcement describes three `fast-import` features that could access paths outside the repository but were not covered by existing restrictions for untrusted input streams. Two submodule-rewriting features could read arbitrary files, with possible disclosure through error messages; `export-pack-edges` could create files or append to existing files. The release says these features are now rejected when supplied through the input stream unless the caller explicitly enables `--allow-unsafe-features`.

**Mismatch lens:** a stream is treated as untrusted, but individual features carried by that stream do not consistently inherit the same trust restriction.

**Reported remediation:** reject the affected features when they arrive through an untrusted stream unless the caller explicitly opts into unsafe features.

**Research question:** Is trust provenance preserved from the stream boundary through feature parsing to every file-accessing operation, and is any opt-in explicit, scoped, and auditable?

## 3. Comparative analysis

| CVE | Checked representation or assumption | Later interpretation/effect | Primary mismatch |
|---|---|---|---|
| 2026-111760 | Index path length before truncation | Path used for filesystem write | Validation/write path disagreement |
| 2026-113408 | Server-advertised unborn symbolic `HEAD` accepted before target validation | Later files-backend ref update | Ingestion/effect validation gap |
| 2026-114469 | Encoded patch size | Expanded binary-patch size | Input-size/resource-size disagreement |
| 2026-114466 | Stream-level untrusted status applied incompletely to features | Feature-specific filesystem reads/writes | Trust-provenance propagation gap |

The first three cases directly illustrate representation or interpretation differences at validation and use boundaries. The fourth broadens the analysis: a parser or command stream can carry capabilities whose trust restrictions must remain attached to the operation they authorize. It should not be described as the same technical bug as integer truncation or encoded-size accounting.

The common design lesson is narrower than “validate everything twice.” Repeated checks alone can still be inconsistent. A stronger requirement is to define a canonical representation and trust context, validate the exact value and operation that will be used, and prevent an unchecked transformation or alternate execution path from changing the security meaning between validation and effect.

## 4. Security-engineering implications

The cases suggest a review checklist for software that accepts paths, references, compressed data, or command streams:

1. **Canonicalization:** Is there one documented canonical form for the value being authorized?
2. **Transformation accounting:** Can truncation, decoding, decompression, normalization, or path resolution change the value after validation?
3. **Binding:** Is the later operation bound to the exact validated value, rather than re-reading or re-interpreting mutable input?
4. **Resource accounting:** Are limits applied to expanded size and actual resource consumption, not merely encoded input size?
5. **Trust propagation:** Does an untrusted source remain untrusted through every parser feature and downstream operation?
6. **Effect-boundary enforcement:** Are filesystem writes, reference updates, and other consequential effects constrained at the point they occur?
7. **Evidence:** Can a reviewer inspect the source revision, patch, test, environment, and observed result supporting each security claim?

These are review questions, not proof that any particular implementation satisfies them.

## 5. Relationship to KAIROSEED

KAIROSEED distinguishes capability, permission, authorization, execution, and evidence. These Git cases are useful external examples for studying how an operation can escape the assumptions made at an earlier validation boundary.

They do **not** validate KAIROSEED’s architecture. The vulnerabilities concern Git’s own parsing, path, reference, resource-accounting, and import behavior. A KAIROSEED adapter or policy gate would need its own threat model, implementation review, adversarial tests, and independent observation of protected effects.

A possible future KAIROSEED evaluation could translate the general lessons into harmless isolated fixtures: path canonicalization consistency, symbolic-reference validation, encoded-versus-expanded resource limits, and propagation of untrusted provenance. Such tests must be separately specified, authorized, implemented, and independently reviewed. No such test is claimed here.

## 6. Limitations and open verification work

- **Patch verification:** The source announcement summarizes fixes; this paper has not independently inspected the full patch diffs or test additions.
- **Version reconciliation:** The CVE-2026-111760 advisory metadata and the release announcement appear inconsistent about patch availability. The exact canonical status needs confirmation from the Git release and maintenance-branch commits.
- **Distributor variance:** Downstream packages may backport fixes or publish different status at different times. Upstream release numbers must not be treated as a complete inventory of deployed exposure.
- **Root-cause diversity:** The four cases are grouped by a common review lens, not a single implementation defect.
- **Exploitability:** This paper does not independently reproduce any vulnerability or establish exploitability in a particular installation.
- **Generality:** Four selected cases do not establish prevalence across Git, other software, or all authorization systems.

### Falsifiable follow-up questions

1. For each CVE, can the relevant upstream patch and regression test be located and mapped to the reported defect?
2. Does the patch ensure that validation and the consequential operation use the same canonical value and constraints?
3. Do upstream regression tests include negative cases for the relevant representation or trust-boundary transition?
4. Do maintenance backports preserve the same security property, rather than merely compiling or passing unrelated tests?
5. Can an independent reviewer reproduce the documented pre-fix failure and post-fix rejection in an isolated, authorized test environment?

Until those checks are completed, patch correctness and independent reproduction remain **NOT VERIFIED in this research artefact**.

## 7. Conclusion

The four Git vulnerabilities illustrate a recurring class of security-review problem: a value can pass a check in one representation or trust context and later be interpreted or used differently. The cases justify examining the relationship between validation, transformation, provenance, and effect—not assuming that an earlier check automatically protects a later action.

The defensible conclusion is:

> **Security validation must remain bound to the exact representation, trust context, and resource that the consequential operation will use.**

This is a source-grounded research observation, not a universal theorem, a claim of novelty, or evidence that KAIROSEED has solved the problem.

## References

1. Elijah Newren, GitHub Blog, [“Git security vulnerabilities announced”](https://github.blog/open-source/git/git-security-vulnerabilities-announced-7/), 2026-11-10. Primary release announcement covering all six vulnerabilities, remediation summaries, release/backport versions, and operational recommendations. This paper uses the four CVEs in scope.
2. Git project, [GHSA-vp2w-7xxj-jvxr: Recursive clones are susceptible to Remote Code Execution](https://github.com/git/git/security/advisories/GHSA-vp2w-7xxj-jvxr), published 2026-11-10. Advisory metadata should be reconciled with the release announcement as described above.
3. Git project, [Git v2.56.1 release notes](https://github.com/git/git/blob/v2.56.1/Documentation/RelNotes/2.56.1.adoc). Release-note record; patch-level source review remains outstanding.
4. GitLab Git project work item, [CVE-2026-113408](https://gitlab.com/gitlab-org/git/-/work_items/809), linked by the GitHub release announcement.
5. GitLab Git project work item, [CVE-2026-114469](https://gitlab.com/gitlab-org/git/-/work_items/811), linked by the GitHub release announcement.
6. GitLab Git project work item, [CVE-2026-114466](https://gitlab.com/gitlab-org/git/-/work_items/812), linked by the GitHub release announcement.

**Source review date:** 2026-11-11  
**Research status:** SOURCE-GROUNDED DRAFT  
**Independent patch review:** NOT PERFORMED  
**Independent reproduction:** NOT PERFORMED  
**KAIROSEED validation:** NOT CLAIMED  
**Production authorization:** NO
