"""SCIИENTIA proposal -> ASTRA decision -> simulator execution.

This module is simulation-only. It does not connect to physical flight hardware.
"""
from __future__ import annotations

from typing import Any, Iterable, Mapping

from astra.core import Decision, ExecutionRequest, Policy, decision_record, evaluate
from .simulator import DroneSimulator


class GovernedDrone:
    """Execute individual simulator actions through the ASTRA authorization gate."""

    def __init__(self, simulator: DroneSimulator, policy: Policy) -> None:
        self.simulator = simulator
        self.policy = policy

    def execute(
        self,
        *,
        actor: str,
        capability: str,
        action: str,
        requested_scope: Mapping[str, Any],
        vx: float = 0.0,
        vy: float = 0.0,
        vz: float = 0.0,
        dt: float = 0.1,
        purpose: str | None = None,
    ) -> dict[str, Any]:
        telemetry_before = self.simulator.telemetry()
        proposal = self.simulator.propose(
            action=action, vx=vx, vy=vy, vz=vz, dt=dt
        )
        request = ExecutionRequest(
            actor=actor,
            capability=capability,
            action=action,
            resource="drone://simulator",
            requested_scope=requested_scope,
            requested_resources={
                "speed": (vx * vx + vy * vy + vz * vz) ** 0.5
            },
            purpose=purpose,
        )
        decision, reasons = evaluate(request, self.policy)
        record = decision_record(
            request,
            decision,
            reasons,
            evidence={
                "proposal": proposal,
                "telemetry_before": telemetry_before,
            },
        )
        if decision is not Decision.ALLOW:
            return {"decision": decision.value, "record": record}

        telemetry_after = self.simulator.apply(proposal)
        record["evidence"]["telemetry_after"] = telemetry_after
        return {
            "decision": decision.value,
            "record": record,
            "telemetry": telemetry_after,
        }


def run_governed_mission(
    *,
    mission: Iterable[Mapping[str, Any]],
    simulator: DroneSimulator,
    policy: Policy,
    actor: str = "scientia",
    capability: str = "drone.flight",
    requested_scope: Mapping[str, Any] | None = None,
    purpose: str = "simulation_mission",
) -> dict[str, Any]:
    """Run a proposed mission one authorized action at a time.

    Every step passes through ASTRA. Execution stops on BLOCK or REVIEW.
    The result contains the complete evidence trail and final telemetry.
    """
    scope = dict(requested_scope or {"zone": "simulation"})
    steps: list[dict[str, Any]] = []
    status = "COMPLETED"

    for index, command in enumerate(mission):
        action = str(command.get("action", ""))
        if not action:
            raise ValueError(f"mission step {index} is missing 'action'")

        result = GovernedDrone(simulator, policy).execute(
            actor=actor,
            capability=capability,
            action=action,
            requested_scope=scope,
            vx=float(command.get("vx", 0.0)),
            vy=float(command.get("vy", 0.0)),
            vz=float(command.get("vz", 0.0)),
            dt=float(command.get("dt", 0.1)),
            purpose=purpose,
        )
        step = {
            "index": index,
            "command": dict(command),
            "decision": result["decision"],
            "record": result["record"],
        }
        if "telemetry" in result:
            step["telemetry"] = result["telemetry"]
        steps.append(step)

        if result["decision"] != Decision.ALLOW.value:
            status = "BLOCKED" if result["decision"] == Decision.BLOCK.value else "REVIEW_REQUIRED"
            break

    return {
        "status": status,
        "steps_executed": len(steps),
        "steps": steps,
        "final_telemetry": simulator.telemetry(),
        "simulation_only": True,
    }
