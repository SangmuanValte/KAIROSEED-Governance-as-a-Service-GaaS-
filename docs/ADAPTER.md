# KAIROSEED Adapter

> **Boundary: this is a reference adapter, not proof of a production deployment.**

## Purpose

`Kairoseed` wraps a consequential agent tool call with an authorization and execution boundary.

```
Agent → Kairoseed.exec()
      → ClaimStore
      → Policy
      → Execution Gate
      → Tool
      → EvidenceSink
```

Core distinction:

> **Capability ≠ Permission**

## ClaimStore

`ClaimStore` retrieves the authorization claim:

```ts
export interface ClaimStore {
  get(id: string): Promise<Claim | undefined> | Claim | undefined;
  save?(claim: Claim): Promise<void> | void;
}
```

The reference package provides `InMemoryClaimStore`. Production deployments should connect this interface to the authoritative authorization store.

### Single-use concurrency warning

The in-memory implementation does not provide atomic concurrent claim consumption. Two concurrent requests could observe the same active claim before either persists `USED`.

A production implementation should atomically consume or lease a single-use authorization using a transaction, row-level locking, or an equivalent concurrency control.

## EvidenceSink

```ts
export interface EvidenceSink {
  append(event: EvidenceEvent): Promise<void> | void;
}
```

The reference package provides `InMemoryEvidenceSink`. Production implementations should use an authoritative evidence store with appropriate access controls.

## Policy

`Policy.evaluate()` returns `ALLOW`, `DENY`, or `PAUSE`. The default policy binds policy version, subject, action, and scope.

## Fail-closed conditions

The reference adapter blocks when:

- claim is missing
- claim is not `ACTIVE`
- claim is expired
- `paramsHash` does not match
- subject does not match
- action does not match
- scope does not match
- policy version does not match
- policy returns `DENY` or `PAUSE`

A blocked request emits `BLOCKED` evidence and does not invoke the consequential tool callback.

## paramsHash binding

When a claim contains `paramsHash`, the adapter deterministically serializes request parameters and computes SHA-256. Execution is blocked when:

```
SHA256(request.params) != claim.paramsHash
```

Production systems should specify and share a canonical serialization format between authorization and execution components.

## Boundary

The consequential callback occurs only after the authorization checks:

```
authorization → policy → execution gate → tool
```

This is a reference implementation, not proof of a production deployment or universal security guarantee.
