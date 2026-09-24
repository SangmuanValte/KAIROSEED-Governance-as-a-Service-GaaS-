"""Deterministic bounded drone digital twin; no physical I/O."""
from __future__ import annotations
from dataclasses import dataclass, asdict
from math import sqrt
from typing import Any

@dataclass
class DroneState:
    x: float = 0.0
    y: float = 0.0
    z: float = 10.0
    vx: float = 0.0
    vy: float = 0.0
    vz: float = 0.0
    yaw: float = 0.0
    battery: float = 100.0
    armed: bool = False

class DroneSimulator:
    def __init__(self, *, max_speed: float = 20.0, max_altitude: float = 120.0) -> None:
        self.max_speed = max_speed
        self.max_altitude = max_altitude
        self.state = DroneState()

    def telemetry(self) -> dict[str, Any]:
        data = asdict(self.state)
        data["speed"] = sqrt(self.state.vx**2 + self.state.vy**2 + self.state.vz**2)
        return data

    def propose(self, *, action: str, vx: float = 0.0, vy: float = 0.0,
                vz: float = 0.0, yaw_rate: float = 0.0, dt: float = 0.1) -> dict[str, Any]:
        if dt <= 0 or dt > 1.0:
            raise ValueError("dt must be in (0, 1]")
        if self.state.battery <= 0:
            raise RuntimeError("battery_depleted")
        speed = sqrt(vx * vx + vy * vy + vz * vz)
        if speed > self.max_speed:
            raise ValueError("speed_limit_exceeded")
        next_z = self.state.z + vz * dt
        if next_z < 0 or next_z > self.max_altitude:
            raise ValueError("altitude_limit_exceeded")
        return {
            "action": action, "dt": dt,
            "velocity": {"vx": vx, "vy": vy, "vz": vz},
            "yaw_rate": yaw_rate,
            "predicted": {
                "x": self.state.x + vx * dt,
                "y": self.state.y + vy * dt,
                "z": next_z,
                "battery": max(0.0, self.state.battery - 0.08 * dt * (1.0 + speed / self.max_speed)),
            },
        }

    def apply(self, proposal: dict[str, Any]) -> dict[str, Any]:
        p, v = proposal["predicted"], proposal["velocity"]
        self.state.x, self.state.y, self.state.z = p["x"], p["y"], p["z"]
        self.state.vx, self.state.vy, self.state.vz = v["vx"], v["vy"], v["vz"]
        self.state.yaw += proposal["yaw_rate"] * proposal["dt"]
        self.state.battery = p["battery"]
        return self.telemetry()
