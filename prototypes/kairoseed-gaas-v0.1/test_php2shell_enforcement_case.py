"""Frozen, harmless fixture tests for KAIROSEED-CASE-PHP2SHELL-001.

These tests model authorization and observation logic only. They do not
reproduce PHP2Shell, exercise PHP, send network traffic, or demonstrate
mitigation of CVE-2026-109618 / CVE-2026-109619.
"""
from dataclasses import dataclass

from kairoseed_gaas import ActionProposal, Decision, EvidenceLedger, govern


@dataclass(frozen=True)
class Request:
    request_id: str
    resource: str
    operation: str


class MockProtectedResource:
    """Harmless in-memory state used only by this test fixture."""

    def __init__(self):
        self._state = {"marker": "baseline", "revision": 0}

    def read_at_boundary(self):
        return dict(self._state)

    def apply(self, marker: str):
        self._state = {"marker": marker, "revision": self._state["revision"] + 1}


class FixtureObserver:
    """Read-only observer adapter; not an independently administered observer."""

    def observe(self, resource: MockProtectedResource):
        return resource.read_at_boundary()


def _denied_decision(request: Request):
    ledger = EvidenceLedger()
    try:
        proposal = ActionProposal(
            agent_id="php2shell-case-fixture",
            intent=f"{request.operation}:{request.resource}",
            authority_scope="unauthorized",
            policy_version="v0.1",
        )
        result = govern(proposal, ledger)
        assert result.decision is Decision.BLOCK
        return result
    finally:
        ledger.close()


def test_php2shell_t01_deny_leaves_mock_protected_state_unchanged():
    resource = MockProtectedResource()
    observer = FixtureObserver()
    before = observer.observe(resource)
    request = Request("req-t01", "mock://protected-record", "write")
    result = _denied_decision(request)

    # The denied path never calls resource.apply().
    after = observer.observe(resource)
    assert result.decision is Decision.BLOCK
    assert after == before


def test_php2shell_t02_authorized_control_reaches_mock_resource():
    resource = MockProtectedResource()
    observer = FixtureObserver()
    before = observer.observe(resource)

    ledger = EvidenceLedger()
    try:
        proposal = ActionProposal(
            agent_id="php2shell-case-fixture",
            intent="write:mock://control-record",
            authority_scope="authorized",
            policy_version="v0.1",
        )
        result = govern(proposal, ledger)
        assert result.decision is Decision.ALLOW
        resource.apply("authorized-control")
    finally:
        ledger.close()

    after = observer.observe(resource)
    assert after["revision"] == before["revision"] + 1
    assert after["marker"] == "authorized-control"


def test_php2shell_t03_attributed_mutation_after_deny_falsifies_fixture_invariant():
    resource = MockProtectedResource()
    observer = FixtureObserver()
    before = observer.observe(resource)
    request = Request("req-t03", "mock://protected-record", "write")
    result = _denied_decision(request)

    # Synthetic fixture event: the request identifier is deliberately linked
    # to the mutation. This tests adjudication logic, not real-world causality.
    synthetic_event = {
        "request_id": request.request_id,
        "resource": request.resource,
        "event": "protected_state_mutation",
    }
    resource.apply("unexpected-mutation")
    after = observer.observe(resource)

    causally_linked_in_fixture = (
        synthetic_event["request_id"] == request.request_id
        and synthetic_event["resource"] == request.resource
        and synthetic_event["event"] == "protected_state_mutation"
    )
    invariant_holds = (
        result.decision is Decision.BLOCK
        and after == before
    )
    assert causally_linked_in_fixture
    assert not invariant_holds
    # The observed counterexample is a FAIL within this synthetic fixture.


def test_php2shell_t04_missing_independent_observer_assurance_is_not_verified():
    resource = MockProtectedResource()
    observer = FixtureObserver()
    before = observer.observe(resource)
    request = Request("req-t04", "mock://protected-record", "write")
    result = _denied_decision(request)
    after = observer.observe(resource)

    # The fixture observer shares the test process and resource object. It is
    # intentionally NOT treated as proof of an independent trust boundary.
    independent_observer_assured = False
    if not independent_observer_assured:
        verdict = "NOT VERIFIED"
    else:
        verdict = (
            "PASS"
            if result.decision is Decision.BLOCK and after == before
            else "FAIL"
        )

    assert result.decision is Decision.BLOCK
    assert after == before
    assert verdict == "NOT VERIFIED"
