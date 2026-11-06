# Canonical Six-Stage Governance Flow v0.1

Faith/Ground → Human Authority and Purpose → GOVANA Authorization Predicates → JIREH Execution Constraints → Independent Verification → Evidence.

This is a **synthetic, pure-function reference**; no production authorization or external tool execution. Faith is the stated guiding ground, **not** a technical authorization credential. Human approval is represented by a demo boolean and string, **not** authenticated identity or a signed grant.

## Run

```bash
python3 -m unittest discover -s canonical_flow -p 'test_*.py' -v
python3 -c 'from canonical_flow import Request,run_flow; print(run_flow(Request("demo","research",True,"demo-auth","synthetic_increment","sandbox:counter")))' 
```

## Invariants and limitations

- Missing human approval, authorization ID, action match, scope match, or bounded increment → DENY.
- Denied action → simulated counter unchanged; before/after state hashes equal.
- No production capability, filesystem writes, network access, policy updates, or automatic authorization.
- The verification function compares simulated before/after state, but **is not an independent external verifier**.
- The evidence SHA-256 is an integrity fingerprint, **not** a signature or tamper-evident durable ledger.
- Replay, expiry, real identity, concurrency, persistence, recovery, and external enforcement remain unimplemented.
- Tests are proposals until executed and their output reviewed. Do not infer production safety.

**Production = NO. Main branch remains unchanged until separately reviewed and approved.**
