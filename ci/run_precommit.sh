#!/usr/bin/env bash
set -euo pipefail

GEN_DIR=${1:-./generated/ci_generated}

echo "Running pre-commit for repo..."
pre-commit run --all-files || true

echo "Running pre-commit for generated project: ${GEN_DIR}..."
if [ -f "${GEN_DIR}/.pre-commit-config.yaml" ]; then
  pre-commit run --config "${GEN_DIR}/.pre-commit-config.yaml" --all-files || true
else
  echo "No pre-commit config in generated project; skipping."
fi
