from dataclasses import asdict, dataclass
from enum import Enum
from hashlib import sha256
import json
import sqlite3
import threading
import time
from pathlib import Path


class Decision(str, Enum):
    ALLOW = "ALLOW"
    ESCALATE = "ESCALATE"
    BLOCK = "BLOCK"


@dataclass(frozen=True)
class ActionProposal:
    agent_id: str
    intent: str
    authority_scope: str
    policy_version: str
    capability: bool = True
    validation_passed: bool = True


@dataclass(frozen=True)
class GovernanceDecision:
    decision: Decision
    reason: str
    proposal_hash: str
    evidence_initialized: bool


def _canonical(payload: dict) -> str:
    return json.dumps(payload, sort_keys=True, separators=(",", ":"))


def _record_hash(payload: dict) -> str:
    return sha256(_canonical(payload).encode()).hexdigest()


class EvidenceLedger:
    """Durable, hash-linked SQLite evidence ledger.

    The ledger serializes appends with a process-local lock and SQLite's
    transactional guarantees. It is tamper-evident, not tamper-proof: a
    privileged database operator can still alter storage outside this API.
    """

    def __init__(self, path: str | Path = ":memory:"):
        self.path = str(path)
        if self.path != ":memory:":
            Path(self.path).parent.mkdir(parents=True, exist_ok=True)
        self._lock = threading.RLock()
        self._conn = sqlite3.connect(
            self.path,
            check_same_thread=False,
            isolation_level=None,
        )
        self._conn.execute("PRAGMA foreign_keys = ON")
        self._conn.execute("PRAGMA busy_timeout = 5000")
        self._conn.execute("PRAGMA journal_mode = WAL")
        self._conn.execute(
            """
            CREATE TABLE IF NOT EXISTS evidence (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp REAL NOT NULL,
                proposal_json TEXT NOT NULL,
                decision TEXT NOT NULL,
                reason TEXT NOT NULL,
                previous_hash TEXT NOT NULL,
                record_hash TEXT NOT NULL UNIQUE
            )
            """
        )

    @property
    def records(self) -> list[dict]:
        with self._lock:
            rows = self._conn.execute(
                "SELECT timestamp, proposal_json, decision, reason, previous_hash, record_hash "
                "FROM evidence ORDER BY id"
            ).fetchall()
        return [
            {
                "timestamp": row[0],
                "proposal": json.loads(row[1]),
                "decision": row[2],
                "reason": row[3],
                "previous_hash": row[4],
                "record_hash": row[5],
            }
            for row in rows
        ]

    def append(self, proposal: ActionProposal, decision: Decision, reason: str) -> dict:
        with self._lock:
            self._conn.execute("BEGIN IMMEDIATE")
            try:
                previous_row = self._conn.execute(
                    "SELECT record_hash FROM evidence ORDER BY id DESC LIMIT 1"
                ).fetchone()
                previous = previous_row[0] if previous_row else "GENESIS"
                payload = {
                    "timestamp": time.time(),
                    "proposal": asdict(proposal),
                    "decision": decision.value,
                    "reason": reason,
                    "previous_hash": previous,
                }
                record = {**payload, "record_hash": _record_hash(payload)}
                self._conn.execute(
                    "INSERT INTO evidence "
                    "(timestamp, proposal_json, decision, reason, previous_hash, record_hash) "
                    "VALUES (?, ?, ?, ?, ?, ?)",
                    (
                        record["timestamp"],
                        _canonical(record["proposal"]),
                        record["decision"],
                        record["reason"],
                        record["previous_hash"],
                        record["record_hash"],
                    ),
                )
                self._conn.execute("COMMIT")
                return record
            except Exception:
                self._conn.execute("ROLLBACK")
                raise

    def verify_chain(self) -> bool:
        records = self.records
        previous = "GENESIS"
        for record in records:
            payload = {key: value for key, value in record.items() if key != "record_hash"}
            if record["previous_hash"] != previous:
                return False
            if _record_hash(payload) != record["record_hash"]:
                return False
            previous = record["record_hash"]
        return True

    def close(self) -> None:
        with self._lock:
            self._conn.close()


def proposal_hash(proposal: ActionProposal) -> str:
    return sha256(_canonical(asdict(proposal)).encode()).hexdigest()


def govern(proposal: ActionProposal, ledger: EvidenceLedger) -> GovernanceDecision:
    # Fail closed: every required predicate must pass before ALLOW.
    if not proposal.capability:
        decision, reason = Decision.BLOCK, "capability_missing"
    elif not proposal.intent.strip():
        decision, reason = Decision.BLOCK, "intent_missing"
    elif proposal.authority_scope != "authorized":
        decision, reason = Decision.BLOCK, "authority_invalid"
    elif proposal.policy_version != "v0.1":
        decision, reason = Decision.BLOCK, "unsupported_policy_version"
    elif not proposal.validation_passed:
        decision, reason = Decision.BLOCK, "validation_failed"
    else:
        decision, reason = Decision.ALLOW, "all_required_predicates_passed"

    record = ledger.append(proposal, decision, reason)
    return GovernanceDecision(
        decision=decision,
        reason=reason,
        proposal_hash=proposal_hash(proposal),
        evidence_initialized=bool(record),
    )
