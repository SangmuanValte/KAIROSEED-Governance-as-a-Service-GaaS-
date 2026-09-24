from astra.core import Policy
from drone_simulator.mission import GovernedDrone
from drone_simulator.simulator import DroneSimulator

policy = Policy(
    allowed_actions=frozenset({"takeoff", "move"}),
    allowed_capabilities=frozenset({"drone.flight"}),
    allowed_actors=frozenset({"scientia"}),
    allowed_resources=frozenset({"drone://simulator"}),
    authority_scope={"zone": "simulation"},
    resource_limits={"speed": 20.0},
)

drone = GovernedDrone(DroneSimulator(), policy)
print(drone.execute(
    actor="scientia", capability="drone.flight", action="move",
    requested_scope={"zone": "simulation"}, vx=4.0, vy=1.0,
))
