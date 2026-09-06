from governance_validator import GovernanceValidator


NOW = 1_800_000_000.0


def payload(**overrides):
    value = {
        "id": "incident-001",
        "source": "security-core-team",
        "action_type": "SANDBOX_ESCAPE",
        "timestamp": NOW,
        "blast_radius": "STAGING_RESOURCE_LEAK",
        "cryptographic_proof_hash": "abc123",
        "raw_log_uri": "evidence://incident-001",
    }
    value.update(overrides)
    return value


def test_verified_high_gravity_event():
    result = GovernanceValidator().calculate_incident_gravity(payload(), now=NOW)
    assert result.gravity_index == 0.7
    assert result.actionable is True
    assert result.verification_status == "VERIFIED"


def test_unverified_authority_cannot_be_actionable():
    result = GovernanceValidator().calculate_incident_gravity(
        payload(source="unknown-source"), now=NOW
    )
    assert result.gravity_index == 0.0
    assert result.actionable is False
    assert result.verification_status == "VERIFIED"


def test_missing_evidence_is_explicitly_unverified():
    result = GovernanceValidator().calculate_incident_gravity(
        payload(raw_log_uri=None), now=NOW
    )
    assert result.gravity_index == 0.0
    assert result.verification_status == "UNVERIFIED"


def test_future_timestamp_does_not_exceed_one():
    result = GovernanceValidator().calculate_incident_gravity(
        payload(timestamp=NOW + 3600), now=NOW
    )
    assert result.vector_breakdown["time"] == 1.0
