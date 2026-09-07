#!/usr/bin/env python3
"""
Lightweight verification instrument:
- Accepts a root directory to scan for YAML workflow files.
- Looks for the specific problematic pattern 'decision: authorized' and other simple invariants.
- Produces evidence JSON with campaign, observations, assertions, metrics, reproducible flag.
"""
import os
import re
import json
import argparse
import sys


def find_workflow_violations(root):
    obs = []
    wf_dir = os.path.join(root, '.github', 'workflows')
    candidates = []
    # if root is a temp dir containing specific files, check all files directly
    if os.path.isdir(wf_dir):
        for rootdir, _, files in os.walk(wf_dir):
            for fname in files:
                path = os.path.join(rootdir, fname)
                candidates.append(path)
    else:
        # if no workflows dir, scan all .yml/.yaml files in root
        for fname in os.listdir(root):
            if fname.endswith(('.yml', '.yaml')):
                candidates.append(os.path.join(root, fname))
    for path in candidates:
        try:
            with open(path, 'r', encoding='utf-8') as f:
                txt = f.read()
        except Exception:
            continue
        if re.search(r"decision\s*:\s*[\'\"]?authorized[\'\"]?", txt, re.IGNORECASE):
            obs.append({'path': path, 'reason': 'decision: authorized found'})
    return obs


def build_evidence(campaign, observations):
    assertions = []
    n = len(observations)
    assertions.append({
        'name': 'no-authorized-decision',
        'type': 'equality',
        'expected': 0,
        'actual': n,
        'pass': (n == 0),
        'severity': 'blocker' if n > 0 else 'ok',
        'note': 'The workflow emitted a decision labeled "authorized" which couples authority & executor.'
    })
    evidence = {
        'campaign': campaign,
        'observations': observations,
        'assertions': assertions,
        'metrics': {'observations_count': n},
        'reproducible': True
    }
    return evidence


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--root', default='.')
    p.add_argument('--out', required=True)
    p.add_argument('--campaign', required=True)
    args = p.parse_args()

    obs = find_workflow_violations(args.root)
    evidence = build_evidence(args.campaign, obs)
    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    with open(args.out, 'w', encoding='utf-8') as f:
        json.dump(evidence, f, indent=2)
    failed = any(not a['pass'] for a in evidence['assertions'])
    if failed:
        print("Verifier: assertions failed", file=sys.stderr)
        return 2
    print("Verifier: passed")
    return 0


if __name__ == '__main__':
    sys.exit(main())
