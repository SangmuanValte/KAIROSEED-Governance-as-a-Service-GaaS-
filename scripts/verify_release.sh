#!/usr/bin/env bash
set -euo pipefail

echo "[1/3] Python reference tests"
python -m pytest -q

echo "[2/3] Adversarial authorization-boundary tests"
python -m pytest -q tests/adversarial

echo "[3/3] Safe example"
python examples/authorized_unauthorized.py

echo "Verification completed for the Python reference path."
echo "This script does not establish production security, complete mediation, concurrency safety, or durable evidence."
