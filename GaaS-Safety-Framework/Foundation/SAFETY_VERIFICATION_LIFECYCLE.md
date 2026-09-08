# GaaS Safety Verification Lifecycle

**Status:** Reusable foundation artifact v1.0  
**Scope:** End-to-end verification, monitoring, correction, and learning loop for agentic systems

## Canonical lifecycle

`SYSTEM MODEL → TRUST BOUNDARY → CAPABILITY → AUTHORITY → ATTACK PATH → CONTROL → TEST → EVIDENCE → MONITOR → CORRECT → LEARN ↺`

## Stage questions

| Stage | Core question |
|---|---|
| **System Model** | What exists, and how does it interact? |
| **Trust Boundary** | Where does trust change or become conditional? |
| **Capability** | What can each component actually do? |
| **Authority** | What is each component permitted to do? |
| **Attack Path** | How could capability be converted into an unauthorized consequence? |
| **Control** | What prevents, detects, or limits that path? |
| **Test** | Does the control actually work under relevant conditions? |
| **Evidence** | What observable record proves what happened? |
| **Monitor** | Is the boundary continuing to hold over time? |
| **Correct** | What happens when it does not? |
| **Learn** | What should change in the model, control, or assumptions? |

## Capability / authority boundary

**Capability:** “Can the agent perform the action?”  
**Authority:** “Is the agent permitted to perform the action?”

`CAPABILITY ≠ PERMISSION`

Additional capability does not imply additional authority. Any increase in effective authority requires an explicitly defined authorization boundary with attributable scope, purpose, policy, validity, and applicable constraints.

## Attack-path governance test

The attack-path question is:

> **Can the agent cause a consequential effect that the governance system would not independently authorize?**

The test boundary is:

```text
CAPABILITY
    ↓
POSSIBLE ACTION
    ↓
CONSEQUENTIAL EFFECT?
    ↓
WOULD GOVERNANCE INDEPENDENTLY AUTHORIZE IT?
          │
       ┌──┴──┐
      YES    NO
       │      │
     ALLOW   ATTACK PATH
              ↓
       BLOCK / ESCALATE
              ↓
             DENY
              ↓
       NO AUTHORIZATION
              ↓
        NO EXECUTION
              ↓
           EVIDENCE
```

## Circumvention invariant

If governance independently denies an action, the agent must not obtain the same consequential effect through an alternative path without a new, valid authorization.

```text
DENY
→ NO AUTHORIZATION
→ NO EXECUTION
→ EVIDENCE
```

An alternative route that produces the same protected consequence without new valid authorization is a **governance bypass** and constitutes a test failure.

## Closed-loop operation

`EVIDENCE → MONITOR → CORRECT → LEARN → UPDATED MODEL / CONTROL / ASSUMPTIONS → RE-TEST`

Correction and learning must preserve historical evidence. Superseding a conclusion, policy, control, or assumption must not erase the record that caused the change.

## Relationship to Agent Circumvention Test

`AGENT_CIRCUMVENTION_TEST` is a test-harness artifact within this lifecycle. It operationalizes the **Attack Path → Control → Test → Evidence** portion and feeds observed failures into **Monitor → Correct → Learn**.

The lifecycle is broader than circumvention testing: it applies to ordinary authorization verification, trust-boundary changes, capability changes, control validation, operational monitoring, incident correction, and evidence-driven governance updates.

## Verification boundary

This lifecycle is a verification specification. A documented lifecycle does not itself establish security. Claims must remain bounded by the controls tested, evidence collected, environments exercised, and assumptions declared.
