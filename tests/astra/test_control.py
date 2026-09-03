import hashlib, json

class AuthorizationDenied(Exception): pass

class State:
    def __init__(self):
        self.version = 1
        self.value = 0

class Proposal:
    def __init__(self, proposal_id, capability, scope, requested_value):
        self.proposal_id = proposal_id
        self.capability = capability
        self.scope = scope
        self.requested_value = requested_value

def authorize(p, state, allowed_capabilities, allowed_scope):
    if p.capability not in allowed_capabilities:
        raise AuthorizationDenied("capability denied")
    if p.scope != allowed_scope:
        raise AuthorizationDenied("scope denied")
    return {"proposal_id": p.proposal_id, "state_version": state.version}

def execute(receipt, p, state):
    if receipt["state_version"] != state.version:
        raise AuthorizationDenied("stale authorization")
    state.value = p.requested_value
    return state.value

def run():
    results = []
    s = State(); p = Proposal("T01", "db.write", "/protected", 1)
    try:
        authorize(p, s, {"db.read"}, "/protected")
        results.append(("T01", False, "unexpected admission"))
    except AuthorizationDenied:
        results.append(("T01", s.value == 0, "denied before state change"))

    s = State(); p = Proposal("T02", "db.write", "/allowed", 7)
    r = authorize(p, s, {"db.write"}, "/allowed")
    execute(r, p, s)
    results.append(("T02", s.value == 7, "authorized bounded execution"))

    s = State(); p = Proposal("T03", "db.write", "/outside", 9)
    try:
        authorize(p, s, {"db.write"}, "/allowed")
        results.append(("T03", False, "unexpected scope admission"))
    except AuthorizationDenied:
        results.append(("T03", True, "scope mismatch denied"))

    s = State(); p = Proposal("T04", "db.write", "/allowed", 3)
    r = authorize(p, s, {"db.write"}, "/allowed")
    s.version += 1
    try:
        execute(r, p, s)
        results.append(("T04", False, "stale receipt executed"))
    except AuthorizationDenied:
        results.append(("T04", True, "stale authorization denied"))

    passed = all(ok for _, ok, _ in results)
    return results, passed

if __name__ == "__main__":
    results, passed = run()
    for test_id, ok, note in results:
        print(f"{test_id}: {'PASS' if ok else 'FAIL'} — {note}")
    print("CONTROL_RESULT:", "PASS" if passed else "FAIL")
    raise SystemExit(0 if passed else 1)
