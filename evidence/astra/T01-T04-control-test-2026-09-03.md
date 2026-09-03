# ASTRA Control Test Evidence — T01–T04

**Date:** 2026-09-03
**Repository:** `SangmuanValte/KAIROSEED-Governance-as-a-Service-GaaS-`
**Target branch:** `main`
**Control under test:** Capability does not imply authorization; authorization is bounded by explicit capability/scope and bound to state version.

## Execution record

The executable test was run in an isolated local runtime before being committed to `main`.

Command executed:

```text
python /tmp/astra-test/test_control.py
```

Observed result:

```text
T01: PASS — denied before state change
T02: PASS — authorized bounded execution
T03: PASS — scope mismatch denied
T04: PASS — stale authorization denied
CONTROL_RESULT: PASS
```

## Test results

| Test | Control condition | Observation | Result |
|---|---|---|---|
| T01 | Capability unavailable to authority policy | Proposal denied; protected state remained unchanged | PASS |
| T02 | Explicit capability + matching scope | Bounded action executed and produced expected state | PASS |
| T03 | Scope differs from authorized scope | Proposal denied | PASS |
| T04 | Authorization receipt bound to old state version | Execution denied after state version changed | PASS |

## Integrity markers

- Test script SHA-256: `1674c08c49f156b3c499e1656679c004c91abfa7fedd293efc9ed55f01388b6f`
- Captured output SHA-256: `72ec5a883d6672790597d300ddacb4f33bdbb911c95a42d677c51eba784a5cc0`
- GitHub commit containing test script on `main`: `c6190cf62f76ee6415329cfb4a5c88a04029fce8`

## Interpretation boundary

This evidence supports the behavior of the four executable test cases in this reference control model. It does **not** establish production security, hardware attestation, universal agent/runtime protection, or effectiveness against a compromised execution environment.

The result is therefore recorded as:

**T01–T04 CONTROL TEST: PASS**

and not as a universal security guarantee.

## Governance rule preserved

`CLAIM → CONTROL → TEST → OBSERVE → AUDIT → EVIDENCE → RESULT CLAIM`

No additional authority is inferred from capability or test success.
