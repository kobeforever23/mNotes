#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

if [[ ! -d ".venv" ]]; then
  echo "Missing .venv. Run scripts/setup_local_env.sh first."
  exit 1
fi

source .venv/bin/activate
python main.py
