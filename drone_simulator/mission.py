"""SCIИENTIA proposal -> ASTRA decision -> simulator execution."""
from __future__ import annotations
from typing import Any
from astra.core import ExecutionRequest, Policy, evaluate, decision_record, Decision
from .simulator import DroneSimulator

class GovernedDrone:
    def __init__(self, simulator: DroneSimulator, policy: Policy) -> None:
        self.simulator = simulator
        self.policy = policy

    def execute(self, *, actor: str, capability: str, action: str,
                requested_scope: dict[str, Any], vx: float = 0.0,
                vy: float = 0.0, vz: float = 0.0, dt: float = 0.1) -> dict[str, Any]:
        proposal = self.simulator.propose(action=action, vx=vx, vy=vy, vz=vz, dt=dt)
        request = ExecutionRequest(
            actor=actor, capability=capability, action=action,
            resource="drone://simulator", requested_scope=requested_scope,
            requested_resources={"speed": (vx * vx + vy * vy + vz * vz) ** 0.5},
        )
        decision, reasons = evaluate(request, self.policy)
        record = decision_record(
            request, decision, reasons,
            evidence={"proposal": proposal, "telemetry_before": self.simulator.telemetry()},
        )
        if decision is not Decision.ALLOW:
            return {"decision": decision.value, "record": record}
        telemetry = self.simulator.apply(proposal)
        record["evidence"]["telemetry_after"] = telemetry
        return {"decision": decision.value, "record": record, "telemetry": telemetry}
