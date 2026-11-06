import unittest
from canonical_flow import Request, run_flow

def req(**changes):
    data = dict(request_id="demo-1", purpose="Synthetic research", human_approved=True,
                authorization_id="local-demo-1", action="synthetic_increment",
                scope="sandbox:counter", increment=1)
    data.update(changes)
    return Request(**data)

class CanonicalFlowTests(unittest.TestCase):
    def test_authorized_synthetic_transition(self):
        e = run_flow(req(), 5)
        self.assertTrue(e["authorized"])
        self.assertTrue(e["verified"])
        self.assertEqual((e["before"], e["after"]), (5, 6))
        self.assertFalse(e["production"])

    def test_denials_preserve_state(self):
        for change in ({"human_approved": False}, {"authorization_id": ""},
                       {"action": "publish"}, {"scope": "production"},
                       {"increment": 2}, {"increment": True}, {"purpose": ""}):
            with self.subTest(change=change):
                e = run_flow(req(**change), 7)
                self.assertFalse(e["authorized"])
                self.assertEqual(e["before_sha256"], e["after_sha256"])
                self.assertEqual(e["after"], 7)
                self.assertEqual(e["stages"][3]["status"], "BLOCKED")

    def test_deterministic_evidence(self):
        self.assertEqual(run_flow(req()), run_flow(req()))

    def test_invalid_initial_state(self):
        for value in (-1, 1.5, True):
            with self.assertRaises(ValueError):
                run_flow(req(), value)

    def test_six_stages_and_no_external_actions(self):
        e = run_flow(req())
        self.assertEqual([s["stage"] for s in e["stages"]],
            ["FAITH_GROUND", "HUMAN_AUTHORITY", "GOVANA", "JIREH",
             "INDEPENDENT_VERIFICATION", "EVIDENCE"])
        self.assertTrue(e["simulated"])

if __name__ == "__main__":
    unittest.main()
