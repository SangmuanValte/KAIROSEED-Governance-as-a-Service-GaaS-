# CI Findings — 2026-11-06

## Direct GitHub evidence

- [Failed GaaS run #42264348902](https://github.com/SangmuanValte/KAIROSEED-Governance-as-a-Service-GaaS-/actions/runs/42264348902): commit `9b846da128e2ff325297dfde4a0860267e545313`; full suite reports **19 passed, 1 failed**.
- [Failed GaaS run #42144072574](https://github.com/SangmuanValte/KAIROSEED-Governance-as-a-Service-GaaS-/actions/runs/42144072574): earlier revision, also failed.
- [Successful GaaS run #37677125279](https://github.com/SangmuanValte/KAIROSEED-Governance-as-a-Service-GaaS-/actions/runs/37677125279): earlier commit `5ee38eeae2b088ead534e6a6db7828c9054dd388`; **26 passed**.

A past success does not override a later failure. These outcomes have separate commit identities and different tested revisions.

## Root-cause investigation

Failed test: `test_security_invariants.py::test_evidence_chain_detects_modified_record`.

The test sets `ledger.records[0]["reason"] = "tampered"`, then expects `verify_chain()` to return false. However, the `records` property generates a new Python list of dictionaries from stored SQL rows. Mutating a returned list element does not alter persistent records. Thus the expected stored-data tamper condition was not created.

The CI output reports `assert not True`. This is a **test-fixture defect**, not a demonstrated exploit against the stored ledger integrity mechanism.

## Required correction and renewed evidence

- Revise the fixture so the intended storage-integrity scenario is actually exercised in an isolated test database.
- Check a valid ledger and an independently changed test fixture as separate controls.
- Rerun the complete test suite and preserve the exact commit, environment, test command and raw log.
- Do not claim the integrity property passed until those outputs are available.
- Do not treat a result hash or signature as proof of actual protected-state noninterference.

## Release-workflow language risk

`.github/workflows/kairoseed-gaas-release.yml` currently contains the literal output `INDEPENDENT_VERIFICATION=PASS`. This string is not itself independent verification. A reviewer must check a genuine independent evidence artifact rather than rely on fixed text in a workflow. Production activation remains a separate authorized process; this dossier does not trigger it.

## Current disposition

- **Current-head CI:** FAIL (one observed test failure).
- **Persisted ledger tamper-detection assurance:** NOT VERIFIED by the failed test.
- **Production release and end-to-end containment:** NOT VERIFIED / NOT AUTHORIZED.
- **Canonical documentation:** UNCHANGED.

**No verified evidence → No PASS.**
