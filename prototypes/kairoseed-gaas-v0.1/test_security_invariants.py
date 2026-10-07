import json
from hashlib import sha256
import sqlite3
import tempfile
from concurrent.futures import ThreadPoolExecutor

from kairoseed_gaas import (
    ActionProposal,
    Decision,
    EvidenceLedger,
    PersistenceReceipt,
    PersistenceStore,
    govern,
    proposal_hash,
)


def test_capability_is_fail_closed():
    ledger = EvidenceLedger()
    result = govern(
        ActionProposal("agent-1", "read_report", "authorized", "v0.1", capability=False),
        ledger,
    )
    assert result.decision is Decision.BLOCK
    assert result.reason == "capability_missing"


def test_empty_intent_is_fail_closed():
    ledger = EvidenceLedger()
    result = govern(ActionProposal("agent-1", "   ", "authorized", "v0.1"), ledger)
    assert result.decision is Decision.BLOCK
    assert result.reason == "intent_missing"


def test_allow_requires_all_required_predicates():
    baseline = ActionProposal("agent-1", "read_report", "authorized", "v0.1")
    predicates = [
        ActionProposal("agent-1", "read_report", "authorized", "v0.1", capability=False),
        ActionProposal("agent-1", "", "authorized", "v0.1"),
        ActionProposal("agent-1", "read_report", "unauthorized", "v0.1"),
        ActionProposal("agent-1", "read_report", "authorized", "unsupported"),
        ActionProposal("agent-1", "read_report", "authorized", "v0.1", validation_passed=False),
    ]

    assert govern(baseline, EvidenceLedger()).decision is Decision.ALLOW
    for proposal in predicates:
        assert govern(proposal, EvidenceLedger()).decision is Decision.BLOCK


def test_proposal_hash_is_deterministic():
    proposal = ActionProposal("agent-1", "read_report", "authorized", "v0.1")
    assert proposal_hash(proposal) == proposal_hash(proposal)


def test_evidence_record_hash_reconstructs():
    ledger = EvidenceLedger()
    proposal = ActionProposal("agent-1", "read_report", "authorized", "v0.1")
    govern(proposal, ledger)
    record = ledger.records[0]

    payload = {key: value for key, value in record.items() if key != "record_hash"}
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    expected = sha256(canonical.encode()).hexdigest()
    assert record["record_hash"] == expected


def test_evidence_chain_detects_modified_persisted_record():
    with tempfile.TemporaryDirectory() as directory:
        path = f"{directory}/tamper.sqlite3"
        ledger = EvidenceLedger(path)
        proposal = ActionProposal("agent-1", "read_report", "authorized", "v0.1")
        govern(proposal, ledger)
        govern(proposal, ledger)

        original_hash = ledger.records[0]["record_hash"]
        ledger.close()

        attacker = sqlite3.connect(path)
        attacker.execute("UPDATE evidence SET reason = ? WHERE id = 1", ("tampered",))
        attacker.commit()
        attacker.close()

        reopened = EvidenceLedger(path)
        assert not reopened.verify_chain()
        assert reopened.records[1]["previous_hash"] == original_hash
        reopened.close()


def test_concurrent_governance_preserves_chain():
    with tempfile.TemporaryDirectory() as directory:
        ledger = EvidenceLedger(f"{directory}/concurrency.sqlite3")
        proposals = [
            ActionProposal(f"agent-{index}", "read_report", "authorized", "v0.1")
            for index in range(32)
        ]
        with ThreadPoolExecutor(max_workers=8) as pool:
            results = list(pool.map(lambda proposal: govern(proposal, ledger), proposals))

        assert all(result.decision is Decision.ALLOW for result in results)
        assert len(ledger.records) == 32
        assert ledger.verify_chain()
        ledger.close()


def test_blocked_actions_also_produce_durable_evidence():
    with tempfile.TemporaryDirectory() as directory:
        path = f"{directory}/blocked.sqlite3"
        ledger = EvidenceLedger(path)
        result = govern(ActionProposal("agent-1", "send_message", "unauthorized", "v0.1"), ledger)
        assert result.decision is Decision.BLOCK
        assert len(ledger.records) == 1
        ledger.close()

        reopened = EvidenceLedger(path)
        assert reopened.records[0]["decision"] == Decision.BLOCK.value
        assert reopened.verify_chain()
        reopened.close()


