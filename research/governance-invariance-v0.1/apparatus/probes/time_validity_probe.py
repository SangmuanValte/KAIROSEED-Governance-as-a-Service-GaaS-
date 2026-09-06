"""Probe: expired authorization cannot become executable."""

from metrics.aewa import aewa, seal_transition


def run(now: int = 100, expires_at: int = 99):
    authority = {"echo:return"}
    action = "file:read"
    expired = now >= expires_at
    executed = False if expired else True
    trace = [{
        "action": action,
        "authority_before": sorted(authority),
        "authority_after": sorted(authority),
        "authorized_transition": False,
        "executed": executed,
    }]
    record = seal_transition(
        {"authority": sorted(authority), "now": now},
        {"action": action, "executed": executed, "expired": expired},
        {"type": "temporal-validation", "result": "BLOCK" if expired else "ALLOW"},
    )
    return {"probe": "time_validity", "expired": expired, "executed": executed, "aewa": aewa(trace), "record": record}


if __name__ == "__main__":
    print(run())
