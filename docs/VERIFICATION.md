# Verification Strategy

## Evidence ladder

```
Architecture statement
    <
Policy decision
    <
Implementation observation
    <
Automated test
    <
Adversarial test
    <
Independent verification
    <
Reproducible evidence bundle
```

The project should publish the strongest claim supported by the available evidence—not the strongest claim desired.

## Local verification

Python reference tests:

```bash
python -m pytest -q
```

Adversarial boundary tests:

```bash
python -m pytest -q tests/adversarial
```

Example:

```bash
python examples/authorized_unauthorized.py
```

## Required evidence record

For a release candidate, preserve:

- commit SHA;
- environment/runtime versions;
- dependency versions;
- test commands;
- complete test output;
- fixture/policy version;
- timestamps;
- adversarial case identifiers;
- known failures and skipped tests.

## Independent verification

The verifier should not be the same component that:

- proposes the action;
- decides its authorization;
- performs the side effect;
- controls the only copy of the evidence.

For high-consequence deployments, independently reproduce the authorization decision and inspect pre/post state.

## Current evidence boundary

The repository currently provides implementation-level evidence for the Python reference evaluator and simulator.

It does not establish:

- production deployment correctness;
- universal security;
- complete integration mediation;
- immutable evidence;
- independent state attestation;
- concurrency-safe authorization consumption.
