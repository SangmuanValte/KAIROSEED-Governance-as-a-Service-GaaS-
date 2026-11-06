"""Phase 0 synthetic JSONL ledger service.

Append-only at the application API, hash-chained for accidental/partial tampering.
This is NOT immutable WORM storage and cannot prevent privileged rewriting.
"""
from __future__ import annotations

from hashlib import sha256
import json
import os
from pathlib import Path
import time
from multiprocessing.connection import wait


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def record_hash(previous_hash, body):
    return sha256((previous_hash + "|" + canonical(body)).encode("utf-8")).hexdigest()


class LedgerError(Exception):
    pass


class Ledger:
    def __init__(self, filename):
        self.path = Path(filename)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.touch(mode=0o600, exist_ok=True)

    def records(self):
        raw = self.path.read_bytes()
        if raw and not raw.endswith(b"\n"):
            raise LedgerError("TORN_RECORD")
        records = []
        for number, line in enumerate(raw.splitlines(), start=1):
            if not line:
                raise LedgerError("BLANK_RECORD")
            try:
                record = json.loads(line)
            except (ValueError, UnicodeError) as exc:
                raise LedgerError(f"INVALID_JSON:{number}") from exc
            records.append(record)
        return records

    def verify_chain(self):
        try:
            previous = "GENESIS"
            for index, record in enumerate(self.records(), start=1):
                if not isinstance(record, dict) or set(record) != {"sequence", "previous_hash", "body", "record_hash"}:
                    return False
                if record["sequence"] != index or record["previous_hash"] != previous:
                    return False
                if not isinstance(record["body"], dict):
                    return False
                expected = record_hash(previous, record["body"])
                if record["record_hash"] != expected:
                    return False
                previous = expected
            return True
        except (LedgerError, KeyError, TypeError, ValueError):
            return False

    def append(self, body):
        if not isinstance(body, dict):
            raise LedgerError("INVALID_EVENT")
        if not self.verify_chain():
            raise LedgerError("BROKEN_CHAIN")
        records = self.records()
        prior = records[-1]["record_hash"] if records else "GENESIS"
        item = {"sequence": len(records) + 1, "previous_hash": prior,
                "body": {**body, "recorded_ns": time.time_ns()}}
        item["record_hash"] = record_hash(prior, item["body"])
        # Only this service writes in Phase 0. O_APPEND is not a WORM guarantee.
        with self.path.open("a", encoding="utf-8") as output:
            output.write(canonical(item) + "\n")
            output.flush()
            os.fsync(output.fileno())
        return item

    def query_revoked(self, token_id):
        if not self.verify_chain():
            raise LedgerError("BROKEN_CHAIN")
        return any(
            x["body"].get("event") == "REVOKE" and x["body"].get("token_id") == token_id
            for x in self.records()
        )


def ledger_worker(control, gat_query, filename):
    """Ledger process, not an executor. GAT only receives query capability."""
    ledger = Ledger(filename)
    channels = {control: "control", gat_query: "gat"}
    while channels:
        ready = wait(list(channels))
        for conn in ready:
            try:
                request = conn.recv()
            except EOFError:
                channels.pop(conn, None)
                continue
            try:
                op = request.get("op")
                if op == "query_revoked":
                    result = {"ok": True, "revoked": ledger.query_revoked(request["token_id"])}
                elif channels[conn] == "control" and op == "append":
                    result = {"ok": True, "record": ledger.append(request["body"])}
                elif channels[conn] == "control" and op == "verify":
                    result = {"ok": True, "valid": ledger.verify_chain()}
                elif channels[conn] == "control" and op == "stop":
                    conn.send({"ok": True})
                    return
                else:
                    result = {"ok": False, "error": "NOT_AUTHORIZED_FOR_CHANNEL"}
            except (LedgerError, KeyError, AttributeError, TypeError, ValueError) as exc:
                result = {"ok": False, "error": str(exc)}
            try:
                conn.send(result)
            except (BrokenPipeError, EOFError, OSError):
                channels.pop(conn, None)
