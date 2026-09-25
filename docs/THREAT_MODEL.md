# KAIROSEED Threat Model

> **Boundary: this is a reference adapter, not proof of a production deployment.**

The following eight adversarial cases target the authorization-to-execution boundary.

| # | Attempt | Expected result |
|---|---|---|
| 1 | Missing claim | `BLOCKED: claim_not_found` |
| 2 | Revoked claim | `BLOCKED: claim_revoked` |
| 3 | Expired claim | `BLOCKED: claim_expired` |
| 4 | Subject substitution | `BLOCKED: policy_denied` |
| 5 | Action substitution | `BLOCKED: policy_denied` |
| 6 | Scope substitution | `BLOCKED: policy_denied` |
| 7 | Parameter substitution | `BLOCKED: params_hash_mismatch` |
| 8 | Single-use replay | `BLOCKED: claim_used` after successful consumption |

## 1. Missing claim

Submit an execution request with an unknown claim identifier.

Expected:

```
BLOCKED
reason = claim_not_found
```

## 2. Revoked claim

Change an active claim to `REVOKED`, then repeat the same request.

Expected:

```
BLOCKED
reason = claim_revoked
```

## 3. Expired claim

Use a claim whose expiration time has passed.

Expected:

```
BLOCKED
reason = claim_expired
```

## 4–6. Substitution attacks

Change the subject, action, or scope while keeping the authorization claim unchanged.

Expected:

```
BLOCKED
reason = policy_denied
```

## 7. Parameter substitution

Supply parameters whose deterministic SHA-256 differs from the claim's `paramsHash`.

Expected:

```
BLOCKED
reason = params_hash_mismatch
```

## 8. Single-use replay

A `singleUse` claim should transition to `USED` after successful execution.

A later attempt should be rejected.

**Concurrency warning:** the in-memory reference implementation does not atomically consume claims. Production implementations require transactional consumption or equivalent concurrency control.

## Out of scope

This fixture set is not exhaustive. Production threat models may additionally require controls for direct tool bypass, compromised identities, policy-service compromise, replay across workers, stale authorization, database privilege escalation, side channels, runtime compromise, serialization disagreement, and evidence-store compromise.
