#!/usr/bin/env python3
"""Package an explicit documentation/workflow allowlist; never authorize actions."""

import argparse
import hashlib
import io
import json
import re
import subprocess
import sys
import zipfile
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parents[1]
CONFIG = "release/context-release.json"


class ReleaseError(ValueError):
    pass


def digest(data):
    return hashlib.sha256(data).hexdigest()


def json_bytes(value):
    return (json.dumps(value, sort_keys=True, indent=2, ensure_ascii=False) + "\n").encode()


def safe_name(name):
    if not isinstance(name, str) or not name or "\\" in name:
        raise ReleaseError("Invalid package path")
    p = PurePosixPath(name)
    if p.is_absolute() or str(p) != name or any(x in {".", ".."} for x in p.parts):
        raise ReleaseError(f"Unsafe package path: {name}")
    return p


def read_file(root, name):
    parts = safe_name(name).parts
    path = root
    for part in parts:
        path = path / part
        if path.is_symlink():
            raise ReleaseError(f"Symlink is not a release input: {name}")
    if not path.is_file():
        raise ReleaseError(f"Missing release input: {name}")
    return path.read_bytes()


def snapshot(root=ROOT):
    root = Path(root).resolve()
    config_bytes = read_file(root, CONFIG)
    config = json.loads(config_bytes)
    if config.get("schema_version") != 1 or config.get("scope") != "documentation-and-local-workflow":
        raise ReleaseError("Unsupported schema or release scope")
    if not re.fullmatch(r"context-workflow-v[0-9]+\.[0-9]+\.[0-9]+", config.get("release_id", "")):
        raise ReleaseError("Release ID must be context-workflow-vMAJOR.MINOR.PATCH")
    names = config.get("files")
    if not isinstance(names, list) or not names or not all(isinstance(n, str) for n in names):
        raise ReleaseError("An explicit file allowlist is required")
    if len(set(names)) != len(names) or "MANIFEST.json" in names:
        raise ReleaseError("Duplicate or reserved package path")
    foundation = config.get("foundation", {})
    if not {CONFIG, config.get("notes"), foundation.get("path")}.issubset(names):
        raise ReleaseError("Config, notes, and foundation must be packaged")
    data = {name: read_file(root, name) for name in sorted(names)}
    if data[CONFIG] != config_bytes:
        raise ReleaseError("Release config changed during preparation")
    if digest(data[foundation["path"]]) != foundation.get("sha256"):
        raise ReleaseError("Foundation bytes differ from the recorded baseline")
    return config, data


def require_commit(root, source_commit, data):
    if source_commit == "UNCOMMITTED":
        return
    if not re.fullmatch(r"[0-9a-f]{40}", source_commit):
        raise ReleaseError("Supply a full Git commit or UNCOMMITTED")

    def git(*args):
        result = subprocess.run(["git", "-C", str(root), *args], capture_output=True, check=False)
        if result.returncode:
            raise ReleaseError("Cannot verify release inputs against the supplied Git commit")
        return result.stdout

    if git("rev-parse", "HEAD").decode().strip() != source_commit:
        raise ReleaseError("HEAD differs from the supplied commit")
    for name, content in data.items():
        if git("show", f"{source_commit}:{name}") != content:
            raise ReleaseError(f"Uncommitted release input: {name}")


def build(root, out, source_commit):
    root, out = Path(root).resolve(), Path(out).resolve()
    config, data = snapshot(root)
    if out == root or root.is_relative_to(out) or any((root / n).is_relative_to(out) for n in data):
        raise ReleaseError("Output directory overlaps release inputs")
    require_commit(root, source_commit, data)
    manifest = {
        "schema_version": 1,
        "release_id": config["release_id"],
        "scope": config["scope"],
        "source_commit": source_commit,
        "build_kind": "LOCAL_PREPARATION" if source_commit == "UNCOMMITTED" else "COMMIT_BOUND_PACKAGE",
        "independent_verification": "NOT_ASSESSED",
        "files": [{"path": n, "bytes": len(b), "sha256": digest(b)} for n, b in data.items()],
    }
    manifest_data = json_bytes(manifest)
    stream = io.BytesIO()
    with zipfile.ZipFile(stream, "w", compression=zipfile.ZIP_STORED) as archive:
        for name, content in sorted({**data, "MANIFEST.json": manifest_data}.items()):
            info = zipfile.ZipInfo(name, date_time=(1980, 1, 1, 0, 0, 0))
            info.create_system = 3
            info.external_attr = 0o100644 << 16
            archive.writestr(info, content)
    archive_name = config["release_id"] + ".zip"
    outputs = {archive_name: stream.getvalue(), "MANIFEST.json": manifest_data}
    outputs["SHA256SUMS"] = "".join(f"{digest(b)}  {n}\n" for n, b in outputs.items()).encode()
    out.mkdir(parents=True, exist_ok=True)
    for name, content in outputs.items():
        path = out / name
        if path.is_symlink() or (path.exists() and path.read_bytes() != content):
            raise ReleaseError(f"Refusing to replace different output: {name}")
    for name, content in outputs.items():
        (out / name).write_bytes(content)
    return {"archive": str(out / archive_name), "sha256": digest(stream.getvalue()), "source_commit": source_commit}


def check_archive(path, expected_sha256=None):
    raw = Path(path).read_bytes()
    if expected_sha256 is not None and digest(raw) != expected_sha256:
        raise ReleaseError("Archive differs from the expected external digest")
    with zipfile.ZipFile(io.BytesIO(raw)) as archive:
        names = archive.namelist()
        if len(names) != len(set(names)) or "MANIFEST.json" not in names:
            raise ReleaseError("Missing manifest or duplicate archive entry")
        for name in names:
            safe_name(name)
            if (archive.getinfo(name).external_attr >> 16) & 0o170000 == 0o120000:
                raise ReleaseError("Archive contains a symlink")
        manifest = json.loads(archive.read("MANIFEST.json"))
        if manifest.get("schema_version") != 1 or manifest.get("scope") != "documentation-and-local-workflow":
            raise ReleaseError("Unsupported archive manifest")
        records = manifest["files"]
        expected = [record["path"] for record in records]
        if len(set(expected)) != len(expected) or set(names) != set(expected) | {"MANIFEST.json"}:
            raise ReleaseError("Archive members differ from the manifest")
        for record in records:
            content = archive.read(record["path"])
            if len(content) != record["bytes"] or digest(content) != record["sha256"]:
                raise ReleaseError(f"Archive integrity mismatch: {record['path']}")
    return {"integrity": "PASS", "files": len(records), "sha256": digest(raw), "source_commit": manifest["source_commit"], "independent_verification": "NOT_ASSESSED"}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("verify")
    bp = sub.add_parser("build")
    bp.add_argument("--source-commit", required=True)
    bp.add_argument("--out", type=Path, required=True)
    cp = sub.add_parser("check")
    cp.add_argument("archive", type=Path)
    cp.add_argument("--sha256")
    args = parser.parse_args()
    try:
        if args.command == "verify":
            config, data = snapshot()
            result = {"input_check": "PASS", "release_id": config["release_id"], "files": len(data), "foundation_bytes_preserved": True}
        elif args.command == "build":
            result = build(ROOT, args.out, args.source_commit)
        else:
            result = check_archive(args.archive, args.sha256)
    except (ReleaseError, OSError, ValueError, KeyError, TypeError, zipfile.BadZipFile) as exc:
        print(json.dumps({"result": "BLOCK", "reason": str(exc)}), file=sys.stderr)
        return 1
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
