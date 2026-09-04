#!/usr/bin/env python3
"""Generate a compact KairoSeed governance record.

The script deliberately does not sign or publish records. Signing and persistence
remain explicit deployment steps so capability is never confused with permission.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import uuid
from datetime import datetime, timezone
from pathlib import Path


def now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def sha256_json(record: dict) -> str:
    payload = json.dumps(record, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def build_record(args: argparse.Namespace) -> dict:
    timestamp = now()
    return {
        "record_version": "1.0",
        "id": str(uuid.uuid4()),
        "request": {
            "type": args.action,
            "requester": args.requester,
            "request_context": {"pr": args.pr} if args.pr else {},
        },
        "capability": {
            "capability_id": args.capability_id,
            "source_repo": args.source_repo,
            "source_commit": args.source_commit,
            "branch": args.branch,
        },
        "authorization": {
            "decision": args.decision,
            "policy_id": args.policy_id,
            "reviewer": args.reviewer,
            "reviewer_role": args.reviewer_role,
            "timestamp": timestamp,
            "reason": args.reason,
        },
        "execution": {
            "executed": False,
            "execution_start": None,
            "execution_end": None,
            "executor": args.executor,
            "execution_outcome": "blocked" if args.decision == "DENY" else "skipped",
        },
        "links": {"pr": args.pr} if args.pr else {},
        "meta": {
            "created_at": timestamp,
            "created_by": args.created_by,
            "immutable": True,
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--action", default="deploy")
    parser.add_argument("--requester", required=True)
    parser.add_argument("--capability-id", required=True)
    parser.add_argument("--source-repo", required=True)
    parser.add_argument("--source-commit", required=True)
    parser.add_argument("--branch", default="main")
    parser.add_argument("--decision", choices=["ALLOW", "DENY"], required=True)
    parser.add_argument("--policy-id", required=True)
    parser.add_argument("--reviewer", required=True)
    parser.add_argument("--reviewer-role", default="reviewer")
    parser.add_argument("--reason", required=True)
    parser.add_argument("--executor", default="github-actions")
    parser.add_argument("--created-by", default="governance-service")
    parser.add_argument("--pr", type=int)
    parser.add_argument("--output", default="record.json")
    args = parser.parse_args()

    record = build_record(args)
    digest = sha256_json(record)
    Path(args.output).write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
    print(f"record_id={record['id']}")
    print(f"record_sha256={digest}")
    print(f"decision={record['authorization']['decision']}")
    print(f"execution={record['execution']['execution_outcome']}")


if __name__ == "__main__":
    main()
