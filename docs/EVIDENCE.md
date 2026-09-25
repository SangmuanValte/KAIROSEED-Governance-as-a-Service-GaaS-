# KAIROSEED Evidence

> **Boundary: this is a reference adapter, not proof of a production deployment.**

## Event schema

```ts
interface EvidenceEvent {
  id: string;
  timestamp: number;
  event: "BLOCKED" | "EXECUTED" | "VERIFICATION";
  subject: string;
  action: string;
  scope: string;
  claimId: string;
  decision: "ALLOW" | "DENY" | "PAUSE";
  reason?: string;
  resultHash?: string;
}
```

## Event types

### BLOCKED

Authorization or policy checks rejected the request.

Typical reasons include:

- `claim_not_found`
- `claim_revoked`
- `claim_used`
- `claim_expired`
- `params_hash_mismatch`
- `policy_denied`
- `policy_pause`

The reference adapter does not invoke the tool callback for a blocked request.

### EXECUTED

Authorization allowed the request and the consequential callback completed. The reference adapter records a SHA-256 hash of the serialized result.

### VERIFICATION

The reference adapter uses this event for post-execution/tool-error evidence. It is an evidence record, not a formal proof event.

## Independent observer procedure

An observer should verify the execution chain independently:

1. Identify the authorization record.
2. Verify subject, action, and scope.
3. Verify expiry and authorization state.
4. Verify policy version.
5. Verify parameter binding when present.
6. Inspect the execution record.
7. Inspect the evidence event.
8. Confirm that blocked requests did not invoke the tool.

For production deployments, preserve raw records, implementation version, migration version, fixture version, timestamps, and relevant logs.

## Evidence boundary

Evidence demonstrates what the inspected system recorded. It does not automatically prove that no other execution path, side channel, infrastructure compromise, or untested input existed.

A passing experiment is evidence under defined conditions, not a universal security guarantee.
