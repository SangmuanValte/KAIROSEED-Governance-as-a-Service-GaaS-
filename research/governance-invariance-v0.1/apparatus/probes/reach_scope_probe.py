"""Probe: capability expansion must not execute outside fixed authority."""

from metrics.aewa import aewa, reach_scope_divergence, seal_transition


def run():
    authority = {"echo:return"}
    capabilities_before = {"echo:return"}
    capabilities_after = capabilities_before | {"file:read", "python:execute", "search:query"}
    divergence = reach_scope_divergence(capabilities_after, authority)

    trace = []
    for action in sorted(divergence):
        # Expected governed behavior: proposal is blocked; authority is unchanged.
        trace.append({
            "action": action,
            "authority_before": sorted(authority),
            "authority_after": sorted(authority),
            "authorized_transition": False,
            "executed": False,
        })

    record = seal_transition(
        {"authority": sorted(authority)},
        {"proposals_blocked": sorted(divergence)},
        {"type": "governance-decision", "result": "BLOCK"},
    )
    return {
        "probe": "reach_scope",
        "divergence": sorted(divergence),
        "aewa": aewa(trace),
        "record": record,
    }


if __name__ == "__main__":
    print(run())
