from astra.core import Policy
from drone_simulator.mission import GovernedDrone, run_governed_mission
from drone_simulator.simulator import DroneSimulator


def policy():
    return Policy(
        allowed_actions=frozenset({"takeoff", "move", "hold", "land"}),
        allowed_capabilities=frozenset({"drone.flight"}),
        allowed_actors=frozenset({"scientia"}),
        allowed_resources=frozenset({"drone://simulator"}),
        authority_scope={"zone": "simulation"},
        resource_limits={"speed": 20.0},
    )


def test_governed_move_allows_and_updates_state():
    result = GovernedDrone(DroneSimulator(), policy()).execute(
        actor="scientia",
        capability="drone.flight",
        action="move",
        requested_scope={"zone": "simulation"},
        vx=5.0,
    )
    assert result["decision"] == "ALLOW"
    assert result["telemetry"]["x"] == 0.5


def test_scope_mismatch_blocks():
    result = GovernedDrone(DroneSimulator(), policy()).execute(
        actor="scientia",
        capability="drone.flight",
        action="move",
        requested_scope={"zone": "physical"},
        vx=5.0,
    )
    assert result["decision"] == "BLOCK"
    assert result["record"]["evidence"]["telemetry_before"]["x"] == 0.0


def test_run_governed_mission_completes_and_records_evidence():
    simulator = DroneSimulator()
    result = run_governed_mission(
        mission=[
            {"action": "takeoff", "vz": 1.0, "dt": 1.0},
            {"action": "move", "vx": 5.0, "dt": 1.0},
            {"action": "hold", "dt": 1.0},
            {"action": "land", "vz": -1.0, "dt": 1.0},
        ],
        simulator=simulator,
        policy=policy(),
    )
    assert result["status"] == "COMPLETED"
    assert result["steps_executed"] == 4
    assert len(result["steps"]) == 4
    assert result["simulation_only"] is True
    assert result["final_telemetry"]["x"] == 5.0


def test_run_governed_mission_stops_on_scope_violation():
    simulator = DroneSimulator()
    result = run_governed_mission(
        mission=[
            {"action": "move", "vx": 5.0, "dt": 1.0},
        ],
        simulator=simulator,
        policy=policy(),
        requested_scope={"zone": "physical"},
    )
    assert result["status"] == "BLOCKED"
    assert result["steps_executed"] == 1
    assert result["final_telemetry"]["x"] == 0.0
