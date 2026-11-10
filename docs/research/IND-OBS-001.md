# IND-OBS-001 — Independent Protected-State Observation

**Status:** PROPOSED REQUIREMENT · CURRENTLY UNMET  
**Applies to:** KAIROSEED-CASE-PHP2SHELL-001 and future enforcement-verification cases.

## Requirement

Protected-state observations used to adjudicate enforcement correctness MUST be collected at, or independently anchored to, the protected resource boundary.

The enforcement subject MUST NOT be the sole source of evidence about its own enforcement behavior.

The test contract MUST separately establish:

1. **Observer independence:** the observer is outside the enforcement subject's administrative and execution trust boundary.
2. **Observation integrity:** the evidence path detects or prevents unauthorized alteration, omission, and substitution within its stated threat model.
3. **Resource identity:** the observed resource is the same protected resource named in the authorization request.
4. **Causal attribution:** the evidence supports a causal link between the tested request and any observed state transition; temporal proximity alone is insufficient.
5. **Adjudication independence:** the reviewer can inspect the evidence and reproduce the verdict without relying solely on the subject's own report.

## Verdict rule

If any required property is absent, untested, or unsupported, the verdict MUST be **NOT VERIFIED**. A DENY decision followed by a causally attributable protected-state mutation is a **FAIL** for the tested invariant. A passing result is limited to the declared resource, runtime, threat model, and test coverage.

## Current state

**UNMET.** The PHP2Shell case's fixture observer is a read-only adapter in the same test process and shares the mock resource object. It is useful for exercising the verdict logic but does not demonstrate independent administration, separate hardware, a separate trust domain, or independent evidence custody.

This requirement is committed before test execution. No claim of compliance is made.
