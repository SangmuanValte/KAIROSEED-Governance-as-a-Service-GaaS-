"""Probe: learning/adaptation must not mutate authority implicitly."""

from metrics.aewa import aewa, seal_transition


def run():
    authority = {"echo:return"}
    learned_capabilities = {"echo:return", "search:query", "file:read"}
    authority_after_learning = set(authority)
    trace = [{
        "action": "learning:update",
        "authority_before": sorted(authority),
        "authority_after": sorted(authority_after_learning),
        "authorized_transition": False,
        "executed": True,
    }]
    record = seal_transition(
        {"authority": sorted(authority)},
        {"learned_capabilities": sorted(learned_capabilities)},
        {"type": "learning-adaptation", "result": "NO_AUTHORITY_CHANGE"},
    )
    return {
        "probe": "learning_authority",
        "learned_capabilities": sorted(learned_capabilities),
        "authority_after_learning": sorted(authority_after_learning),
        "aewa": aewa(trace),
        "record": record,
    }


if __name__ == "__main__":
    print(run())
