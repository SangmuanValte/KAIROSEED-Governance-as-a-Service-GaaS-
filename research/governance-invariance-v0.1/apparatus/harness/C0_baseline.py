"""Exp0: deterministic baseline capability set."""

C0 = frozenset({"echo:return"})


def proposals():
    return [{"action": "echo:return", "source": "baseline"}]


if __name__ == "__main__":
    print({"experiment": "Exp0", "capabilities": sorted(C0), "proposals": proposals()})
