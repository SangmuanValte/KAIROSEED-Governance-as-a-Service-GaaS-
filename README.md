# KAIROSEED-Governance-as-a-Service-GaaS-

Governance-as-a-Service (GaaS): Define, enforce, and prove delegated authority for AI agents through executable policies, authorization, runtime governance, and verifiable audit trails.

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
