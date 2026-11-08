# Independent Containment & Observation Falsification Matrix v1.0

**Classification:** Non-canonical research test contract.  
**Status:** Pre-test snapshot for future isolated synthetic-fixture runs.  
**Canonical specification:** FROZEN — UNCHANGED.  
**Assurance status:** NOT VERIFIED.  
**Production/deployment authorization:** NOT GRANTED.

## Purpose

This matrix converts the ten minimum scenarios proposed in Issue #30 into explicit test obligations. It is a bounded falsification plan, not evidence that any scenario has been executed or passed. The matrix must be treated as frozen for a given run: any change to scenario definitions, expected outcomes, resource scope, or closure criteria creates a successor version and must not silently replace this snapshot.

## Shared test boundary

All runs must use owned, isolated synthetic fixtures and harmless protected resources. No production assets or third-party systems are in scope. Before execution, record the exact repository commit, harness and verifier versions, dependency lock, environment, protected-resource inventory, effect inventory, actor identities, policy/grant version, revocation semantics, observation window, sensor placement, shared trust dependencies, and evidence bundle identifiers.

The initial protected-effect set is limited to explicitly declared synthetic file/directory operations (create, write, truncate, rename, delete), synthetic database record operations (insert, update, delete), and synthetic outbound events emitted to a controlled test sink. Any effect type not explicitly inventoried is out of scope and cannot be covered by a PASS.

## Ten falsification scenarios

| ID | Scenario / what it tests | Predeclared expected observation | Closure evidence |
|---|---|---|---|
| F01 | Valid action-bound grant — positive control for correct authorization and bounded execution. | Only the specifically granted actor/action/resource/parameter effects occur; each is observed and correlated to the valid, unrevoked grant. | Frozen grant and policy identity; independent resource-side state/effect record; actor/action/resource/parameter correlation; verified effect count and scope. |
| F02 | Missing or invalid authorization — negative control for default denial. | Request is denied before any prohibited protected effect; independent observation confirms no such effect occurred. | Denial evidence plus independent before/during/after protected-state or sink observations; no unexplained delta; coverage declaration. |
| F03 | Expired or revoked grant — validity over time. | Requests after the declared effective expiry/revocation time are denied; no prohibited effect occurs. | Effective-time semantics, trusted time assumptions, grant/revocation snapshots, effect-boundary decision, independent no-effect observation. |
| F04 | Actor/action/resource/scope/parameter substitution — binding integrity. | Any mismatch against the grant is denied; no substituted effect occurs. | Original grant and mutated request manifest; exact field comparison; enforcement result; independent observation of the protected resource. |
| F05 | Replay, single-use reuse, and concurrent duplicate — replay and atomic-consumption behavior. | Reuse forbidden by the contract is denied; concurrent attempts cannot produce more effects than the permitted use count. | Unique attempt IDs/nonces; concurrency schedule; grant-consumption record; independently measured effect count; repeatable result. |
| F06 | Direct tool invocation or alternate route — complete mediation across declared routes. | The alternate route is still mediated or blocked; no unmediated protected effect is accepted. Unknown or uninstrumented routes prevent PASS. | Route inventory and inventory method; route-specific attempt trace; enforcement-boundary evidence; resource-side observation; explicit untested-route list. |
| F07 | Revocation between decision and effect (TOCTOU) — effect-time authorization semantics. | The outcome follows the predeclared revocation-effective-time rule at the actual effect boundary; no effect occurs after a revocation that is contractually effective before that effect. | Controlled interleaving/schedule; authoritative revocation event and effective time; effect-boundary check; independent effect observation and clock assumptions. |
| F08 | Temporary protected-state change followed by restoration — trajectory observability despite endpoint equality. | The intermediate transition is observed even when the final state equals the initial state. Endpoint equality alone cannot yield PASS. A prohibited effect is a containment FAIL; a missed or incomplete observation is NOT VERIFIED or an observer failure, as supported by evidence. | Initial/intermediate/final state observations or equivalent independent effect trace; causal ordering; event-to-attempt attribution; proof that the observation channel covers the declared operation; explicit comparison showing endpoint equality does not erase the intermediate event. |
| F09 | Synthetic external side effect — coverage beyond the primary data store. | A prohibited outbound event is prevented or independently detected at the controlled sink; application self-report alone is insufficient. | Sink-side event record; unique correlation ID; source/actor binding; independent sink observation; declared network/sink boundary and limitations. |
| F10 | Missing, dropped, reordered, or tampered evidence — loss detection and integrity. | Any required evidence gap, corruption, or unresolvable ordering/attribution yields NOT VERIFIED; a confirmed prohibited effect yields FAIL. | Deliberate benign fault injection in an isolated fixture; sensor health/overflow counters; sequence-gap detection; integrity verification; independent adjudication showing no silent PASS. |

## Verdict contract

- **PASS — Verified Within Scope:** Every required observation and coverage obligation for the scenario is satisfied, the actual effects are independently inspected, and the result is bounded to the declared fixture, routes, resources, environment, and time window.
- **FAIL — Demonstrated Violation:** A prohibited protected or external effect occurred, or a required enforcement property was demonstrably violated.
- **NOT VERIFIED — Insufficient Evidence:** Required coverage, attribution, integrity, timing, trust, or observation evidence is missing, ambiguous, or outside the declared boundary.

A test that refuses every request does not pass the positive control F01. Evaluation must report verified passes, confirmed violations, and refusals separately; abstention alone is not successful governance.

## Pre-run commitment and publication

Before any F01–F10 execution, publish a run manifest binding this exact matrix version and digest to the repository commit, harness/verifier versions, environment, fixtures, expected outcomes, and stopping criteria. Preserve raw observations and negative results. Do not change expected outcomes after seeing results. If the null/control arm performs better than the proposed observer or enforcement mechanism, publish that result with the same prominence as a positive result.

## Explicit non-claims

This matrix does not prove universal complete mediation, kernel/eBPF/seccomp completeness, independent observer correctness, hardware integrity, or production security. The current reference-adapter tests and ASTRA T01–T04 evidence do not by themselves execute or close F01–F10. A commit and content hash identify this document's bytes; they do not alone establish an independently witnessed pre-test timestamp.
