#!/usr/bin/env python3
"""Verify core KairoSeed governance invariants in a record."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("record", type=Path)
    args = parser.parse_args()

    record = json.loads(args.record.read_text(encoding="utf-8"))
    required = [
        "record_version", "id", "request", "capability",
        "authorization", "execution", "meta", "links",
    ]
    missing = [key for key in required if key not in record]
    if missing:
        raise SystemExit(f"FAIL missing fields: {', '.join(missing)}")

    decision = record["authorization"]["decision"]
    executed = record["execution"]["executed"]
    immutable = record["meta"]["immutable"]

    if decision == "DENY" and executed:
        raise SystemExit("FAIL invariant: DENY must never execute")
    if not immutable:
        raise SystemExit("FAIL invariant: evidence must be marked immutable")
    if decision == "ALLOW" and executed:
        outcome = record["execution"].get("execution_outcome")
        if outcome not in {"success", "failure", "partial"}:
            raise SystemExit("FAIL: executed record has no terminal execution outcome")

    print("PASS governance record")
    print(f"record_id={record['id']}")
    print(f"decision={decision}")
    print(f"executed={executed}")
    print("invariant=CAPABILITY != PERMISSION")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
