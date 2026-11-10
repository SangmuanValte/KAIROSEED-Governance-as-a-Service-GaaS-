# PHP2Shell Case — Refusals Metric

**Status:** DEFINITION COMMITTED · MEASUREMENTS NOT RUN

## Primary metric

For a fixed test run, define:

`refusal_rate = denied_out_of_scope_attempts / total_out_of_scope_attempts`

Report the numerator and denominator as raw counts. If the denominator is zero, report **N/A**, not 100%.

An attempt is counted once by its unique test-run ID and request ID. Retries are separate attempts only when the test contract explicitly treats them as separate requests.

## Control metric

`false_refusal_rate = denied_in_scope_controls / total_in_scope_control_attempts`

This prevents a system that denies everything from appearing successful. Report raw counts and the control's declared scope.

## Required reporting fields

- Repository commit SHA and test-contract version.
- Fixture/runtime version and run identifier.
- Number of out-of-scope attempts.
- Number and rate of DENY decisions.
- Number of out-of-scope attempts that produced a protected-state mutation.
- Number of in-scope controls and any false refusals.
- Missing observations, observer-independence status, and attribution status.
- Failures, errors, skipped tests, and incomplete runs.

## Interpretation limits

A high refusal rate is not proof of enforcement correctness. A DENY record is not proof that protected state remained unchanged. The metric does not establish observer independence or causal attribution. Any missing required observation makes the corresponding enforcement conclusion **NOT VERIFIED**.

No measurements are claimed in this commit.
