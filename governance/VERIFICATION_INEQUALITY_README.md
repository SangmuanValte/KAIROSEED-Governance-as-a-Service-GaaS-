# Verification Inequality v0.1 — Engineering Boundary

Canonical invariant:

`C ⊆ E ⊆ S_auth`

This implementation deliberately separates validation layers:

1. `VERIFICATION_INEQUALITY_v0.1.json` — machine-readable architectural registry.
2. `govana_core.rego` — pre-execution epoch and evidence-scope policy.
3. `jireh_ebpf.yaml` — runtime adapter specification; **not yet an eBPF implementation**.
4. `formal/verification.lean` — abstract inclusion and stale-epoch proofs.
5. `tests/injection_tests.py` — deterministic staging model.

## Commands

`lake build` typechecks the abstract Lean model. It does **not** execute Python
injection tests or prove runtime implementation correctness.

Run deterministic staging tests separately:

```bash
python -m unittest tests/injection_tests.py -v
```

A CI workflow may require both commands before merge or deploy.

## Evidence boundary

Passing the Lean model establishes only the theorems encoded in that model.
Passing the Python tests establishes only the tested deterministic policy
behavior.

Neither establishes:

- eBPF implementation correctness,
- OPA engine correctness,
- TPM authenticity,
- sub-millisecond detection,
- absence of hidden execution,
- universal safety.

Those require separate implementation and empirical evidence consistent with
`Claim ≤ Evidence ≤ Established Scope`.
