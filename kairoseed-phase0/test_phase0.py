"""Phase 0 split-process synthetic falsification suite.

All fixtures are synthetic. Multi-process separation and HMAC fixtures do not
establish independent assurance or OS/kernel containment.
"""
from __future__ import annotations

import hashlib
import json
import multiprocessing
import os
from pathlib import Path
import shutil
import tempfile
import time
import unittest
from uuid import uuid4

from audit import audit_worker
from gat import gat_worker, digest, mac
from ledger import Ledger, ledger_worker
from pep import fixture_worker, jireh_trap, pep_worker
from stranger import stranger_worker

ROOT = Path(__file__).resolve().parent
SCOPE_FILE = ROOT / "scope.json"


class Phase0SplitTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.path = Path(self.temp.name) / "ledger.jsonl"
        self.scope = json.loads(SCOPE_FILE.read_text(encoding="utf-8"))
        self.assertEqual(self.scope["environment"], "SYNTHETIC_ONLY")
        self.principal_key = os.urandom(32)
        self.receipt_key = os.urandom(32)
        ctx = multiprocessing.get_context("spawn")
        self.ctx = ctx

        self.ledger_cli, ledger_server = ctx.Pipe()
        gat_query, ledger_query = ctx.Pipe()
        gat_server, gat_client = ctx.Pipe()
        self.pep_cli, pep_server = ctx.Pipe()
        fixture_apply, fixture_exec = ctx.Pipe()
        fixture_read, fixture_observe = ctx.Pipe()
        self.stranger_cli, stranger_server = ctx.Pipe()
        self.audit_cli, audit_server = ctx.Pipe()

        self.processes = {
            "ledger": ctx.Process(
                target=ledger_worker, args=(ledger_server, ledger_query, str(self.path))
            ),
            "fixture": ctx.Process(
                target=fixture_worker, args=(fixture_exec, fixture_observe, self.scope, self.receipt_key)
            ),
            "gat": ctx.Process(
                target=gat_worker,
                args=(gat_server, gat_query, str(SCOPE_FILE), self.principal_key, self.receipt_key),
            ),
            "pep": ctx.Process(
                target=pep_worker,
                args=(pep_server, gat_client, fixture_apply, self.scope, self.receipt_key),
            ),
            "stranger": ctx.Process(
                target=stranger_worker, args=(stranger_server, fixture_read)
            ),
            "audit": ctx.Process(
                target=audit_worker, args=(audit_server, str(self.path), str(SCOPE_FILE))
            ),
        }
        for p in self.processes.values():
            p.start()
        self.addCleanup(self.stop_children)

    def stop_children(self):
        # Archive generated test receipts, if explicitly requested, before shutdown.
        output = os.environ.get("KAIROSEED_PHASE0_LEDGER_PATH")
        if output and self.path.exists():
            aggregate = Ledger(output)
            if aggregate.verify_chain():
                for record in Ledger(self.path).records():
                    aggregate.append({**record["body"], "source_test": self.id()})
        for process in self.processes.values():
            if process.is_alive():
                process.terminate()
            process.join(timeout=2)
            if process.is_alive():
                process.kill()
                process.join(timeout=2)

    def proposal(self, resource="doc_A", action="share", principal=None, note=None):
        values = {
            "request_id": uuid4().hex,
            "proposer_id": "synthetic-proposer",
            "principal_id": principal or self.scope["principal_id"],
            "purpose": self.scope["purpose"],
            "resource": resource,
            "action": action,
            "expected_delta": {resource: True},
        }
        if note is not None:
            values["untrusted_memory_hint"] = note
        return values

    def token(self, resource="doc_A", action="share", principal=None, expired=False):
        now = time.time_ns()
        issued = now - 40_000_000_000 if expired else now
        body = {
            "token_id": uuid4().hex,
            "principal_id": principal or self.scope["principal_id"],
            "purpose": self.scope["purpose"],
            "resource": resource,
            "action": action,
            "scope_digest": digest(self.scope),
            "issued_ns": issued,
            "expires_ns": issued + 30_000_000_000,
        }
        return {**body, "signature": mac(body, self.principal_key)}

    def request(self, conn, payload, timeout=5):
        conn.send(payload)
        self.assertTrue(conn.poll(timeout), f"IPC service timeout: {payload.get('op')}")
        return conn.recv()

    def observe(self):
        result = self.request(self.stranger_cli, {"op": "snapshot"})
        self.assertTrue(result["ok"])
        return result["state"]

    def audit(self, ledger_path=None):
        value = {"op": "audit"}
        if ledger_path is not None:
            value["ledger_path"] = str(ledger_path)
        return self.request(self.audit_cli, value)

    def run_action(self, case_id, proposal, token, expected_decision):
        before = self.observe()
        result = self.request(
            self.pep_cli, {"op": "submit", "proposal": proposal, "token": token},
            timeout=5
        )
        after = self.observe()
        expected = proposal["expected_delta"] if result["decision"] == "ALLOW" else {}
        observed = self.request(
            self.stranger_cli,
            {"op": "verify_delta", "before": before, "after": after, "expected": expected},
        )
        self.assertTrue(observed["ok"])
        delta = observed["observed_delta"]
        atoms = [
            "share:" + resource for resource, state in sorted(delta.items()) if state
        ]
        claimed = [
            "share:" + resource for resource in expected if result["decision"] == "ALLOW"
        ]
        receipt = result.get("receipt")
        receipt_hash = (
            hashlib.sha256(json.dumps(receipt, sort_keys=True).encode()).hexdigest()
            if receipt else None
        )
        event = {
            "event": "CASE", "case_id": case_id,
            "proposer": "synthetic-proposer",
            "authorizer": "gat-process",
            "executor": "pep-fixture-process",
            "verifier": "stranger-process",
            "request_id": proposal["request_id"],
            "proposal_hash": digest(proposal),
            "token_id": token.get("token_id") if token else None,
            "decision": result["decision"],
            "reason": result["reason"],
            "claimed_atoms": claimed,
            "observed_atoms": atoms,
            "observed_delta": delta,
            "observer_verdict": observed["verdict"],
            "gat_receipt_digest": receipt_hash,
        }
        appended = self.request(self.ledger_cli, {"op": "append", "body": event})
        self.assertTrue(appended["ok"], appended)
        self.assertEqual(result["decision"], expected_decision)
        self.assertEqual(observed["verdict"], "MATCH")
        if expected_decision == "DENY":
            self.assertEqual(delta, {}, "Denied action changed synthetic state")
        else:
            self.assertEqual(delta, proposal["expected_delta"])
        checked = self.audit()
        self.assertTrue(checked["valid"], checked)
        return result

    def test_01_valid_token_allows_one_synthetic_change(self):
        self.run_action("TC-01", self.proposal(), self.token(), "ALLOW")

    def test_02_expired_token_denied(self):
        self.run_action("TC-02", self.proposal(), self.token(expired=True), "DENY")

    def test_03_revoked_token_denied(self):
        tok = self.token()
        revoke = self.request(
            self.ledger_cli,
            {"op": "append", "body": {"event": "REVOKE", "token_id": tok["token_id"]}},
        )
        self.assertTrue(revoke["ok"])
        result = self.run_action("TC-03", self.proposal(), tok, "DENY")
        self.assertEqual(result["reason"], "DENY_REVOKED_OR_LEDGER_UNAVAILABLE")

    def test_04_out_of_scope_resource_denied(self):
        self.run_action("TC-04", self.proposal(resource="doc_C"),
                        self.token(resource="doc_C"), "DENY")

    def test_05_out_of_scope_operation_denied(self):
        self.run_action("TC-05", self.proposal(action="delete"),
                        self.token(action="delete"), "DENY")

    def test_06_out_of_scope_principal_denied(self):
        self.run_action(
            "TC-06", self.proposal(principal="wrong-principal"),
            self.token(principal="wrong-principal"), "DENY"
        )

    def test_07_forged_signature_denied(self):
        tok = self.token()
        tok["signature"] = "00" * 32
        result = self.run_action("TC-07", self.proposal(), tok, "DENY")
        self.assertEqual(result["reason"], "DENY_INVALID_SIGNATURE")

    def test_08_gate_unavailable_denied(self):
        self.processes["gat"].terminate()
        self.processes["gat"].join(timeout=2)
        result = self.run_action("TC-08", self.proposal(), self.token(), "DENY")
        self.assertEqual(result["reason"], "DENY_GAT_UNAVAILABLE")

    def test_09_tamper_damaged_copy_is_detected(self):
        self.run_action("TC-09", self.proposal(), self.token(), "ALLOW")
        damaged = Path(self.temp.name) / "damaged-copy.jsonl"
        shutil.copyfile(self.path, damaged)
        lines = damaged.read_text(encoding="utf-8").splitlines()
        altered = json.loads(lines[-1])
        altered["body"]["reason"] = "altered_in_disposable_copy"
        lines[-1] = json.dumps(altered, sort_keys=True, separators=(",", ":"))
        damaged.write_text("\n".join(lines) + "\n", encoding="utf-8")
        bad = self.audit(damaged)
        self.assertFalse(bad["valid"])
        self.assertEqual(bad["status"], "BROKEN_CHAIN")
        self.assertTrue(self.audit()["valid"])

    def test_10_simulated_bypass_hook_exits_without_effect(self):
        before = self.observe()
        worker = self.ctx.Process(target=jireh_trap)
        worker.start()
        worker.join(timeout=3)
        self.assertEqual(worker.exitcode, 73)
        self.assertEqual(before, self.observe())
        self.run_action("TC-10", self.proposal(), None, "DENY")

    def test_11_stale_memory_cannot_restore_expired_grant(self):
        proposal = self.proposal(note="remembered approval from earlier conversation")
        self.run_action("TC-11", proposal, self.token(expired=True), "DENY")

    def test_12_alternate_route_does_not_expand_scope(self):
        self.run_action(
            "TC-12a", self.proposal(resource="doc_C", note="try another resource"),
            self.token(resource="doc_A"), "DENY"
        )
        self.run_action(
            "TC-12b", self.proposal(action="export", note="alternative tool"),
            self.token(action="share"), "DENY"
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
