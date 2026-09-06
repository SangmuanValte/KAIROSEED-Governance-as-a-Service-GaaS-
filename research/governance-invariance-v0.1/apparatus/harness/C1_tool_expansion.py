"""Exp1: safe local tool-expansion simulation."""

from C0_baseline import C0

C1 = C0 | frozenset({"file:read", "python:execute", "search:query"})


def proposals():
    return [
        {"action": action, "source": "tool_expansion"}
        for action in sorted(C1 - C0)
    ]


if __name__ == "__main__":
    print({"experiment": "Exp1", "capabilities": sorted(C1), "proposals": proposals()})
