# FAILURE MODES

This file is reserved for empirical counterexamples.

## Recording rule

If a reproducible run produces AEWA > 0, do **not** silently repair the implementation before preserving the trace. Record:

1. run identifier and commit SHA;
2. capability state `C_t` and `C_{t+1}`;
3. authorized action space `A_t` and `A_{t+1}`;
4. proposed and executed action;
5. authorization ledger transition (or absence of one);
6. governed state before/after;
7. EvidenceSeal and hash-chain status;
8. exact reproduction command and environment;
9. whether the result is a harness defect, configuration defect, implementation defect, or unresolved;
10. replication status.

## Claim discipline

An AEWA observation is first a counterexample to the tested implementation/configuration under the tested conditions. It is not, by itself, evidence that all KAIROSEED deployments fail.

No failure has been recorded by this file until an actual empirical run produces one.
