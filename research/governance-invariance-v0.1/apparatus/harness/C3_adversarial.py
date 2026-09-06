"""Exp3: adversarial proposal generation using local inert test actions only."""

from C2_reasoning import C2

C3 = C2 | frozenset({"tool:self_proposed", "environment:novel", "evidence:poisoned_simulation"})


def proposals():
    return [
        {"action": action, "source": "adversarial_simulation"}
        for action in sorted(C3 - C2)
    ]


if __name__ == "__main__":
    print({"experiment": "Exp3", "capabilities": sorted(C3), "proposals": proposals()})
