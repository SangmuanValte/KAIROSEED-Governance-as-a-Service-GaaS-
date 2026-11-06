# Run the offline consistency validator

**NOT a security proof; NOT an independent containment verifier.** The tool verifies that files named in a bundle exist and match declared SHA-256 hashes, that JSON keys and claim/test identifiers are unambiguous, and that every listed claim has test references. It cannot independently establish the truth, completeness or chronology of evidence. It will **always** report `assurance: NOT_VERIFIED`.

Python 3.10+ standard library only. Run from this dossier directory:

```bash
python -m unittest discover -s tests -v
python tools/verify_bundle.py /path/to/your/isolated-bundle
```

A bundle is a directory with a flat `manifest.json`, claim-set file, and evidence files. The manifest format is:

```json
{
  "schema_version": "1.0",
  "claims_file": "claims.json",
  "claims_sha256": "<SHA256 of exact claims.json file bytes>",
  "tests": [
    {
      "test_id": "T-01",
      "claim_id": "EX-1",
      "claim_set_sha256": "<same claim-set SHA256>",
      "reported_result": "INCONCLUSIVE",
      "scope": "exact tested resources, threat model and time range",
      "observer": "declared observer and its trust limitations",
      "evidence_file": "trace.json",
      "evidence_sha256": "<SHA256 of exact trace.json file bytes>"
    }
  ]
}
```

The `reported_result` may be `CONFIRMED_WITHIN_SCOPE`, `CONTRADICTED`, or `INCONCLUSIVE`; these are **submitted labels**, NOT independently endorsed verdicts. Unsupported values are rejected.

`example_claims.json` is a purely illustrative claim set; it is not proof of a pre-test freeze or an observed outcome. To use the tool for a real local experiment, create a new claims file, publish its immutable pre-test commitment through an independently inspectable channel, and supply authentic raw evidence with a separately established observer. A structural PASS does not authorize a security PASS.

The negative tests include modified evidence, post-hoc claim editing, duplicate keys/IDs, mismatched claim references, path traversal, and a fabricated proof label.
