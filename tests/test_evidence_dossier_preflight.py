"""Unit tests for dossier metadata preflight only.

These tests do not verify GOVANA/JIREH runtime safety.
"""
from pathlib import Path
import unittest

from research.evidence_dossier.preflight import check_claims


ROOT = Path(__file__).resolve().parents[1]


def fixture() -> dict:
    return {
        "schema": "kairoseed-research-dossier-v0.1",
        "assurance": "NOT_VERIFIED",
        "canonical_specification": "FROZEN_UNCHANGED",
        "claims": [{
            "id": "TEST-001",
            "status": "CODE_PRESENT",
            "statement": "Reference documentation is present",
            "scope": "Repository fixture only",
            "evidence": ["README.md"],
            "missing": "Independent operational verification",
        }],
    }


class EvidenceDossierPreflightTests(unittest.TestCase):
    def test_valid_metadata_is_accepted_without_security_pass(self):
        self.assertEqual(check_claims(fixture(), ROOT), [])

    def test_invalid_assurance_claim_is_rejected(self):
        data = fixture()
        data["assurance"] = "PASS"
        self.assertTrue(check_claims(data, ROOT))

    def test_duplicate_claim_id_is_rejected(self):
        data = fixture()
        data["claims"].append(dict(data["claims"][0]))
        self.assertTrue(any("duplicate" in x for x in check_claims(data, ROOT)))

    def test_unavailable_source_is_rejected(self):
        data = fixture()
        data["claims"][0]["evidence"] = ["nonexistent/research-proof.txt"]
        self.assertTrue(any("missing repository source" in x
                            for x in check_claims(data, ROOT)))


if __name__ == "__main__":
    unittest.main()
