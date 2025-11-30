#!/usr/bin/env bash
set -euo pipefail

GEN_DIR=${1:-./generated/ci_generated}

echo "Installing project dependencies and running migrations/tests in generated project: ${GEN_DIR}"

if [ ! -d "${GEN_DIR}" ]; then
  echo "Generated project directory ${GEN_DIR} not found. Run ./ci/generate_project.sh first."
  exit 2
fi

# Use pixi to create env and install requirements
if command -v pixi >/dev/null 2>&1; then
  echo "Running pixi install..."
  pixi install
else
  echo "pixi not found; installing pixi into runner..."
  python -m pip install --upgrade pip
  python -m pip install pixi
  pixi install
fi

echo "Running migrations..."
pixi run -- python manage.py migrate

echo "Running unit tests..."
pixi run -- python manage.py test

echo "Tests finished"