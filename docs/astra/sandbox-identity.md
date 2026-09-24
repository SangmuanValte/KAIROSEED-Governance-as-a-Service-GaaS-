# ASTRA Sandbox Identity

The sandbox identity is the machine-readable identity and bounded execution context for an ASTRA sandbox.

## Non-authority invariant

Sandbox identity does not grant consequential authority.

Sandbox Identity != Authority.
Capability != Authorization != Execution != Verification.

A sandbox may have technical capability or tool access while ASTRA independently denies consequential execution.

## 50-agent deployment profile

The initial fabric contains 50 logical sandbox identities: astra-sbx-0001 through astra-sbx-0050, paired with agent-0001 through agent-0050.

Each identity is independently scoped. No sandbox inherits authority merely because another sandbox is authorized.

## Lifecycle

CREATE -> INITIALIZE -> ACTIVE -> EXPIRE / REVOKE -> QUARANTINE / CLOSED

Expiration or revocation must invalidate the active execution lease and prevent crossing the consequence boundary.

## Governance relationship

SANDBOX -> ACTION PROPOSAL -> CONFLICT CHECK -> CONSTRAINT CHECK -> AUTHORIZATION -> CONSEQUENCE BOUNDARY -> EXECUTION -> VERIFICATION -> AUDIT

The sandbox is an execution substrate, not an authority source.

## Lineage

- parent_action_id links the sandbox to the action that created or delegated its execution context.
- correlation_id groups related agent, sandbox, policy, execution, and verification events.
- audit_id links the sandbox lifecycle to its evidence trail.

## Security properties

1. Fail closed when authority is absent, expired, or revoked.
2. Keep capability and authority independently represented.
3. Keep data and tool scopes explicit.
4. Bound compute and network resources.
5. Preserve action lineage.
6. Make revocation observable.
7. Require independent verification for consequential outcomes.
