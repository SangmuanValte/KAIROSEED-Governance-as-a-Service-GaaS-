# Independent Verification Protocol — Proposed, Not Yet Executed

## Preconditions / claim freeze

1. Finalize the *exact* claim set with IDs, scope, assumptions, prohibited effects and falsifiers.
2. Serialize it in one declared format, hash exact bytes, and commit/publish a pre-test commitment through an independently inspectable chronological mechanism. GitHub commit or declaration alone is not an independent trusted timestamp.
3. Bind each test case to the exact claim hash **before test execution**. The reviewer must inspect whether a result was actually run after that commitment.
4. If the claim changes, preserve prior version and test verdict; create a new hash and separate run. No retroactive overwrite or silent narrowing.

## Threat model / independent observer

Declare actors, authoritative grant source, revocation effective time, protected-resource `P`, allowed and prohibited operations, external effects, observation coverage, concurrency and TOCTOU assumptions, host/kernel privileges, and all mandatory enforcement paths. Explain observer placement, shared dependencies and common-mode tampering risks. An 'independent verifier' label is not a trust proof.

## Minimum isolated falsification cases

- Valid grant, correct subject/action/resource/parameters and bounded effect.
- Missing, expired, revoked, wrong-subject, wrong-target, wrong-scope, wrong-policy and replayed authorization.
- Concurrent attempts using one grant and revocation between decision and actual effect.
- Direct execution against protected resource *without* calling adapter (isolated test fixture only).
- Partial tool effect followed by error, failed evidence append, retry after uncertain outcome.
- Intermediate unauthorized mutation restored before the final snapshot, and synthetic external side-effect.
- Denial trace that says BLOCK while the protected resource is actually modified.
- Incomplete observer/ledger data, corrupted receipt or sensor/clock inconsistency.

Measure **actual protected-state transitions throughout the observation interval**. Before/after hashes alone can miss transient effects; signed logs alone can repeat false observations. Neither one passing example nor a large finite test count proves universal bypass impossibility.

## Artifact checklist required to assert a bounded PASS

- [ ] Versioned signed or otherwise independently precommitted claim-set digest
- [ ] Exact repository commit, build dependencies, kernel/toolchain and isolated fixture
- [ ] Human authorization and bounded synthetic test scope
- [ ] Test manifest referencing each claim hash, threat model and expected outcome
- [ ] Trace of action, actor, resource, parameter bounds and grant status
- [ ] Coverage map, independent effect observer and disclosed shared trust base
- [ ] Authentic raw observations of intermediate and external effects, including failures
- [ ] Independent verification of evidence integrity, chronology and effect attribution
- [ ] Per-claim result: CONFIRMED WITHIN SCOPE / CONTRADICTED / INCONCLUSIVE, justified by cited evidence
- [ ] Reproducible instructions, immutable-linked supersession history, and limitations
- [ ] Separate production/readiness authorization (not inferred from the verdict)

## Tooling boundary

The included `tools/verify_bundle.py` checks **syntactic and cryptographic file consistency** of a local evidence bundle. It does NOT validate that measurements came from a genuinely independent sensor, that claimed observations are true, that all effects were covered, that the pre-test commitment was independently witnessed, or that a proof obligation passed. Its only affirmative result is `BUNDLE_STRUCTURALLY_VALID`; assurance remains `NOT_VERIFIED` unless separately assessed by an independently accountable process.

## Specific JIREH C3/C6 question

`SIGSTOP sent` does not imply quiescence, memory immutability or exclusion of external writers. `t_freeze < t_hash < t_sign < t_kill` demonstrates a reported order, not atomicity. The bounded KGS-003-EVIDENCE-002 measurement must report race distributions, post-request mutations, stop-confirmation latency, observation gaps and external writer effects. Synthetic-only results cannot be promoted to eBPF/seccomp or production JIREH guarantees.

**Related:** [GitHub issue #30](https://github.com/SangmuanValte/KAIROSEED-Governance-as-a-Service-GaaS-/issues/30); [non-canonical JIREH freeze](https://github.com/SangmuanValte/KAIROSEED-Governance-as-a-Service-GaaS-/blob/9b846da128e2ff325297dfde4a0860267e545313/docs/research/freezes/JIREH-v1.1-design-intent-freeze-2026-11-06.md).
