# Contributing

## Development principle

KAIROSEED follows:

```
Design → Build → Verify → Publish
```

Contributions should make the authorization boundary clearer, more enforceable, or more verifiable.

## Pull requests

A useful PR should state:

- what changed;
- which security boundary changed;
- which invariant is affected;
- tests added or updated;
- known limitations;
- whether the change affects documented claims.

## Security-sensitive changes

Changes to authorization, execution gates, policy evaluation, evidence, identity binding, or replay/revocation behavior require adversarial tests.

A PR must not describe a planned control as implemented.

## Testing

Run:

```bash
python -m pytest -q
python -m pytest -q tests/adversarial
```

If a test cannot be run, record the reason and mark the result UNVERIFIED.

## Evidence discipline

When a test fails:

1. preserve the failure;
2. identify the boundary;
3. add or update a regression test;
4. fix the implementation;
5. rerun verification.

Do not replace evidence with a narrative claim.
