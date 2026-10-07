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


@dataclass(frozen=True)
class PersistenceReceipt:
    trace_id: str
    decision: Decision
    claim_atoms: tuple[str, ...]
    supported_claim_atoms: tuple[str, ...]
    evidence_scope_atoms: tuple[str, ...]
    authorized_scope_atoms: tuple[str, ...]
    evidence_digest: str
    policy_digest: str


@dataclass(frozen=True)
class PersistenceResult:
    persisted: bool
    reason: str
    receipt_hash: str | None = None


class PersistenceStore:
    """Canonical persistence boundary for the reference prototype.

    Governance/execution and persistence are intentionally separate. Canonical
    state is appended only when the storage layer itself admits the receipt:
    decision == ALLOW, C subset E, and evidence scope subset S_auth.

    This reference implementation does not claim TPM-backed signing,
    tamper-proof storage, or production certification.
    """

    def __init__(self, path: str | Path):
        self.path = str(path)
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
        self._conn.executescript(
            """
            CREATE TABLE IF NOT EXISTS persistence (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                idempotency_key TEXT NOT NULL UNIQUE,
                payload_json TEXT NOT NULL CHECK (json_valid(payload_json)),
                trace_id TEXT NOT NULL,
                decision TEXT NOT NULL CHECK (decision = 'ALLOW'),
                claim_atoms_json TEXT NOT NULL CHECK (json_valid(claim_atoms_json)),
                supported_claim_atoms_json TEXT NOT NULL CHECK (json_valid(supported_claim_atoms_json)),
                evidence_scope_atoms_json TEXT NOT NULL CHECK (json_valid(evidence_scope_atoms_json)),
                authorized_scope_atoms_json TEXT NOT NULL CHECK (json_valid(authorized_scope_atoms_json)),
                evidence_digest TEXT NOT NULL,
                policy_digest TEXT NOT NULL,
                receipt_hash TEXT NOT NULL UNIQUE
            );

            CREATE TRIGGER IF NOT EXISTS persistence_claim_evidence_guard
            BEFORE INSERT ON persistence
            WHEN EXISTS (
                SELECT 1
                FROM json_each(NEW.claim_atoms_json) AS claim
                WHERE NOT EXISTS (
                    SELECT 1
                    FROM json_each(NEW.supported_claim_atoms_json) AS supported
                    WHERE supported.value = claim.value
                )
            )
            BEGIN
                SELECT RAISE(ABORT, 'CLAIM_WITHOUT_EVIDENCE');
            END;

            CREATE TRIGGER IF NOT EXISTS persistence_evidence_scope_guard
            BEFORE INSERT ON persistence
            WHEN EXISTS (
                SELECT 1
                FROM json_each(NEW.evidence_scope_atoms_json) AS evidence_scope
                WHERE NOT EXISTS (
                    SELECT 1
                    FROM json_each(NEW.authorized_scope_atoms_json) AS authorized_scope
                    WHERE authorized_scope.value = evidence_scope.value
                )
            )
            BEGIN
                SELECT RAISE(ABORT, 'EVIDENCE_OUTSIDE_SCOPE');
            END;
            """
        )

    def persist(
        self,
        *,
        idempotency_key: str,
        payload: dict,
        receipt: PersistenceReceipt,
    ) -> PersistenceResult:
        receipt_payload = {
            "trace_id": receipt.trace_id,
            "decision": receipt.decision.value,
            "claim_atoms": list(receipt.claim_atoms),
            "supported_claim_atoms": list(receipt.supported_claim_atoms),
            "evidence_scope_atoms": list(receipt.evidence_scope_atoms),
            "authorized_scope_atoms": list(receipt.authorized_scope_atoms),
            "evidence_digest": receipt.evidence_digest,
            "policy_digest": receipt.policy_digest,
        }
        receipt_hash = _record_hash(
            {
                "idempotency_key": idempotency_key,
                "payload": payload,
                "receipt": receipt_payload,
            }
        )

        with self._lock:
            self._conn.execute("BEGIN IMMEDIATE")
            try:
                cursor = self._conn.execute(
                    """
                    INSERT INTO persistence (
                        idempotency_key,
                        payload_json,
                        trace_id,
                        decision,
                        claim_atoms_json,
                        supported_claim_atoms_json,
                        evidence_scope_atoms_json,
                        authorized_scope_atoms_json,
                        evidence_digest,
                        policy_digest,
                        receipt_hash
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ON CONFLICT(idempotency_key) DO NOTHING
                    """,
                    (
                        idempotency_key,
                        _canonical(payload),
                        receipt.trace_id,
                        receipt.decision.value,
                        _canonical(list(receipt.claim_atoms)),
                        _canonical(list(receipt.supported_claim_atoms)),
                        _canonical(list(receipt.evidence_scope_atoms)),
                        _canonical(list(receipt.authorized_scope_atoms)),
                        receipt.evidence_digest,
                        receipt.policy_digest,
                        receipt_hash,
                    ),
                )
                self._conn.execute("COMMIT")
                if cursor.rowcount == 0:
                    return PersistenceResult(False, "idempotent_duplicate")
                return PersistenceResult(True, "persisted", receipt_hash)
            except sqlite3.IntegrityError as error:
                self._conn.execute("ROLLBACK")
                return PersistenceResult(False, str(error))

    def count(self) -> int:
        with self._lock:
            return int(
                self._conn.execute("SELECT COUNT(*) FROM persistence").fetchone()[0]
            )

    def close(self) -> None:
        with self._lock:
            self._conn.close()
