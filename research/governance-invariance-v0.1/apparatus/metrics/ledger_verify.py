"""Ledger verification helpers for the research apparatus."""

from aewa import reconstructable


def verify(records: list[dict]) -> dict:
    return {
        "reconstructable": reconstructable(records),
        "records": len(records),
    }
