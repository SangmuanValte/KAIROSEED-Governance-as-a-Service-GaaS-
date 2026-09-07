"""Deterministic KAIROSEED governance scoring for observed agentic failures.

This module is observation-only: it never executes an external action.
"""

from __future__ import annotations

import time
from dataclasses import dataclass, asdict
from typing import Any, Dict, Mapping


DEFAULT_AUTHORITIES = {
    "@sys_evaluation_monitor",
    "security-core-team",
    "infra-gatekeeper-01",
}

ACTION_SCORES = {
    "SANDBOX_ESCAPE": 1.0,
    "UNAUTHORIZED_API_CALL": 0.8,
    "ENVIRONMENT_DRIFT": 0.5,
    "TELEMETRY_LOG": 0.1,
}

CONSEQUENCE_SCORES = {
    "CRITICAL_PRODUCTION_MUTATION": 1.0,
    "STAGING_RESOURCE_LEAK": 0.7,
    "EVAL_SUITE_INTERRUPTION": 0.3,
    "NONE": 0.0,
}


@dataclass(frozen=True)
class GravityResult:
    incident_id: str | None
    gravity_index: float
    actionable: bool
    verification_status: str
    vector_breakdown: Dict[str, float]


class GovernanceValidator:
    """Evaluate telemetry against fixed governance vectors.

    Formula: A_auth * A_act * T * C * E

    Time is bounded to [0.1, 1.0]. Evidence is intentionally binary in this
    MVP: both a proof hash and raw-log reference are required for E=1.
    """

    def __init__(self, verified_authorities: set[str] | None = None) -> None:
        self.verified_authorities = verified_authorities or set(DEFAULT_AUTHORITIES)

    @staticmethod
    def _time_score(event_time: float, now: float, window: float = 86400.0) -> float:
        delta = max(0.0, now - event_time)
        return max(0.1, min(1.0, 1.0 - (delta / window)))

    def calculate_incident_gravity(
        self,
        incident_payload: Mapping[str, Any],
        *,
        now: float | None = None,
    ) -> GravityResult:
        now = time.time() if now is None else now

        source = str(incident_payload.get("source", ""))
        authority = 1.0 if source in self.verified_authorities else 0.0

        action = ACTION_SCORES.get(
            str(incident_payload.get("action_type", "UNKNOWN")), 0.0
        )

        event_time = float(incident_payload.get("timestamp", now))
        temporal = self._time_score(event_time, now)

        consequence = CONSEQUENCE_SCORES.get(
            str(incident_payload.get("blast_radius", "NONE")), 0.0
        )

        has_hash = bool(incident_payload.get("cryptographic_proof_hash"))
        has_log_ref = bool(incident_payload.get("raw_log_uri"))
        evidence = 1.0 if has_hash and has_log_ref else 0.0

        gravity = authority * action * temporal * consequence * evidence
        verification = "VERIFIED" if evidence == 1.0 else "UNVERIFIED"

        return GravityResult(
            incident_id=incident_payload.get("id"),
            gravity_index=round(gravity, 4),
            actionable=gravity > 0.3,
            verification_status=verification,
            vector_breakdown={
                "authority": authority,
                "action": action,
                "time": round(temporal, 4),
                "consequence": consequence,
                "evidence": evidence,
            },
        )

    def as_dict(self, incident_payload: Mapping[str, Any], *, now: float | None = None) -> Dict[str, Any]:
        return asdict(self.calculate_incident_gravity(incident_payload, now=now))
