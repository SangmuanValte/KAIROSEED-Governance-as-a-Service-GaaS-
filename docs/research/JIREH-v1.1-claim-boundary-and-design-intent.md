# JIREH v1.1 — Claim Boundary and Design Intent

> **Classification:** Non-canonical research documentation  
> **Documentation decision:** Accepted for documentation, 2026-11-06  
> **Assurance status:** **NOT VERIFIED**  
> **Canonical specification:** **FROZEN — UNCHANGED**  
> **Deployment or production authorization:** **NOT GRANTED**

## Purpose

Prevent an architectural aspiration from being read as an implemented or independently verified capability. Distinguish **specified claims**, **design intent**, **test obligations**, and **observed evidence**. This record documents the research interpretation; it does not amend a frozen canonical contract, prove a runtime mechanism, or itself establish a cryptographic pre-test claim freeze.

**Governing rules:** Capability ≠ Permission · Authorization ≠ Execution · Completion ≠ Verified Success · Claim ≤ Evidence ≤ Established Scope. **No verified evidence → No PASS.**

## A. JIREH v1.1 — Specified research claims (not implementation evidence)

| ID | Specified boundary / behavior | Verification boundary |
|---|---|---|
| J-01 | JIREH is defined as a post-authorization runtime enforcement and containment layer, downstream of GOVANA CORE. It must not originate, grant, expand, or renew permissions. | Architectural responsibility is specified; enforcement of that separation is **NOT VERIFIED**. |
| J-02 | Proposed normal incident sequence: deny prohibited effects and initiate PAUSE/isolation; verify containment where possible; capture evidence; ATTEST/SIGN; then attempt KILL/termination and independently verify its effect. | PAUSE, SIGN, and KILL are **not an atomic or non-preemptible transaction**. No runtime timing or isolation guarantee is established. |
| J-03 | The Sign → Kill interval is an explicit research risk that must be measured. Signing witnesses specific evidence; it neither grants authority nor proves the workload has terminated. | An ordered design does not establish observed order, absence of intermediate effects, or termination success. |
| J-04 | An assurance verdict must bind to a frozen, versioned claim set, its pre-test commitment, the specific test and per-claim evidence. Contradicted claims are preserved and superseded visibly rather than quietly edited. | A conversation statement or later commit alone does not prove pre-test commitment, independent evidence, or correct adjudication. |
| J-05 | The proposed evaluation flow is: FZ → Generate → Check grants → Dynamics/Spectral/Governance evaluation → Join → Verify against frozen claims → if contradicted, record supersession proposal → new FZ. | Flow is a **research process description**. No operational proof is established for its proposed dynamics or spectral stages. |

“Specified” means the desired contract has been described; it does **not** mean the contract has been implemented, enforced, independently tested, or passed.

## B. JIREH — Design Intent only (NOT v1.1 verified capability)

| Proposed direction | Missing proof or implementation obligation |
|---|---|
| Lyapunov stability and divergence monitoring | Explicit state variables and (V(x)), sufficient assumptions, threshold semantics, runtime traces, and independent verification; **G1 unresolved**. |
| Spectral viability / entropy-collapse monitoring | Defined eigenvalue/variance window, (δ_{min}), semantics distinguishing gridlock from timeout, and measured trigger behavior; **G2 unresolved**. |
| eBPF/seccomp and related Linux isolation | Actual code, pinned kernel/runtime environment, hook coverage, independent protected-effect observations, and adversarial cross-path tests. SIGSTOP delivery is **not** synchronous memory immutability. |
| PTZ-to-JIREH constraint compilation | Source proof specification, compiler semantics, deployable policy artifact, source-to-output binding and independently checked preservation; **G3 unresolved**. |
| Deterministic fail-closed operation | A precise bounded property and proof/measurement of all protected-effect paths, including concurrency, revocation races, external writers, termination failures, and trust dependencies. |
| Tamper-resistant L6 receipts and independent verification | Independently established provenance, protected effect observations, trust/coverage model, and integrity/chronology checks. A signature or timestamp alone is not proof of containment. |

**Do not describe the above as operational JIREH v1.1 capabilities.** Acceptable label: **“JIREH Design Intent — NOT v1.1 Verified Claim. Not established as implemented or proven; subject to counterexample.”**

## C. Non-atomic termination and assurance rules

1. **Pre-effect denial takes priority.** The system must not allow prohibited effects to continue merely because signing or termination has not completed.
2. **PAUSE requested ≠ PAUSE effective.** Explicit observation is needed before claiming the workload is quiescent. Suspending execution does not, by itself, prevent external memory writes or other out-of-band effects.
3. **Sign → Kill is non-atomic.** Its elapsed window, interruption, replay, and failed termination are open test obligations. Do not treat ordered user-space timestamps as proof of atomicity.
4. **Kill must be outcome-checked.** A termination request is not a confirmed termination. Any retry must be scoped and identity-bound; token revocation and future pattern restrictions require valid separate authorization.
5. **Evidence cannot self-certify.** Independently inspect protected state, intermediate transitions, and stated external effects. A matching before/after hash and adapter log alone are insufficient.
6. **Per-claim verdict:** **PASS — Verified Within Scope**, **FAIL — demonstrated violation**, or **NOT VERIFIED — insufficient evidence**. No broad assurance from enumerated-path tests.

## D. Evidence and claim-freeze integrity

A testable claim freeze needs a versioned and canonically serialized claim artifact, digest, explicit scope, recorded commitment before the test, and traceable evidence supporting that chronology. Each test must bind to the exact claim hash. Subsequent narrowing or correction creates a separate new version; the prior claim and its verdict remain preserved.

This documentation file is **not** itself the frozen canonical claim set and contains **no claim** that an L6 ledger entry, signed claim commitment, or independent verification certificate already exists. A Git commit records file revision history; it does not independently establish that a claim was frozen before an experiment.

## E. Related open research

- [Issue #30 — Independent Containment Verification: Complete Mediation and Unauthorized Effects](https://github.com/SangmuanValte/KAIROSEED-Governance-as-a-Service-GaaS-/issues/30) — proposed scope/coverage model, independent observer requirements, adversarial matrix, and assurance contract.
- KGS-003-EVIDENCE-002 — proposed synthetic race measurement protocol; any synthetic results must remain explicitly separated from real JIREH/eBPF/seccomp performance and C3/C6 assurance.
- C-KILL-v0.4 — proposed successor claim for **ordered, witnessed, non-atomic** termination. The previously asserted atomicity guarantee is not accepted as proven; preserve the original assertion as historical context. Do not label an experimental counterexample as executed unless linked evidence establishes it.

## F. Disposition

**Documentation accepted; independent verification NOT VERIFIED.** Canonical specification stays frozen. No deployment, code change, policy expansion, test PASS, formal proof, or independent reproduction is authorized or implied by this document.

> **Containment is not inferred. Containment is inspected.**  
> **No verified evidence → No PASS.**
