WHO
- SangmuanValte — building governance-first infrastructure for autonomous AI.

WHAT IS BEING BUILT
- KAIROSEED: governance model and decision primitives.
- ASTRA: orchestration and agent patterns.
- automate-prototype: practical loop for research → prototype → verify → evidence.

WHY
- To let agents execute and learn while keeping authority explicit and auditable.
- Execution over abstraction: turn ideas into small, testable prototypes and collect reproducible evidence before making governance decisions.

START HERE
1. automate-prototype — the practical entry point (quickstart + examples).
2. KAIROSEED — governance & design principles.
3. experiments/ — reproducible experiments and evidence artifacts.

CORE REPOSITORIES
- automate-prototype — prototype loop code, workflows, verification instruments.
- KAIROSEED — governance patterns, invariants, policies.
- astra — orchestration utilities (agents, adapters).

TOOLS / EXPERIMENTS
- Verification instruments (HAB-001) that scan workflows and produce evidence JSON.
- Small experiments live in experiments/<name> with README and evidence artifacts.

EVIDENCE
- Each experiment contains evidence.json and an artifacts/ folder with logs and reproducibility checks.
- PRs that change governance-relevant files attach verification artifacts and a short human-facing summary.

HOW TO EXPLORE
- Start with automate-prototype/README.md for a guided quickstart.
- Browse experiments/ to see examples and evidence.
- Open issues/PRs if you want to propose changes to governance invariants or new verification campaigns.
