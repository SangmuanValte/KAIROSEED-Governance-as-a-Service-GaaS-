# Verification Protocol — Research Draft

This protocol supports the [proof gates](PROOF_GATES.md). It is **not** evidence of completed independent verification.

## Pre-test

- Record exact claim set, revision, assumptions, scope and falsification criteria.
- Compute a commitment over canonical claim bytes **before** running tests.
- Record the commit and execution environment. Keep original claim versions intact.
- Identify the person or system responsible for observing protected effects.

## Test and observations

- Run only authorized tests against isolated, harmless fixtures.
- Preserve unedited raw outputs, including failures and environment details.
- Distinguish policy decisions, execution attempts, actual effects and final state.
- State which routes and effects were monitored and which were not.
- Explain any shared dependencies between the verifier and the component under assessment.

## Verdict

For each frozen claim, give **PASS within scope**, **FAIL**, or **NOT VERIFIED**, with links to raw evidence and a precisely stated observation window.

A success record is not automatically an independent attestation. A failure must remain visible even if a corrected claim is later tested.

## Release boundary

Verification does not authorize deployment. Keep production controls, legal approvals, accountable signoff and rollback requirements under a separate gate.

**Current status: NOT VERIFIED.** No real JIREH containment result, formal end-to-end guarantee or independent security certification is asserted.
