"""Exp2: safe simulation of planning, memory, and concurrent proposals."""

from C1_tool_expansion import C1

C2 = C1 | frozenset({"memory:read", "plan:compose", "proposal:concurrent"})


def proposals():
    return [
        {"action": action, "source": "reasoning_expansion"}
        for action in sorted(C2 - C1)
    ]


if __name__ == "__main__":
    print({"experiment": "Exp2", "capabilities": sorted(C2), "proposals": proposals()})
