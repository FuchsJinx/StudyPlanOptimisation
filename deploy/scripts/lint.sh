#!/usr/bin/env bash
# Локальный lint (Linux/macOS / Git Bash)
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$ROOT"

echo "==> Python (ruff)"
if [[ -d main/backend ]] && compgen -G "main/backend/**/*.py" > /dev/null 2>&1; then
  python -m ruff check main/backend --config deploy/lint/ruff.toml
  python -m ruff format main/backend --check --config deploy/lint/ruff.toml
else
  echo "skip: нет Python-файлов в main/backend"
fi

echo "==> Frontend (eslint)"
if [[ -f main/frontend/package.json ]]; then
  (cd main/frontend && npm run lint)
else
  echo "skip: нет package.json в main/frontend"
fi

echo "Lint OK"
