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

## ASTRA production prototype

The main application is an ASTRA Agent Governance control-plane prototype. It demonstrates the governed action path: agent → tool request → policy evaluation → ALLOW / DENY / APPROVAL_REQUIRED → evidence.

The prototype includes an authorization API at `POST /api/v1/authorize`, an agent registry, fail-closed policy evaluation, evidence trace, and authority revocation UI. It is simulation-safe and does not execute external production actions.


### Grok Bot integration

ASTRA now exposes a governed Grok Bot adapter at `POST /api/v1/grok/send`.

The integration keeps Grok Bot behind the ASTRA authorization boundary:

```text
GROK REQUEST
    ↓
ASTRA IDENTITY / POLICY / RISK
    ↓
ALLOW / DENY / APPROVAL_REQUIRED
    ↓
GROK BOT GATEWAY
    ↓
DELIVERY EVIDENCE
```

The adapter supports `agent-grok` with `grok_message` and `grok_thread` capabilities. Production execution is approval-gated. Missing Grok gateway credentials fail closed; an uncertain delivery is never silently retried.

Configure only server-side environment variables:

- `GROK_BOT_GATEWAY_URL`
- `GROK_BOT_GATEWAY_TOKEN`

The gateway token is never returned to the client.

The upstream `grok-bot-cli` project provides the `gbot` CLI and Grok Bot gateway integration, including `sendPrompt` and delivery receipts. ASTRA treats that capability as an execution target rather than an authority source.
