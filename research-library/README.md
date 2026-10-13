# KAIROSEED — Internal R&D Library

**Mode:** STACK / PARK / PRESERVE  
**Initialized:** 2026-10-04  
**Working branch:** `rd-proof-2026-10-04` (Draft PR #26)  
**Canonical principle:** Claim <= Evidence <= Established Scope

## Purpose

This is a **read-only-by-policy catalog of references** to code, architecture, experiments, results and unresolved judgments. It is *not* an authorization mechanism, a deployment configuration, an agent execution queue, or a claim that each indexed artifact has been independently verified.

**No automatic promotions:** An index entry never changes FAIL, UNKNOWN, or UNVERIFIED to PASS. Links do not constitute proof. Any future execution requires separately approved scope and independent evidence.

## Layout

- `catalog.json` — machine-readable registry of what is actually linked and the current evidence state.
- `INTAKE_TEMPLATE.md` — repeatable form for adding records without overstating conclusions.
- `../evidence/RD-2026-10-04/OPERATIONAL_PROOF.md` — initial frozen R&D proof and unresolved judgment record.

Existing code and documents remain in their original paths, including `src/`, `docs/`, `tests/`, `governance/`, and `evidence/`. **Reference; do not duplicate or migrate** as part of this archival phase.

## Status vocabulary

| Status | Meaning |
| --- | --- |
| `INDEXED` | Path or document identified, contents/outcomes not necessarily reviewed |
| `SPECIFIED` | Documented requirement or planned test; no execution implied |
| `REFERENCE_CODE` | Implementation exists; no universal correctness assertion |
| `OBSERVED_FAIL` | A specific, linked run failed |
| `UNVERIFIED` | Outcome requires further evidence, not equal to false |
| `PARKED` | Intentionally deferred; no execution authorized |
| `VERIFIED_SCOPE` | Allowed only with recorded reproducible tests, assumptions, independent observation and exact scope |

## Workflow for later use

1. **Discover:** Record the canonical path/URL and exact revision (commit SHA, if applicable).
2. **Classify:** Specify whether the entry is a source file, design, hypothesis, test plan, observed result, or unresolved issue.
3. **Separate claims from observations:** Write an expected outcome separately from measured outcomes.
4. **Preserve:** Link the raw logs or original records; never replace a failure with an optimistic summary.
5. **Review:** Require human acceptance for scope changes; get independent evidence before labeling `VERIFIED_SCOPE`.
6. **Park:** When deferred, record the next falsifiable question instead of launching new agents or environments.

## Preserved initial boundary

The observed GitHub Actions run [36940347874](https://github.com/SangmuanValte/KAIROSEED-Governance-as-a-Service-GaaS-/actions/runs/36940347874) on commit `384cc7025a07de8cab9dac4d5a0bfa3cc450d488` failed during the **full test suite** after source compilation succeeded. Later production-gate steps were skipped. The failing assertion was not identified from the information reviewed, so no repair or PASS is claimed.

## Research governance

AURORA may organize research questions and sources; SEEDFORGE may propose implementation work; GOVANA/JIREH are architecture concepts under evaluation. **Cataloging these names does not imply operational authorization or verified enforcement.** External agents, Gemini/Meta AI artifacts, and earlier chats are not treated as independently verified evidence unless source records are explicitly imported and examined.

**Current instruction: archive and index only.** Do not merge the draft PR, deploy, claim production readiness, or start high-consequence tests solely because an entry exists here.
