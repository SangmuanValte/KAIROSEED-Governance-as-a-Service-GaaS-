# ASTRA Execution Gate v1

A minimal reference implementation of the ASTRA invariant:

> Capability ≠ Permission. Authorization precedes consequential execution.

The gate evaluates an ExecutionRequest against an explicit Policy and returns:

- ALLOW — inside the current authorization envelope.
- BLOCK — one or more mandatory constraints fail.
- REVIEW — additional approval is required.

Every decision can be converted into an audit record containing actor, capability, action, requested scope, decision, reasons, correlation identifiers, result, evidence, and timestamp.

The gate is policy evaluation only. A separate runtime executor must enforce the decision immediately before the side effect and emit evidence after execution.
