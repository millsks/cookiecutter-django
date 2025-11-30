#!/usr/bin/env bash
set -euo pipefail

GEN_DIR=${1:-./generated/ci_generated}
PROJECT_MODULE=$(basename "${GEN_DIR}")

echo "Running integration checks in ${GEN_DIR}"
if [ ! -d "${GEN_DIR}" ]; then
  echo "Generated project directory ${GEN_DIR} not found. Run ./ci/generate_project.sh first."
  exit 2
fi

pushd "${GEN_DIR}"

# Ensure DJANGO_SETTINGS_MODULE points to the generated project settings
export DJANGO_SETTINGS_MODULE="${PROJECT_MODULE}.settings"

# Run migrations to ensure DB is initialized
echo "Running migrations in generated project..."
if command -v pixi >/dev/null 2>&1; then
  pixi run -- python manage.py migrate
else
  python -m pip install --upgrade pip
  python -m pip install pixi
  pixi install
  pixi run -- python manage.py migrate
fi

# Start an rq worker in the background so it can pick up jobs
echo "Starting rqworker in background..."
pixi run -- python manage.py rqworker &>/tmp/ci_rqworker.log &
WORKER_PID=$!

echo "Waiting briefly for worker to initialize..."
sleep 5

# Enqueue a simple test job (adds two numbers) and capture job id
echo "Enqueueing a test job..."
JOB_ID=$(pixi run -- python manage.py shell -c "from django_rq import get_queue; q=get_queue('default'); job = q.enqueue(lambda a,b: a+b, 2, 3); print(job.id)") || true
JOB_ID=$(echo "${JOB_ID}" | tr -d '\r' | tr -d '\n')

if [ -z "${JOB_ID}" ]; then
  echo "Failed to enqueue a job; capturing logs and exiting..."
  tail -n +1 /tmp/ci_rqworker.log || true
  kill ${WORKER_PID} || true
  popd
  exit 3
fi

echo "Enqueued job id: ${JOB_ID}"

# Poll for job status (timeout after ~60 seconds)
SUCCESS=0
for i in {1..30}; do
  STATUS=$(pixi run -- python - <<PY
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', '${PROJECT_MODULE}.settings')
import django
django.setup()
from django_rq import get_queue
q=get_queue('default')
job=q.fetch_job('${JOB_ID}')
print(job.get_status() if job else 'missing')
PY
)
  STATUS=$(echo "${STATUS}" | tr -d '\r' | tr -d '\n')
  echo "Poll ${i}: job status=${STATUS}"
  if [[ "${STATUS}" == "finished" ]]; then
    echo "Job finished successfully"
    SUCCESS=1
    break
  fi
  if [[ "${STATUS}" == "failed" ]]; then
    echo "Job failed; printing worker logs..."
    tail -n +1 /tmp/ci_rqworker.log || true
    break
  fi
  sleep 2
done

# Clean up worker
kill ${WORKER_PID} || true
sleep 1 || true

if [ "${SUCCESS}" -ne 1 ]; then
  echo "Integration check failed (job did not finish successfully)"
  popd
  exit 4
fi

popd

echo "Integration checks passed"