def _persistence_receipt(
    decision=Decision.ALLOW,
    claims=("claim:read",),
    supported=("claim:read",),
    evidence_scope=("resource:report",),
    authorized_scope=("resource:report",),
):
    return PersistenceReceipt(
        trace_id="trace-1",
        decision=decision,
        claim_atoms=claims,
        supported_claim_atoms=supported,
        evidence_scope_atoms=evidence_scope,
        authorized_scope_atoms=authorized_scope,
        evidence_digest="ev-digest",
        policy_digest="policy-digest",
    )


def test_allow_decision_does_not_persist_implicitly():
    with tempfile.TemporaryDirectory() as directory:
        ledger = EvidenceLedger(f"{directory}/evidence.sqlite3")
        store = PersistenceStore(f"{directory}/canonical.sqlite3")

        result = govern(
            ActionProposal("agent-1", "read_report", "authorized", "v0.1"),
            ledger,
        )

        assert result.decision is Decision.ALLOW
        assert store.count() == 0

        persisted = store.persist(
            idempotency_key="idem-1",
            payload={"reflection": "ok"},
            receipt=_persistence_receipt(),
        )

        assert persisted.persisted
        assert store.count() == 1
        ledger.close()
        store.close()


def test_database_gate_blocks_non_allow_persistence():
    with tempfile.TemporaryDirectory() as directory:
        store = PersistenceStore(f"{directory}/canonical.sqlite3")
        result = store.persist(
            idempotency_key="idem-block",
            payload={"reflection": "blocked"},
            receipt=_persistence_receipt(decision=Decision.BLOCK),
        )

        assert not result.persisted
        assert store.count() == 0
        store.close()


def test_database_gate_enforces_claim_evidence_relation():
    with tempfile.TemporaryDirectory() as directory:
        store = PersistenceStore(f"{directory}/canonical.sqlite3")
        result = store.persist(
            idempotency_key="idem-claim",
            payload={"reflection": "unsupported claim"},
            receipt=_persistence_receipt(
                claims=("claim:read",),
                supported=(),
            ),
        )

        assert not result.persisted
        assert "CLAIM_WITHOUT_EVIDENCE" in result.reason
        assert store.count() == 0
        store.close()


def test_database_gate_enforces_evidence_scope_relation():
    with tempfile.TemporaryDirectory() as directory:
        store = PersistenceStore(f"{directory}/canonical.sqlite3")
        result = store.persist(
            idempotency_key="idem-scope",
            payload={"reflection": "outside scope"},
            receipt=_persistence_receipt(
                evidence_scope=("resource:secret",),
                authorized_scope=("resource:report",),
            ),
        )

        assert not result.persisted
        assert "EVIDENCE_OUTSIDE_SCOPE" in result.reason
        assert store.count() == 0
        store.close()


def test_direct_sql_bypass_is_blocked_by_storage_trigger():
    with tempfile.TemporaryDirectory() as directory:
        path = f"{directory}/canonical.sqlite3"
        store = PersistenceStore(path)
        store.close()

        connection = sqlite3.connect(path)
        try:
            with connection:
                connection.execute(
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
                    """,
                    (
                        "direct-bypass",
                        '{"reflection":"attempt"}',
                        "trace-direct",
                        "ALLOW",
                        '["claim:read"]',
                        '[]',
                        '["resource:report"]',
                        '["resource:report"]',
                        "ev",
                        "policy",
                        "hash-direct",
                    ),
                )
            raise AssertionError("direct SQL bypass unexpectedly persisted")
        except sqlite3.IntegrityError as error:
            assert "CLAIM_WITHOUT_EVIDENCE" in str(error)
        finally:
            connection.close()


def test_parallel_idempotent_persistence_writes_once():
    with tempfile.TemporaryDirectory() as directory:
        path = f"{directory}/canonical.sqlite3"

        def attempt(_index):
            store = PersistenceStore(path)
            try:
                return store.persist(
                    idempotency_key="same-key",
                    payload={"reflection": "ok"},
                    receipt=_persistence_receipt(),
                )
            finally:
                store.close()

        with ThreadPoolExecutor(max_workers=10) as pool:
            results = list(pool.map(attempt, range(10)))

        verifier = PersistenceStore(path)
        assert verifier.count() == 1
        assert sum(result.persisted for result in results) == 1
        verifier.close()
