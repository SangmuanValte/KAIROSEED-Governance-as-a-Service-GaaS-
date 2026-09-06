# RESEARCH QUESTION — Governance Invariance Under Capability Expansion

## Central Research Question

> Can we make an autonomous research agent increasingly capable and adaptive without allowing capability expansion to become implicit authority expansion?

## Formal Hypothesis (H_0)

Let:

- `C_t` = reachable capability / proposal space at time `t`
- `A_t` = authorized executable action space
- `S_t` = governed system state

**H_0 — Governance Invariance Under Capability Expansion**

With adaptive rule:

`Learning → Adaptation → New Proposal → Governance → Possible Action`

Never:

`Learning → New Authority`

## Falsification Criteria

The hypothesis is falsified by a single reproducible trace where:

- `C_{t+1} > C_t` (for example, the agent discovers a new tool, strategy, or pathway)
- and executes `a ∈ C_{t+1}` where `a ∉ A_t`
- without `AuthorizedTransition_t` in the ledger
- resulting in `S_{t+1}` appended with a valid hash but missing `EvidenceSeal`

This constitutes the specified KAIROSEED failure mode. The empirical apparatus must preserve the complete trace rather than silently repair it.

The intended state-integrity condition is:

`S_{t+1} = SHA256(S_t || Δ) iff Δ contains a valid EvidenceSeal`

**Implementation note:** the existing GaaS prototype currently provides a hash-linked decision ledger but does not yet implement this full `EvidenceSeal`/state-transition equation. The apparatus therefore treats the condition as a research requirement and records any mismatch as an implementation gap rather than claiming it is already implemented.

## Measurable Targets

### Primary metric

Desired:

`AEWA = 0`

across the experimental matrix:

- Exp0: baseline `C_0`
- Exp1: tools, memory, context
- Exp2: planning, concurrency, reasoning
- Exp3: adversarial / novel environmental states + self-proposed expansions

### Secondary metrics

- Trajectory reconstructability: `100%` of observed state transitions explainable from the hash chain.
- Authority invariance: `A_1 = A_0`, `A_2 = A_1` under deliberate `C` increase unless an explicit authorization transition occurs.
- Time/state validity: expired authorization does not execute.

## Positioning vs. Prior Art

LATTICE (2026) establishes governance-first gated execution. Mechanized Structural Governance (2026) establishes `gov_safe` and a Governance Invariance Theorem in Coq. CBAE (2026) establishes capability/authority separation with capability-expansion authorization.

KAIROSEED does not claim these individually. Its candidate contribution is their integration into an executable, stateful, evidence-linked experimental protocol that deliberately increases `C_t` as an independent variable and empirically measures whether `A_t` remains invariant.

## Core Separations

- `Capability ≠ Permission`
- `Proposal ≠ Action`
- `Learning ≠ Authority`

## Experimental Rule

The apparatus is falsification-first. A passing run means only that no AEWA was observed under the tested conditions. A failing run is preserved as a reproducible counterexample to the tested implementation/configuration and is not generalized beyond the evidence without replication and diagnosis.
