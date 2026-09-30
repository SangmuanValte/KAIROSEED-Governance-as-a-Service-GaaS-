# Smallest Govana → VEP → PEP → JIREH Demo

## Status

**CONFIRMED IMPLEMENTATION:** this demo is a local deterministic reference path.

**Scope:** one actor, one capability, one action, one resource, one authorization envelope.

It does not execute external systems.

## Flow

```
Agent proposal
    ↓
Govana
    ↓
VEP
    ↓
PEP
    ├── BLOCK → no execution
    └── PASS
         ↓
       JIREH
         ↓
      evidence
```

### File map

- `demo.py` — the complete four-stage flow and tiny local state transition.
- `test_demo.py` — positive and adversarial tests.
- `README.md` — scope, invariants, and commands.

## Boundary definitions

**Govana:** produces the minimal proposed action envelope.

**VEP:** validates proposal shape and required fields. It does not grant authority.

**PEP:** makes the authorization decision. This is the authorization boundary.

**JIREH:** operates only after PEP PASS and verifies the resulting local state transition. JIREH does not create permission.

## Invariants

1. Missing authorization ⇒ BLOCK.
2. Wrong actor/action/resource ⇒ BLOCK.
3. PEP BLOCK ⇒ JIREH is never called.
4. PEP PASS is required before the state transition.
5. JIREH verifies the post-state rather than declaring success itself.

## Run

From repository root:

```bash
python demos/governance_minimal/demo.py
python -m pytest -q demos/governance_minimal/test_demo.py
```

Expected tests cover authorized execution, unauthorized action, scope mismatch, and execution-gate enforcement.
