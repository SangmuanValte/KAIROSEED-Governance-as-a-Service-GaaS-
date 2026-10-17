"""Faith/Ground -> Human Authority -> GOVANA -> JIREH -> Verify -> Evidence.

Pure, deterministic, side-effect-free reference simulation. No real protected resources.
"""
from dataclasses import dataclass
from hashlib import sha256
import json

GROUND = "JESUS CHRIST FIRST OVER EVERYTHING"
POLICY_VERSION = "six-stage-v0.1"
ALLOWED_ACTION = "synthetic_increment"
ALLOWED_SCOPE = "sandbox:counter"

@dataclass(frozen=True)
class Request:
    request_id: str
    purpose: str
    human_approved: bool
    authorization_id: str
    action: str
    scope: str
    increment: int = 1

def _digest(value):
    return sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest()

def run_flow(request: Request, initial_state=0):
    """Return a simulated state transition and inspectable evidence; never persist."""
    if type(initial_state) is not int or initial_state < 0:
        raise ValueError("initial_state must be a nonnegative integer")
    if not isinstance(request, Request):
        raise TypeError("request must be Request")
    stages = [{"stage": "FAITH_GROUND", "status": "CONTEXT", "statement": GROUND}]
    human = (request.human_approved is True and isinstance(request.purpose, str)
             and bool(request.purpose.strip()) and isinstance(request.request_id, str)
             and bool(request.request_id.strip()))
    stages.append({"stage": "HUMAN_AUTHORITY", "status": "PASS" if human else "DENY"})
    govana = (human and isinstance(request.authorization_id, str)
              and bool(request.authorization_id.strip())
              and request.scope == ALLOWED_SCOPE and request.action == ALLOWED_ACTION
              and type(request.increment) is int and request.increment == 1)
    stages.append({"stage": "GOVANA", "status": "ALLOW" if govana else "DENY",
                   "policy_version": POLICY_VERSION})
    # Synthetic JIREH: no execution on denied requests; bounded transition otherwise.
    final_state = initial_state + 1 if govana else initial_state
    stages.append({"stage": "JIREH", "status": "SIMULATED" if govana else "BLOCKED"})
    # Independent *function* checking the transition, not an independent trust domain.
    expected = initial_state + 1 if govana else initial_state
    verified = final_state == expected
    stages.append({"stage": "INDEPENDENT_VERIFICATION",
                   "status": "PASS" if verified else "FAIL",
                   "method": "synthetic_state_comparison"})
    evidence = {
        "schema": "kairoseed.canonical_flow.v0.1",
        "production": False,
        "simulated": True,
        "request_id": request.request_id,
        "authorization_id": request.authorization_id if govana else None,
        "scope": request.scope,
        "action": request.action,
        "before": initial_state,
        "after": final_state,
        "before_sha256": _digest({"counter": initial_state}),
        "after_sha256": _digest({"counter": final_state}),
        "authorized": govana,
        "verified": verified,
        "stages": stages,
        "limitations": "In-process synthetic reference; no durable authority, cryptographic attestation or external verifier.",
    }
    evidence["stages"].append({"stage": "EVIDENCE", "status": "RECORDED_IN_MEMORY"})
    evidence["evidence_sha256"] = _digest(evidence)
    return evidence
