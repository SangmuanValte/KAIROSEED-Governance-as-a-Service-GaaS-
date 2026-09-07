import unittest

from pipeline import Decision, Proposal, run_pipeline


class GovernedPipelineTests(unittest.TestCase):
    def test_missing_capability_blocks(self):
        evidence = run_pipeline(Proposal("capability test", False, True, "low", "AUTH-TEST-001"))
        self.assertEqual(evidence["decision"], Decision.BLOCK.value)
        self.assertEqual(evidence["result"], "execution_not_started")
        self.assertEqual(evidence["events"][-2]["stage"], "EXECUTE")
        self.assertEqual(evidence["events"][-2]["status"], "BLOCKED")

    def test_missing_permission_does_not_execute(self):
        evidence = run_pipeline(Proposal("permission test", True, False, "low", None))
        self.assertEqual(evidence["decision"], Decision.REVIEW.value)
        self.assertEqual(evidence["result"], "execution_not_started")

    def test_missing_authorization_does_not_execute(self):
        evidence = run_pipeline(Proposal("authorization test", True, True, "low", None))
        self.assertEqual(evidence["decision"], Decision.REVIEW.value)
        self.assertEqual(evidence["result"], "execution_not_started")

    def test_authorized_low_risk_action_is_simulated(self):
        evidence = run_pipeline(Proposal("bounded simulation", True, True, "low", "AUTH-TEST-002"))
        self.assertEqual(evidence["decision"], Decision.APPROVE.value)
        self.assertEqual(evidence["result"], "simulated_bounded_execution")
        self.assertTrue(evidence["evidence_sha256"])

    def test_high_risk_action_requires_review(self):
        evidence = run_pipeline(Proposal("production publish", True, True, "high", "AUTH-TEST-003"))
        self.assertEqual(evidence["decision"], Decision.REVIEW.value)
        self.assertEqual(evidence["result"], "execution_not_started")


if __name__ == "__main__":
    unittest.main()
