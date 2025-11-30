#!/usr/bin/env bash
set -euo pipefail

# Usage: ./ci/generate_project.sh [PROJECT_SLUG] [PROJECT_NAME] [OUTPUT_DIR] [COOKIECUTTER_REF]
# Defaults:
PROJECT_SLUG=${1:-ci_generated}
PROJECT_NAME=${2:-"CI Generated Project"}
OUTPUT_DIR=${3:-./generated}
COOKIECUTTER_REF=${4:-f-django-rq-intg}

echo "Generating project from cookiecutter ref '${COOKIECUTTER_REF}' into ${OUTPUT_DIR}"

mkdir -p "${OUTPUT_DIR}"

cookiecutter "https://github.com/millsks/cookiecutter-django@${COOKIECUTTER_REF}" \
  --no-input \
  use_rq=yes \
  project_name="${PROJECT_NAME}" \
  project_slug="${PROJECT_SLUG}" \
  output-dir "${OUTPUT_DIR}"

echo "Project generation complete: ${OUTPUT_DIR}/${PROJECT_SLUG}"