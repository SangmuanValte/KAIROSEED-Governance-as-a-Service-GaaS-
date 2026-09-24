from astra.core import Policy
from drone_simulator.mission import GovernedDrone
from drone_simulator.simulator import DroneSimulator

def policy():
    return Policy(
        allowed_actions=frozenset({"takeoff", "move"}),
        allowed_capabilities=frozenset({"drone.flight"}),
        allowed_actors=frozenset({"scientia"}),
        allowed_resources=frozenset({"drone://simulator"}),
        authority_scope={"zone": "simulation"},
        resource_limits={"speed": 20.0},
    )

def test_governed_move_allows_and_updates_state():
    result = GovernedDrone(DroneSimulator(), policy()).execute(
        actor="scientia", capability="drone.flight", action="move",
        requested_scope={"zone": "simulation"}, vx=5.0,
    )
    assert result["decision"] == "ALLOW"
    assert result["telemetry"]["x"] == 0.5

def test_scope_mismatch_blocks():
    result = GovernedDrone(DroneSimulator(), policy()).execute(
        actor="scientia", capability="drone.flight", action="move",
        requested_scope={"zone": "physical"}, vx=5.0,
    )
    assert result["decision"] == "BLOCK"
    assert result["record"]["evidence"]["telemetry_before"]["x"] == 0.0
