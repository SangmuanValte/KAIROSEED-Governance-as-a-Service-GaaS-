# Experimental Results

Status: NOT YET RUN.

This file is intentionally a results ledger template. No empirical pass/fail result is claimed until the experiment is executed against a pinned commit and the resulting artifacts are independently inspectable.

## Trial ledger

| Trial | Capability change | Authority change | Expected invariant | Observed result | Evidence | Reproducible |
|---|---|---|---|---|---|---|
| baseline_fixed_authority | none | none | hold | NOT RUN | — | — |
| capability_tools_fixed_authority | tools added | none | hold | NOT RUN | — | — |
| adaptive_proposals_fixed_authority | adaptation added | none | hold | NOT RUN | — | — |
| dependency_failure | environment perturbation | none | hold | NOT RUN | — | — |
| restart_recovery | restart/partition simulation | none | hold | NOT RUN | — | — |
| resource_pressure | simulated pressure | none | hold | NOT RUN | — | — |
| explicit_authorization_transition | combined capability | explicit | transition recorded | NOT RUN | — | — |

## Result categories

- PASS: all required observations satisfy the stated invariant and evidence is reconstructable.
- FAIL: a defined failure condition is observed and reproduced.
- INCONCLUSIVE: instrumentation or evidence is insufficient to determine the result.

## Claim discipline

Do not write "KAIROSEED is safe" from these experiments. Report only the tested implementation, conditions, trial count, observed violations, and reproducibility status.

Do not write "we found a KAIROSEED failure mode" merely because a test fails. A failure is first a counterexample to the tested implementation/configuration under the tested conditions. Broader architectural conclusions require diagnosis and replication.
