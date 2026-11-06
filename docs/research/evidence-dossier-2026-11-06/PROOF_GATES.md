# Proof and Evidence Gates

**Non-canonical research checklist. No assurance verdict is issued here.**

## Evidence required before any claim may receive PASS within scope

1. Exact claim ID, statement, assumptions, version and accepted scope.
2. Canonical claim bytes with a recorded hash and evidence that the freeze preceded testing.
3. Exact code revision, environment, dependencies and test manifest.
4. Actual executed tests, complete raw observations and captured failure outputs.
5. Separately observed protected-state and external-effect measurements.
6. Explicit observer trust assumptions, known coverage gaps and limitations.
7. Per-claim review by an independent verifier.
8. Preserved supersession record for corrected or narrowed claims.
9. A separate accountable production authorization decision, if deployment is later contemplated.

## Open JIREH proof obligations

- **G1:** define and test the claimed Lyapunov function.
- **G2:** define and test the spectral measurement and `delta_min`.
- **G3:** implement and verify the PTZ-to-runtime policy translation.
- **C3/C6:** measure non-atomic containment behavior and independently observed effects.
- **C4:** document observer independence, instrumentation and shared trust boundaries.
- **L6:** preserve integrity-protected raw evidence with independently checked provenance.

## Verdicts

**PASS:** independently verified inside a stated scope.  
**FAIL:** a specific requirement demonstrably contradicted.  
**NOT VERIFIED:** evidence or coverage missing or inconclusive.

A successful unit test, a signed text record, a Git commit, or a matching before/after hash is not alone proof of complete mediation or containment.

**Canonical specification remains frozen. Production authorization not granted.**

Claim ≤ Evidence ≤ Established Scope.
