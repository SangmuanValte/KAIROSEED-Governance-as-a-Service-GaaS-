# KAIROSEED-Governance-as-a-Service-GaaS-

Governance-as-a-Service (GaaS): Define, enforce, and prove delegated authority for AI agents through executable policies, authorization, runtime governance, and verifiable audit trails.

## GaaS Safety Framework Foundation

`GaaS-Safety-Framework/Foundation/` contains reusable, reproducible governance-safety artifacts for agentic AI verification.

### Agent Circumvention Test

The Foundation defines a standardized test record for checking whether an agent respects a governance boundary after denial or constraint.

```text
INITIAL AUTHORITY
      ↓
OBJECTIVE → ACTION REQUEST
      ↓
GOVERNANCE DECISION
      ↓
AGENT RESPONSE / EXECUTION TRACE
      ↓
INTEGRITY CHECKS
      ↓
EVIDENCE → VERDICT
```

Core invariant:

> **Capability ≠ Permission.**

For denied actions:

`DENY → NO AUTHORIZATION → NO EXECUTION → EVIDENCE`

The Foundation artifact includes:

- `AGENT_CIRCUMVENTION_TEST.md` — normative test specification
- `agent-circumvention-test.schema.json` — machine-readable v1.0 record schema
- `examples/agent-circumvention-denied-001.json` — reproducible synthetic fixture

Threat classes include policy bypass, authority expansion, provenance manipulation, approval forgery, memory poisoning, audit bypass, cross-agent exploitation, and trusted-tool abuse.

A passing test does **not** establish universal security. It establishes only the properties exercised by the declared test, environment, policy version, and evidence.

## WebMCP prototype

`webmcp/` contains the **Automate.prototype** WebMCP challenge prototype. It demonstrates a strict separation between capability and permission:

```text
CAPABILITY → PROPOSAL → SCOPE → AUTHORIZATION → EXECUTION → EVIDENCE
```

The prototype exposes a progressive WebMCP `publish_artifact` capability when `navigator.modelContext` is available. The action remains fail-closed until authorization is explicitly granted, and each authorization/execution transition produces a small evidence record.

### Run locally

Serve the repository with any static HTTP server and open `webmcp/index.html` in a browser with WebMCP support enabled. The page also works as a governance simulation when WebMCP is unavailable.

### Invariant

> Capability does not imply permission. Authorization precedes execution. Execution produces evidence.
