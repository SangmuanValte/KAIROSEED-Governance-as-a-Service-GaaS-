"""Metadata preflight for the KAIROSEED evidence dossier.

Checks only document structure and source links. This is NOT an independent
runtime verifier, a security test, a formal proof, or production permission.
"""

from __future__ import annotations

import json
from pathlib import Path
import sys

ALLOWED = {"SPECIFIED", "CODE_PRESENT", "CI_FAILED", "NOT_VERIFIED"}
REQUIRED = {"id", "status", "statement", "scope", "evidence", "missing"}


def check_claims(data: object, repo_root: Path) -> list[str]:
    problems: list[str] = []
    if not isinstance(data, dict):
        return ["dossier must be a JSON object"]
    if data.get("schema") != "kairoseed-research-dossier-v0.1":
        problems.append("unexpected or missing schema")
    if data.get("assurance") != "NOT_VERIFIED":
        problems.append("dossier may not self-issue an assurance verdict")
    if data.get("canonical_specification") != "FROZEN_UNCHANGED":
        problems.append("canonical freeze state must remain explicit")

    entries = data.get("claims")
    if not isinstance(entries, list) or not entries:
        return problems + ["claims must be a nonempty list"]

    seen: set[str] = set()
    for index, claim in enumerate(entries):
        prefix = f"claims[{index}]"
        if not isinstance(claim, dict):
            problems.append(f"{prefix}: must be an object")
            continue
        missing = REQUIRED - claim.keys()
        if missing:
            problems.append(f"{prefix}: missing {sorted(missing)}")
            continue
        identifier = claim["id"]
        if not isinstance(identifier, str) or not identifier.strip():
            problems.append(f"{prefix}: invalid claim ID")
        elif identifier in seen:
            problems.append(f"{prefix}: duplicate claim ID {identifier}")
        else:
            seen.add(identifier)

        if claim["status"] not in ALLOWED:
            problems.append(f"{prefix}: status is not an allowed research label")
        for key in ("statement", "scope", "missing"):
            if not isinstance(claim[key], str) or not claim[key].strip():
                problems.append(f"{prefix}: {key} must be specific and nonempty")
        sources = claim["evidence"]
        if not isinstance(sources, list) or not sources:
            problems.append(f"{prefix}: source references required")
            continue
        for source in sources:
            if not isinstance(source, str) or not source.strip():
                problems.append(f"{prefix}: blank or invalid source")
            elif source.startswith("https://"):
                if not source.startswith("https://github.com/"):
                    problems.append(f"{prefix}: only repository evidence links supported")
            elif source.startswith("/") or ".." in Path(source).parts:
                problems.append(f"{prefix}: unsafe source path")
            elif not (repo_root / source).is_file():
                problems.append(f"{prefix}: missing repository source {source}")
    return problems


def main() -> int:
    root = Path(__file__).resolve().parents[2]
    manifest = root / "docs/research/evidence-dossier-2026-11-06/claims.json"
    data = json.loads(manifest.read_text(encoding="utf-8"))
    errors = check_claims(data, root)
    if errors:
        for error in errors:
            print(f"DOCUMENTATION_ERROR: {error}")
        return 1
    print(
        f"DOCUMENTATION_PREFLIGHT_OK: {len(data['claims'])} research claims; "
        "no operational assurance verdict issued"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
