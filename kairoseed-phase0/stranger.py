"""Separate synthetic read-only observer process. Imports neither GAT nor PEP.

Observer reads mock fixture state through a dedicated observation channel,
not by accepting the executor's claimed result. This is process separation,
NOT an OS-backed independent security boundary.
"""
from __future__ import annotations


def snapshot(observer_channel):
    observer_channel.send({"op": "snapshot"})
    if not observer_channel.poll(2.0):
        raise RuntimeError("SNAPSHOT_UNAVAILABLE")
    response = observer_channel.recv()
    if response.get("ok") is not True:
        raise RuntimeError("SNAPSHOT_FAILED")
    state = response["state"]
    if not isinstance(state, dict) or not all(
        isinstance(key, str) and isinstance(value, bool)
        for key, value in state.items()
    ):
        raise RuntimeError("INVALID_STATE")
    return dict(state)


def diff(before, after):
    if set(before) != set(after):
        raise ValueError("STATE_KEYS_MISMATCH")
    return {key: after[key] for key in after if before[key] != after[key]}


def verify_delta(before, after, expected):
    observed = diff(before, after)
    return {
        "verdict": "MATCH" if observed == expected else "MISMATCH",
        "observed_delta": observed,
        "expected_delta": dict(expected),
    }


def stranger_worker(request_channel, observer_channel):
    while True:
        try:
            request = request_channel.recv()
        except EOFError:
            return
        op = request.get("op")
        if op == "stop":
            request_channel.send({"ok": True})
            return
        try:
            if op == "snapshot":
                result = {"ok": True, "state": snapshot(observer_channel)}
            elif op == "verify_delta":
                result = {
                    "ok": True,
                    **verify_delta(
                        request["before"], request["after"], request["expected"]
                    ),
                }
            else:
                result = {"ok": False, "reason": "UNKNOWN_OBSERVER_REQUEST"}
        except (RuntimeError, KeyError, ValueError, TypeError, EOFError, OSError) as exc:
            result = {"ok": False, "reason": str(exc)}
        request_channel.send(result)
