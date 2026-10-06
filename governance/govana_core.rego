package kairoseed.govana

import rego.v1

# GOVANA v0.1: pre-execution enforcement for E ⊆ S_auth and epoch binding.
# Expected data shape:
# data.kairoseed.epoch = {"id": 7, "authorized_scope": ["seq", "par", "worker:cpu"]}
# Expected input shape:
# {"token_epoch": 7, "evidence": [{"evidence_id":"ev-1","scope_atoms":["seq"]}]}

default allow := false

violation contains {"code": "STALE_EPOCH"} if {
    input.token_epoch != data.kairoseed.epoch.id
}

scope_authorized(scope) if {
    scope in data.kairoseed.epoch.authorized_scope
}

violation contains {"code": "EVIDENCE_OUTSIDE_SCOPE", "scope_atom": scope} if {
    some evidence in input.evidence
    some scope in evidence.scope_atoms
    not scope_authorized(scope)
}

allow if {
    count(violation) == 0
}

decision := {
    "allow": allow,
    "epoch": data.kairoseed.epoch.id,
    "violations": violation,
}
