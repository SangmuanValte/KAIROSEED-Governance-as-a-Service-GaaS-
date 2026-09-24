# Drone Simulator + ASTRA

This module is a bounded digital-twin execution environment for autonomous
drone experimentation.

SCIИENTIA proposes and predicts. ASTRA evaluates delegated authority.
Only an ASTRA ALLOW decision can mutate simulator state.

Resource identity:
- drone://simulator = simulated execution only
- future physical adapters must use a separate resource and policy scope

Flow:

WORLD -> SCIИENTIA -> UNDERSTANDING -> PREDICTION -> PROPOSAL
-> ASTRA GOVERNOR -> AUTHORIZATION -> SIMULATOR ACTION -> EVIDENCE

Safety properties:
- Fail closed on unauthorized actor, capability, action, resource, scope, or limit.
- No physical I/O exists in this simulator.
- Speed and altitude are bounded.
- Governed actions emit decision records.
- Simulation authorization does not imply physical authorization.
