from demo import Authorization, govana, run


def test_authorized_path_executes_and_is_verified():
    state = {}
    auth = Authorization("agent-1", "read", "document-1", "sandbox")
    result = run(govana("agent-1", "read", "document-1", "sandbox"), auth, state)

    assert result["decision"] == "PASS"
    assert result["executed"] is True
    assert result["evidence"]["verified"] is True
    assert state["last_action"] == "read"


def test_missing_authorization_blocks_before_execution():
    state = {}
    result = run(govana("agent-1", "read", "document-1", "sandbox"), None, state)

    assert result["decision"] == "BLOCK"
    assert result["reason"] == "missing_authorization"
    assert result["executed"] is False
    assert state == {}


def test_authorization_binding_mismatch_blocks():
    state = {}
    auth = Authorization("agent-1", "read", "document-1", "sandbox")
    proposal = govana("agent-1", "delete", "document-1", "sandbox")

    result = run(proposal, auth, state)

    assert result["decision"] == "BLOCK"
    assert result["reason"] == "authorization_binding_mismatch"
    assert result["executed"] is False
    assert state == {}


def test_scope_change_blocks():
    state = {}
    auth = Authorization("agent-1", "read", "document-1", "sandbox")
    proposal = govana("agent-1", "read", "document-1", "production")

    result = run(proposal, auth, state)

    assert result["decision"] == "BLOCK"
    assert result["executed"] is False
    assert state == {}
