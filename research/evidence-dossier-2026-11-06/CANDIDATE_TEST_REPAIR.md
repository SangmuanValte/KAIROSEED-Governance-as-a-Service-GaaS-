# Test-only candidate: persisted SQLite tamper negative control

**Status:** Proposed repair on `research/evidence-package-20261106-verified-scope`; **no security assurance upgrade**.

## Baseline

The inspected main workflow [run 42264348902](https://github.com/SangmuanValte/KAIROSEED-Governance-as-a-Service-GaaS-/actions/runs/42264348902) failed one negative-control test; this was `test_evidence_chain_detects_modified_record` under `prototypes/kairoseed-gaas-v0.1/test_security_invariants.py`.

The prior test changed `ledger.records[0]["reason"]`, but `EvidenceLedger.records` reconstructs detached Python dictionaries from SQLite each time. Therefore the test did not alter the durable row subsequently checked by `verify_chain()`. This explains the source-level failure; it does not mean real stored tampering is undetectable.

## Candidate change (test only)

- Use a temporary on-disk SQLite file; no production data.
- Confirm untampered stored chain initially verifies.
- Demonstrate changing a detached snapshot leaves stored ledger unchanged.
- Close the ledger; directly update the disposable stored row with a different reason.
- Reopen the ledger; assert `verify_chain()` rejects the persisted-row modification.
- Preserve the second record's previously linked hash as an additional fixture check.

**Implementation under review:** [test_security_invariants.py](https://github.com/SangmuanValte/KAIROSEED-Governance-as-a-Service-GaaS-/blob/research/evidence-package-20261106-verified-scope/prototypes/kairoseed-gaas-v0.1/test_security_invariants.py)

The actual `kairoseed_gaas.py` ledger and policy decision code was **not modified**. This test only assesses a narrow tamper-evidence property against one local stored-row modification. It does not prove WORM storage, authentic event collection, complete effect observation, or containment.

## Reproduction on this branch

```bash
python -m pip install -r prototypes/kairoseed-gaas-v0.1/requirements.txt
cd prototypes/kairoseed-gaas-v0.1
python -m pytest -q
```

Review the branch's **actual** GaaS workflow output before labeling the candidate fixed. The main-branch failure remains a historical, revision-bound result and is never erased.

**Expected next disposition:** reviewer checks diff, test logs, and original-vs-updated fixture; independent verification remains a separate gate.
