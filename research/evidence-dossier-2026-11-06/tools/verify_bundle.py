#!/usr/bin/env python3
"""Offline consistency checks for a KAIROSEED research evidence bundle.

This verifies JSON structure, claim/test bindings, and SHA-256 file integrity.
It CANNOT establish trusted chronology, independent observation, complete
mediation, protected-effect noninterference, or production permission.

Exit 0: BUNDLE_STRUCTURALLY_VALID; assurance remains NOT_VERIFIED.
Exit 2: bundle invalid or inconsistent; assurance remains NOT_VERIFIED.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
from typing import Any


class BundleValidationError(ValueError):
    """A declared structural or file-integrity condition is unsatisfied."""


_SHA256 = re.compile(r"^[0-9a-f]{64}$")
_ALLOWED = {"CONFIRMED_WITHIN_SCOPE", "CONTRADICTED", "INCONCLUSIVE"}


def _no_duplicate_keys(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    obj: dict[str, Any] = {}
    for key, value in pairs:
        if key in obj:
            raise BundleValidationError(f"duplicate JSON key: {key}")
        obj[key] = value
    return obj


def _document(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"),
                          object_pairs_hook=_no_duplicate_keys)
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise BundleValidationError(f"cannot read valid JSON: {path.name}") from exc


def _require_mapping(value: Any, label: str) -> dict[str, Any]:
    if type(value) is not dict:
        raise BundleValidationError(f"{label} must be an object")
    return value


def _text(value: Any, label: str) -> str:
    if type(value) is not str or not value.strip():
        raise BundleValidationError(f"{label} must be nonempty text")
    return value


def _digest(value: Any, label: str) -> str:
    if type(value) is not str or not _SHA256.fullmatch(value):
        raise BundleValidationError(f"{label} must be lowercase SHA-256 hex")
    return value


def _safe_file(root: Path, name: Any) -> Path:
    value = _text(name, "filename")
    # Flat, relative, literal names only. No symlinks, traversal or URI.
    if value in (".", "..") or Path(value).name != value or "\\" in value or ":" in value:
        raise BundleValidationError(f"unsafe evidence filename: {value!r}")
    file = root / value
    if file.is_symlink() or not file.is_file() or file.resolve().parent != root.resolve():
        raise BundleValidationError(f"evidence file missing or unsafe: {value}")
    return file


def _sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def validate(root: Path) -> dict[str, Any]:
    root = root.resolve()
    manifest = _require_mapping(_document(_safe_file(root, "manifest.json")), "manifest")
    if manifest.get("schema_version") != "1.0":
        raise BundleValidationError("manifest.schema_version must equal '1.0'")
    claims_file = _safe_file(root, manifest.get("claims_file"))
    claims_digest = _digest(manifest.get("claims_sha256"), "claims_sha256")
    if _sha(claims_file) != claims_digest:
        raise BundleValidationError("claims file hash mismatch")
    claim_set = _require_mapping(_document(claims_file), "claim set")
    if claim_set.get("schema_version") != "1.0":
        raise BundleValidationError("claim_set.schema_version must equal '1.0'")
    claims = claim_set.get("claims")
    if type(claims) is not list or not claims:
        raise BundleValidationError("claim set must contain claims")
    ids: set[str] = set()
    for claim in claims:
        claim = _require_mapping(claim, "claim")
        cid = _text(claim.get("id"), "claim.id")
        for field in ("statement", "scope", "falsifier"):
            _text(claim.get(field), f"{cid}.{field}")
        assumptions = claim.get("assumptions")
        if type(assumptions) is not list or any(type(x) is not str for x in assumptions):
            raise BundleValidationError(f"{cid}.assumptions must be a text list")
        if cid in ids:
            raise BundleValidationError(f"duplicate claim ID: {cid}")
        ids.add(cid)
    tests = manifest.get("tests")
    if type(tests) is not list or not tests:
        raise BundleValidationError("manifest must include at least one test")
    seen: set[str] = set()
    tested_claims: set[str] = set()
    for case in tests:
        case = _require_mapping(case, "test case")
        tid = _text(case.get("test_id"), "test_id")
        if tid in seen:
            raise BundleValidationError(f"duplicate test ID: {tid}")
        seen.add(tid)
        cid = _text(case.get("claim_id"), "claim_id")
        if cid not in ids:
            raise BundleValidationError(f"{tid} references unknown claim {cid}")
        tested_claims.add(cid)
        if _digest(case.get("claim_set_sha256"), f"{tid}.claim_set_sha256") != claims_digest:
            raise BundleValidationError(f"{tid} references a different frozen claim set")
        if case.get("reported_result") not in _ALLOWED:
            raise BundleValidationError(f"{tid} has unknown reported_result")
        _text(case.get("scope"), f"{tid}.scope")
        _text(case.get("observer"), f"{tid}.observer")
        evidence = _safe_file(root, case.get("evidence_file"))
        if _sha(evidence) != _digest(case.get("evidence_sha256"), f"{tid}.evidence_sha256"):
            raise BundleValidationError(f"{tid}: evidence file hash mismatch")
    if ids != tested_claims:
        raise BundleValidationError("every frozen claim needs at least one test reference")
    return {
        "bundle_check": "BUNDLE_STRUCTURALLY_VALID",
        "assurance": "NOT_VERIFIED",
        "claim_set_sha256": claims_digest,
        "claims": len(ids),
        "tests": len(seen),
        "note": ("Hash and reference consistency only. No independent confirmation "
                 "of chronology, sensor coverage, protected effects or truth.")
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("bundle", type=Path, help="directory of JSON bundle files")
    args = parser.parse_args()
    try:
        result = validate(args.bundle)
    except (BundleValidationError, OSError) as exc:
        print(json.dumps({"bundle_check": "INVALID", "assurance": "NOT_VERIFIED",
                          "error": str(exc)}, sort_keys=True))
        return 2
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
