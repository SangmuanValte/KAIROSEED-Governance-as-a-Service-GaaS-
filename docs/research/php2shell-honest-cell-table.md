# PHP2Shell Case — Honest-Cell Table

**Status:** BASELINE COMMITTED · TEST RESULTS PENDING  
**Reference case:** KAIROSEED-CASE-PHP2SHELL-001

| Cell | Claim / observation | Status | Evidence or limitation |
|---|---|---|---|
| H01 | PHP2Shell is a disclosed PHP runtime vulnerability class covering CVE-2026-109618 and CVE-2026-109619 | DOCUMENTED CONTEXT | External advisories cited in the case file |
| H02 | KAIROSEED fixed or patched either CVE | NOT CLAIMED | KAIROSEED is not the PHP remediation |
| H03 | Four harmless fixture tests are defined | COMMITTED | Test file committed; not run |
| H04 | DENY prevents mutation in the mock fixture | NOT VERIFIED | Requires test execution |
| H05 | Authorized control can mutate the mock fixture | NOT VERIFIED | Requires test execution |
| H06 | A causally linked mutation is adjudicated as FAIL | NOT VERIFIED | Synthetic attribution logic only |
| H07 | Independent observer trust boundary is established | UNMET | Fixture observer shares process/resource trust boundary |
| H08 | Refusals metric has measured results | NOT VERIFIED | Metric defined; no measurements |
| H09 | Independent execution and adjudication completed | PENDING | External reviewer not yet engaged |
| H10 | Real PHP2Shell exploit traffic or vulnerable PHP runtime tested | OUT OF SCOPE | No exploit reproduction or live-target testing |
| H11 | KAIROSEED mitigates PHP2Shell in real deployments | NOT ESTABLISHED | No such claim is made |

## Reporting rule

Never replace NOT VERIFIED, UNMET, PENDING, or OUT OF SCOPE with PASS. Preserve negative results and limitations alongside positive observations. Update this table only with a linked run artifact and reviewer evidence.
