"""Negative and positive structural checks; NOT containment or security proof."""
import hashlib
import json
from pathlib import Path
import tempfile
import unittest

from tools.verify_bundle import BundleValidationError, validate


def write_json(path, value):
    path.write_text(json.dumps(value, sort_keys=True, separators=(",", ":")),
                    encoding="utf-8")


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


class BundleTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.claims_path = self.root / "claims.json"
        self.evidence_path = self.root / "trace.json"
        self.claims = {
            "schema_version": "1.0",
            "claims": [{"id": "EX-1", "statement": "Synthetic bounded check",
                        "scope": "isolated fixture",
                        "falsifier": "observed mismatch",
                        "assumptions": ["trusted local fixture"]}]
        }
        write_json(self.claims_path, self.claims)
        write_json(self.evidence_path, {"observation": "synthetic only"})
        self.case = {
            "test_id": "T-1", "claim_id": "EX-1",
            "claim_set_sha256": sha(self.claims_path),
            "reported_result": "INCONCLUSIVE",
            "scope": "isolated fixture", "observer": "self-reported fixture",
            "evidence_file": "trace.json",
            "evidence_sha256": sha(self.evidence_path)
        }
        self.manifest = {"schema_version": "1.0", "claims_file": "claims.json",
                         "claims_sha256": sha(self.claims_path),
                         "tests": [self.case]}
        self.save()

    def save(self):
        write_json(self.root / "manifest.json", self.manifest)

    def test_valid_bundle_does_not_claim_independence(self):
        result = validate(self.root)
        self.assertEqual(result["bundle_check"], "BUNDLE_STRUCTURALLY_VALID")
        self.assertEqual(result["assurance"], "NOT_VERIFIED")

    def test_changed_evidence_rejected(self):
        write_json(self.evidence_path, {"observation": "changed"})
        with self.assertRaisesRegex(BundleValidationError, "evidence file hash mismatch"):
            validate(self.root)

    def test_changed_claims_rejected(self):
        self.claims["claims"][0]["scope"] = "retroactively narrowed"
        write_json(self.claims_path, self.claims)
        with self.assertRaisesRegex(BundleValidationError, "claims file hash mismatch"):
            validate(self.root)

    def test_wrong_test_claim_hash_rejected(self):
        self.case["claim_set_sha256"] = "0" * 64
        self.save()
        with self.assertRaisesRegex(BundleValidationError, "different frozen claim set"):
            validate(self.root)

    def test_unknown_claim_reference_rejected(self):
        self.case["claim_id"] = "EX-99"
        self.save()
        with self.assertRaisesRegex(BundleValidationError, "unknown claim"):
            validate(self.root)

    def test_duplicate_test_id_rejected(self):
        self.manifest["tests"].append(dict(self.case))
        self.save()
        with self.assertRaisesRegex(BundleValidationError, "duplicate test ID"):
            validate(self.root)

    def test_duplicate_claim_id_rejected(self):
        self.claims["claims"].append(dict(self.claims["claims"][0]))
        write_json(self.claims_path, self.claims)
        new_hash = sha(self.claims_path)
        self.manifest["claims_sha256"] = new_hash
        self.case["claim_set_sha256"] = new_hash
        self.save()
        with self.assertRaisesRegex(BundleValidationError, "duplicate claim ID"):
            validate(self.root)

    def test_path_traversal_rejected(self):
        self.case["evidence_file"] = "../trace.json"
        self.save()
        with self.assertRaisesRegex(BundleValidationError, "unsafe evidence filename"):
            validate(self.root)

    def test_duplicate_json_key_rejected(self):
        (self.root / "manifest.json").write_text(
            '{"schema_version":"1.0","schema_version":"1.0"}', encoding="utf-8")
        with self.assertRaisesRegex(BundleValidationError, "duplicate JSON key"):
            validate(self.root)

    def test_author_claim_of_confirmation_is_not_assurance_pass(self):
        self.case["reported_result"] = "CONFIRMED_WITHIN_SCOPE"
        self.save()
        result = validate(self.root)
        self.assertEqual(result["assurance"], "NOT_VERIFIED")

    def test_bad_reported_result_rejected(self):
        self.case["reported_result"] = "PASS_ATOMICITY_PROVEN"
        self.save()
        with self.assertRaisesRegex(BundleValidationError, "unknown reported_result"):
            validate(self.root)


if __name__ == "__main__":
    unittest.main()
