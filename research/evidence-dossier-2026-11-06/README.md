# KAIROSEED — Evidence-Bounded Research Dossier (2026-11-06)

> **Classification:** Non-canonical research documentation and reproducibility tooling.  
> **Base inspected repository revision:** `9b846da128e2ff325297dfde4a0860267e545313`.  
> **Assurance decision:** **HOLD / NOT VERIFIED** for end-to-end protected-effect containment and production readiness.  
> **Canonical specification:** FROZEN — NOT CHANGED by this dossier.  
> **Authority:** Documentation and bounded research only; no release, production use, partner approval, or policy expansion.

## What this dossier demonstrates

KAIROSEED has a body of governance research with inspectable source artifacts: a Python decision-and-ledger prototype, a TypeScript tool-call reference adapter, abstract Lean proofs, operational threat-model documents, a frozen JIREH research classification, and recorded CI/test results. **Existence of these artifacts establishes research work, not universal or deployed enforcement.**

The current inspected main GaaS workflow [run 42264348902](https://github.com/SangmuanValte/KAIROSEED-Governance-as-a-Service-GaaS-/actions/runs/42264348902) concluded **failure** (19 passed, one failed). Its identified negative control `test_evidence_chain_detects_modified_record` mutates a detached in-memory copy returned from SQLite, not persisted data. A separate read-only audit reported a local *diagnostic copy* passing after a test-only correction. That was not a merged repair or a successful current-head CI run.

## Contents / required proof package

| Artifact | Purpose | Current state |
|---|---|---|
| [EVIDENCE_INDEX.md](EVIDENCE_INDEX.md) | Pinned primary artifacts, CI sources, provenance and observation limits | Source inspected |
| [CLAIM_REGISTER.md](CLAIM_REGISTER.md) | Claim IDs, narrow scope, falsifiers and current disposition | Research registry, NOT a cryptographic pre-test freeze |
| [FINDINGS_AND_GAPS.md](FINDINGS_AND_GAPS.md) | Code-level findings and unresolved proof obligations | Source-based or historical, explicitly distinguished |
| [VERIFICATION_PROTOCOL.md](VERIFICATION_PROTOCOL.md) | Independent test design, protected-effect measurement, verdict criteria | Proposed, not executed here |
| [RESEARCH_HISTORY.md](RESEARCH_HISTORY.md) | Historical internal research lineage with evidentiary limitations | Selected retrospective, not comprehensive |
| [RELEASE_GATE.md](RELEASE_GATE.md) | Required release, proof, and independent review artifacts | Release HOLD |
| [tools/verify_bundle.py](tools/verify_bundle.py) | Offline, stdlib-only hash/reference validator | Source utility; it does **not** attest observation truth |
| [tests/test_verify_bundle.py](tests/test_verify_bundle.py) | Negative tests for verifier structural checks | Tests to execute on exact proposed revision |
| [example_claims.json](example_claims.json) | Illustrative claim set | Example ONLY, not committed before historical tests |

## Do not conflate these proof levels

1. **Written specification:** What must hold.
2. **Source inspection:** What a named revision actually contains.
3. **Test execution:** What a specified fixture actually did.
4. **Independent observation:** What happened to protected resources and relevant external effects.
5. **Assurance decision:** A per-claim conclusion justified by a verifiably precommitted claim, trustworthy evidence, and established scope.
6. **Production permission:** A separate explicit authorized decision.

Passing local code tests is insufficient to prove complete mediation, absence of all bypasses, eBPF/seccomp operation, Lyapunov stability, or an independently operated verifier.

## Frozen research boundary

The [JIREH v1.1 classification at pinned revision](https://github.com/SangmuanValte/KAIROSEED-Governance-as-a-Service-GaaS-/blob/be03164e5768f2ae6a877efe3a8be647bb7bd757/docs/research/JIREH-v1.1-claim-boundary-and-design-intent.md) and [freeze manifest](https://github.com/SangmuanValte/KAIROSEED-Governance-as-a-Service-GaaS-/blob/9b846da128e2ff325297dfde4a0860267e545313/docs/research/freezes/JIREH-v1.1-design-intent-freeze-2026-11-06.md) remain historical documentation snapshots. The declaration did not create an independent WORM witness or retroactive pre-test freeze.

Related open falsification contract: [GitHub issue #30](https://github.com/SangmuanValte/KAIROSEED-Governance-as-a-Service-GaaS-/issues/30).

**No verified evidence → No PASS.**  
**Containment is not inferred. Containment is inspected.**  
**Claim ≤ Evidence ≤ Established Scope.**
