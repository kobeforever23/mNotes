#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
python scripts/run_smoke_check.py || true

echo "Setup complete."
echo "Activate env with: source $ROOT/.venv/bin/activate"
echo "Launch app with: python $ROOT/main.py"
