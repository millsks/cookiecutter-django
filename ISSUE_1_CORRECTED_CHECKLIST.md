# Django-RQ Integration Testing & Review Checklist

## Overview

This checklist covers **11 phases** of testing to ensure the django-rq integration with Valkey is production-ready before submitting to cookiecutter-django maintainers.

---

## Phase 1: Pre-Generation Validation

### 1.1 Review Template Files

### 1.2 Review Documentation

- [ ] 1.2 Review Documentation: **docs/4-guides/using-django-rq.rst**: Review comprehensive guide for accuracy
- [ ] 1.2 Review Documentation: **docs/1-getting-started/project-generation-options.rst**: Check `use_rq` option is documented
- [ ] 1.2 Review Documentation: **docs/2-local-development/developing-locally-docker.rst**: Verify RQ section is present
- [ ] 1.2 Review Documentation: **docs/3-deployment/deployment-with-docker.rst**: Check Valkey service is mentioned

---

## Phase 2: Generate Test Projects

### Test Case 1: RQ Only (No Celery)

Generate a project with django-rq but without Celery:

```
cd /Users/millsks/UserLocal/apps/src/code/Public-Git/millsks
cookiecutter cookiecutter-django
```

**Generation options:**

- [ ] Phase 2 – Test Case 1: RQ Only (No Celery): `project_name`: Test RQ Only
- [ ] Phase 2 – Test Case 1: RQ Only (No Celery): `project_slug`: test_rq_only
- [ ] Phase 2 – Test Case 1: RQ Only (No Celery): `use_docker`: y
- [ ] Phase 2 – Test Case 1: RQ Only (No Celery): `use_celery`: n
- [ ] Phase 2 – Test Case 1: RQ Only (No Celery): `use_rq`: y
- [ ] Phase 2 – Test Case 1: RQ Only (No Celery): (Other options: defaults or your preference)

**Validate generated files:**

- [ ] Phase 2 – Test Case 1: RQ Only (No Celery): `docker-compose.local.yml` contains **valkey** service (NOT redis)
- [ ] Phase 2 – Test Case 1: RQ Only (No Celery): `docker-compose.local.yml` has `rqworker`, `rqscheduler`, `rqdashboard` services
- [ ] Phase 2 – Test Case 1: RQ Only (No Celery): `docker-compose.production.yml` contains **valkey** service (NOT redis)
- [ ] Phase 2 – Test Case 1: RQ Only (No Celery): `.envs/.local/.django` has `VALKEY_URL=valkey://valkey:6379/0`
- [ ] Phase 2 – Test Case 1: RQ Only (No Celery): `.envs/.production/.django` has `VALKEY_URL=valkey://valkey:6379/0`
- [ ] Phase 2 – Test Case 1: RQ Only (No Celery): `config/settings/base.py` has `VALKEY_URL` variable and `RQ_QUEUES` using it
- [ ] Phase 2 – Test Case 1: RQ Only (No Celery): `config/settings/base.py` does NOT have `REDIS_URL` variable
- [ ] Phase 2 – Test Case 1: RQ Only (No Celery): `compose/local/django/rq/` directory exists with `worker/start`, `scheduler/start`, `dashboard/start`
- [ ] Phase 2 – Test Case 1: RQ Only (No Celery): `compose/production/django/rq/` directory exists with same scripts
- [ ] Phase 2 – Test Case 1: RQ Only (No Celery): Scripts use `${VALKEY_URL}` not `${REDIS_URL}`
- [ ] Phase 2 – Test Case 1: RQ Only (No Celery): `test_rq_only/users/tasks.py` has `@django_rq.job` decorator
- [ ] Phase 2 – Test Case 1: RQ Only (No Celery): `test_rq_only/users/tests/test_tasks.py` has RQ test with `is_async=False`
- [ ] Phase 2 – Test Case 1: RQ Only (No Celery): `Procfile` has `worker:` and `scheduler:` processes

### Test Case 2: Celery Only (No RQ)

Generate a project with Celery but without django-rq:

```
cookiecutter cookiecutter-django
```

**Generation options:**

- [ ] Phase 2 – Test Case 2: Celery Only (No RQ): `project_name`: Test Celery Only
- [ ] Phase 2 – Test Case 2: Celery Only (No RQ): `project_slug`: test_celery_only
- [ ] Phase 2 – Test Case 2: Celery Only (No RQ): `use_docker`: y
- [ ] Phase 2 – Test Case 2: Celery Only (No RQ): `use_celery`: y
- [ ] Phase 2 – Test Case 2: Celery Only (No RQ): `use_rq`: n
- [ ] Phase 2 – Test Case 2: Celery Only (No RQ): (Other options: defaults)

**Validate generated files:**

- [ ] Phase 2 – Test Case 2: Celery Only (No RQ): `docker-compose.local.yml` contains **redis** service (NOT valkey)
- [ ] Phase 2 – Test Case 2: Celery Only (No RQ): `docker-compose.local.yml` has celery services, NO rq services
- [ ] Phase 2 – Test Case 2: Celery Only (No RQ): `.envs/.local/.django` has `REDIS_URL=redis://redis:6379/0`
- [ ] Phase 2 – Test Case 2: Celery Only (No RQ): `.envs/.local/.django` does NOT have `VALKEY_URL`
- [ ] Phase 2 – Test Case 2: Celery Only (No RQ): `config/settings/base.py` has `REDIS_URL` and Celery config
- [ ] Phase 2 – Test Case 2: Celery Only (No RQ): `config/settings/base.py` does NOT have RQ config or `VALKEY_URL`
- [ ] Phase 2 – Test Case 2: Celery Only (No RQ): `compose/local/django/rq/` directory does NOT exist
- [ ] Phase 2 – Test Case 2: Celery Only (No RQ): `compose/production/django/rq/` directory does NOT exist
- [ ] Phase 2 – Test Case 2: Celery Only (No RQ): `test_celery_only/users/tasks.py` has `@shared_task()` decorator
- [ ] Phase 2 – Test Case 2: Celery Only (No RQ): `test_celery_only/users/tests/test_tasks.py` has Celery test

### Test Case 3: Both RQ and Celery

Generate a project with BOTH:

```
cookiecutter cookiecutter-django
```

**Generation options:**

- [ ] Phase 2 – Test Case 3: Both RQ and Celery: `project_name`: Test Both Queues
- [ ] Phase 2 – Test Case 3: Both RQ and Celery: `project_slug`: test_both_queues
- [ ] Phase 2 – Test Case 3: Both RQ and Celery: `use_docker`: y
- [ ] Phase 2 – Test Case 3: Both RQ and Celery: `use_celery`: y
- [ ] Phase 2 – Test Case 3: Both RQ and Celery: `use_rq`: y

**Validate generated files:**

- [ ] Phase 2 – Test Case 3: Both RQ and Celery: `docker-compose.local.yml` contains BOTH **redis** and **valkey** services
- [ ] Phase 2 – Test Case 3: Both RQ and Celery: `docker-compose.local.yml` has volumes for both: `test_both_queues_local_redis_data` and `test_both_queues_local_valkey_data`
- [ ] Phase 2 – Test Case 3: Both RQ and Celery: Django service `depends_on` includes both `redis` and `valkey`
- [ ] Phase 2 – Test Case 3: Both RQ and Celery: Celery services depend on `redis`
- [ ] Phase 2 – Test Case 3: Both RQ and Celery: RQ services depend on `valkey`
- [ ] Phase 2 – Test Case 3: Both RQ and Celery: `.envs/.local/.django` has BOTH `REDIS_URL` (for Celery) and `VALKEY_URL` (for RQ)
- [ ] Phase 2 – Test Case 3: Both RQ and Celery: `config/settings/base.py` has both `REDIS_URL` and `VALKEY_URL` variables
- [ ] Phase 2 – Test Case 3: Both RQ and Celery: `config/settings/base.py` has Celery config using `REDIS_URL`
- [ ] Phase 2 – Test Case 3: Both RQ and Celery: `config/settings/base.py` has RQ config using `VALKEY_URL`
- [ ] Phase 2 – Test Case 3: Both RQ and Celery: Both `compose/local/django/celery/` and `compose/local/django/rq/` directories exist

### Test Case 4: Neither (Baseline)

Generate a project with no task queues:

```
cookiecutter cookiecutter-django
```

**Generation options:**

- [ ] Phase 2 – Test Case 4: Neither (Baseline): `project_name`: Test No Queues
- [ ] Phase 2 – Test Case 4: Neither (Baseline): `project_slug`: test_no_queues
- [ ] Phase 2 – Test Case 4: Neither (Baseline): `use_docker`: y
- [ ] Phase 2 – Test Case 4: Neither (Baseline): `use_celery`: n
- [ ] Phase 2 – Test Case 4: Neither (Baseline): `use_rq`: n

**Validate generated files:**

- [ ] Phase 2 – Test Case 4: Neither (Baseline): `docker-compose.local.yml` has NO redis or valkey services
- [ ] Phase 2 – Test Case 4: Neither (Baseline): `.envs/.local/.django` has NO REDIS_URL or VALKEY_URL
- [ ] Phase 2 – Test Case 4: Neither (Baseline): `config/settings/base.py` has NO queue-related configuration
- [ ] Phase 2 – Test Case 4: Neither (Baseline): No `compose/*/django/celery/` or `compose/*/django/rq/` directories
- [ ] Phase 2 – Test Case 4: Neither (Baseline): `test_no_queues/users/tasks.py` has simple non-decorated function

---

## Phase 3: Local Development Testing (Test Case 1: RQ Only)

Work with the `test_rq_only` project for these tests:

```
cd test_rq_only
```

### 3.1 Docker Compose Startup

```
docker compose -f docker-compose.local.yml up --build
```

**Verify:**

- [ ] Phase 3 – 3.1 Docker Compose Startup: All services start without errors
- [ ] Phase 3 – 3.1 Docker Compose Startup: `valkey` service is running on port 6379
- [ ] Phase 3 – 3.1 Docker Compose Startup: `rqworker` service starts and logs "Listening on queues: default, high, low"
- [ ] Phase 3 – 3.1 Docker Compose Startup: `rqscheduler` service starts successfully
- [ ] Phase 3 – 3.1 Docker Compose Startup: `rqdashboard` service starts on port 9181
- [ ] Phase 3 – 3.1 Docker Compose Startup: NO redis service is running (since use_celery=n)
- [ ] Phase 3 – 3.1 Docker Compose Startup: Django app accessible at [http://localhost:8000](http://localhost:8000)

### 3.2 Service Health Checks

```
# Check running containers
docker compose -f docker-compose.local.yml ps

# Check Valkey connection
docker compose -f docker-compose.local.yml exec django python manage.py shell
```

In Django shell:

```
import django_rq
queue = django_rq.get_queue("default")
print(queue.connection)  # Should show valkey connection
print(queue.count)  # Should return 0 initially
exit()
```

**Verify:**

- [ ] Phase 3 – 3.2 Service Health Checks: Valkey connection successful
- [ ] Phase 3 – 3.2 Service Health Checks: No connection errors in logs

### 3.3 RQ Dashboard Access

Open [http://localhost:9181](http://localhost:9181)

**Verify:**

- [ ] Phase 3 – 3.3 RQ Dashboard Access: Dashboard loads without errors
- [ ] Phase 3 – 3.3 RQ Dashboard Access: Shows 3 queues: default, high, low
- [ ] Phase 3 – 3.3 RQ Dashboard Access: Shows workers count (should be 1+)
- [ ] Phase 3 – 3.3 RQ Dashboard Access: Shows 0 jobs initially

### 3.4 Enqueue and Process Test Job

```
docker compose -f docker-compose.local.yml exec django python manage.py shell
```

In Django shell:

```
from test_rq_only.users.tasks import get_users_count
import django_rq

# Enqueue the example job
job = get_users_count.delay()
print(f"Job ID: {job.id}")
print(f"Job status: {job.get_status()}")

# Wait a moment, then check result
import time
time.sleep(2)
job.refresh()
print(f"Job status: {job.get_status()}")
print(f"Job result: {job.result}")
exit()
```

**Verify:**

- [ ] Phase 3 – 3.4 Enqueue and Process Test Job: Job enqueued successfully
- [ ] Phase 3 – 3.4 Enqueue and Process Test Job: Job status changes to 'finished'
- [ ] Phase 3 – 3.4 Enqueue and Process Test Job: Job result is an integer (user count)
- [ ] Phase 3 – 3.4 Enqueue and Process Test Job: Worker logs show job processing
- [ ] Phase 3 – 3.4 Enqueue and Process Test Job: Dashboard shows job in "Finished" tab

### 3.5 Test Scheduled Jobs

In Django shell:

```
import django_rq
from datetime import timedelta
from test_rq_only.users.tasks import get_users_count

queue = django_rq.get_queue("default")
# Schedule job for 30 seconds from now
job = queue.enqueue_in(timedelta(seconds=30), get_users_count)
print(f"Scheduled job ID: {job.id}")
exit()
```

**Verify:**

- [ ] Phase 3 – 3.5 Test Scheduled Jobs: Job appears in Dashboard under "Scheduled" tab
- [ ] Phase 3 – 3.5 Test Scheduled Jobs: After 30 seconds, job moves to "Finished"
- [ ] Phase 3 – 3.5 Test Scheduled Jobs: Scheduler logs show job execution

### 3.6 Test Multiple Queues

In Django shell:

```
import django_rq

# Enqueue to high priority queue
high_queue = django_rq.get_queue("high")
job1 = high_queue.enqueue("test_rq_only.users.tasks.get_users_count")

# Enqueue to low priority queue
low_queue = django_rq.get_queue("low")
job2 = low_queue.enqueue("test_rq_only.users.tasks.get_users_count")

print(f"High priority job: {job1.id}")
print(f"Low priority job: {job2.id}")
exit()
```

**Verify:**

- [ ] Phase 3 – 3.6 Test Multiple Queues: Jobs appear in correct queues in Dashboard
- [ ] Phase 3 – 3.6 Test Multiple Queues: Both jobs are processed successfully

### 3.7 Test Hot Reload

Make a change to `test_rq_only/users/tasks.py`:

```python
@django_rq.job
def get_users_count():
    """Test job that returns user count."""
    print("TESTING HOT RELOAD!")  # Add this line
    from test_rq_only.users.models import User
    return User.objects.count()
```

**Verify:**

- [ ] Phase 3 – 3.7 Test Hot Reload: Worker container restarts automatically (check logs)
- [ ] Phase 3 – 3.7 Test Hot Reload: New jobs show the updated log message
- [ ] Phase 3 – 3.7 Test Hot Reload: No manual restart required

### 3.8 Run Unit Tests

```
docker compose -f docker-compose.local.yml exec django pytest
```

**Verify:**

- [ ] Phase 3 – 3.8 Run Unit Tests: All tests pass, including `test_rq_only/users/tests/test_tasks.py`
- [ ] Phase 3 – 3.8 Run Unit Tests: RQ test uses synchronous mode (jobs execute immediately)
- [ ] Phase 3 – 3.8 Run Unit Tests: No failures related to queue configuration

---

## Phase 4: Production Configuration Testing

Still using `test_rq_only` project:

### 4.1 Review Production Docker Compose

```
cat docker-compose.production.yml
```

**Verify:**

- [ ] Phase 4 – 4.1 Review Production Docker Compose: Contains `valkey` service with correct image: `docker.io/valkey/valkey:8.0`
- [ ] Phase 4 – 4.1 Review Production Docker Compose: Volume `production_valkey_data` is defined
- [ ] Phase 4 – 4.1 Review Production Docker Compose: `rqworker`, `rqscheduler`, `rqdashboard` services are present
- [ ] Phase 4 – 4.1 Review Production Docker Compose: RQ services use correct command paths (`/start-rqworker`, etc.)
- [ ] Phase 4 – 4.1 Review Production Docker Compose: NO redis service present (since use_celery=n)

### 4.2 Review Production Environment Variables

```
cat .envs/.production/.django
```

**Verify:**

- [ ] Phase 4 – 4.2 Review Production Environment Variables: Contains `VALKEY_URL=valkey://valkey:6379/0`
- [ ] Phase 4 – 4.2 Review Production Environment Variables: Does NOT contain `REDIS_URL` (since use_celery=n)
- [ ] Phase 4 – 4.2 Review Production Environment Variables: Placeholder values for other settings present

### 4.3 Test Production Build (Optional)

```
docker compose -f docker-compose.production.yml build
```

**Verify:**

- [ ] Phase 4 – 4.3 Test Production Build (Optional): Build completes without errors
- [ ] Phase 4 – 4.3 Test Production Build (Optional): Django image includes RQ startup scripts
- [ ] Phase 4 – 4.3 Test Production Build (Optional): Script permissions are correct (executable)

---

## Phase 5: Dual Queue Testing (Test Case 3: Both)

Switch to `test_both_queues` project:

```
cd ../test_both_queues
docker compose -f docker-compose.local.yml up --build
```

### 5.1 Verify Service Separation

**Verify:**

- [ ] Phase 5 – 5.1 Verify Service Separation: Both `redis` and `valkey` services are running
- [ ] Phase 5 – 5.1 Verify Service Separation: Celery worker connects to redis
- [ ] Phase 5 – 5.1 Verify Service Separation: RQ worker connects to valkey
- [ ] Phase 5 – 5.1 Verify Service Separation: Flower accessible at [http://localhost:5555](http://localhost:5555)
- [ ] Phase 5 – 5.1 Verify Service Separation: RQ Dashboard accessible at [http://localhost:9181](http://localhost:9181)

### 5.2 Test Isolated Task Processing

```
docker compose -f docker-compose.local.yml exec django python manage.py shell
```

In Django shell:

```
# Test Celery task (should use Redis)
from test_both_queues.users.tasks import get_users_count
celery_result = get_users_count.delay()
print(f"Celery task: {celery_result.id}")

# Test RQ task (should use Valkey)
import django_rq
rq_job = django_rq.get_queue("default").enqueue("test_both_queues.users.tasks.get_users_count")
print(f"RQ job: {rq_job.id}")
exit()
```

**Verify:**

- [ ] Phase 5 – 5.2 Test Isolated Task Processing: Both tasks execute successfully
- [ ] Phase 5 – 5.2 Test Isolated Task Processing: Celery task appears in Flower ([http://localhost:5555](http://localhost:5555))
- [ ] Phase 5 – 5.2 Test Isolated Task Processing: RQ job appears in RQ Dashboard ([http://localhost:9181](http://localhost:9181))
- [ ] Phase 5 – 5.2 Test Isolated Task Processing: No cross-contamination (Celery doesn't see RQ jobs and vice versa)

### 5.3 Check Logs for Correct Backend Usage

```
# Check Celery worker logs
docker compose -f docker-compose.local.yml logs celeryworker | grep -i redis

# Check RQ worker logs  
docker compose -f docker-compose.local.yml logs rqworker | grep -i valkey
```

**Verify:**

- [ ] Phase 5 – 5.3 Check Logs for Correct Backend Usage: Celery worker logs show redis:6379 connection
- [ ] Phase 5 – 5.3 Check Logs for Correct Backend Usage: RQ worker logs show valkey:6379 connection
- [ ] Phase 5 – 5.3 Check Logs for Correct Backend Usage: No connection errors

---

## Phase 6: Documentation Review

### 6.1 Read Through All Documentation

- [ ] Phase 6 – 6.1 Read Through All Documentation: **docs/4-guides/using-django-rq.rst**: Read completely, check for typos/accuracy
- [ ] Phase 6 – 6.1 Read Through All Documentation: Verify all code examples are correct
- [ ] Phase 6 – 6.1 Read Through All Documentation: Check that architecture diagram makes sense
- [ ] Phase 6 – 6.1 Read Through All Documentation: Confirm troubleshooting section is helpful
- [ ] Phase 6 – 6.1 Read Through All Documentation: Validate external links work

### 6.2 Documentation Build Test

```
cd /Users/millsks/UserLocal/apps/src/code/Public-Git/millsks/cookiecutter-django
docker compose -f docker-compose.docs.yml up --build
```

**Verify:**

- [ ] Phase 6 – 6.2 Documentation Build Test: Docs build without errors
- [ ] Phase 6 – 6.2 Documentation Build Test: using-django-rq.rst renders correctly at [http://localhost:9000](http://localhost:9000)
- [ ] Phase 6 – 6.2 Documentation Build Test: No Sphinx warnings about the new file
- [ ] Phase 6 – 6.2 Documentation Build Test: Navigation includes the new guide
- [ ] Phase 6 – 6.2 Documentation Build Test: All internal references resolve

---

## Phase 7: Edge Cases and Error Handling

### 7.1 Test Failed Jobs

In Django shell:

```
import django_rq

def failing_task():
    raise Exception("Intentional failure for testing")

queue = django_rq.get_queue("default")
job = queue.enqueue(failing_task)
print(f"Job ID: {job.id}")

import time
time.sleep(2)
job.refresh()
print(f"Job status: {job.get_status()}")  # Should be 'failed'
print(f"Exception: {job.exc_info}")
exit()
```

**Verify:**

- [ ] Phase 7 – 7.1 Test Failed Jobs: Job status is 'failed'
- [ ] Phase 7 – 7.1 Test Failed Jobs: Exception info is captured
- [ ] Phase 7 – 7.1 Test Failed Jobs: Failed job appears in Dashboard "Failed" tab
- [ ] Phase 7 – 7.1 Test Failed Jobs: Worker doesn't crash

### 7.2 Test Valkey Connection Failure

```
# Stop Valkey service
docker compose -f docker-compose.local.yml stop valkey

# Try to enqueue a job
docker compose -f docker-compose.local.yml exec django python manage.py shell
```

In Django shell:

```
import django_rq
queue = django_rq.get_queue("default")
try:
    job = queue.enqueue("test_rq_only.users.tasks.get_users_count")
except Exception as e:
    print(f"Expected error: {e}")
exit()
```

**Verify:**

- [ ] Phase 7 – 7.2 Test Valkey Connection Failure: Clear error message about connection failure
- [ ] Phase 7 – 7.2 Test Valkey Connection Failure: Django app doesn't crash
- [ ] Phase 7 – 7.2 Test Valkey Connection Failure: Worker logs show connection retry attempts

**Cleanup:**

```
docker compose -f docker-compose.local.yml start valkey
```

### 7.3 Test Environment Variable Errors

Edit `.envs/.local/.django` and set an invalid VALKEY_URL:

```
VALKEY_URL=valkey://wrong-host:6379/0
```

Restart services and check logs:

```
docker compose -f docker-compose.local.yml restart django rqworker
docker compose -f docker-compose.local.yml logs rqworker
```

**Verify:**

- [ ] Phase 7 – 7.3 Test Environment Variable Errors: Clear error messages about connection issues
- [ ] Phase 7 – 7.3 Test Environment Variable Errors: Dashboard shows connection problem

**Cleanup:** Revert to correct VALKEY_URL

---

## Phase 8: Cleanup and File Audit

### 8.1 Check for Leftover Redis References in RQ-Only Project

In `test_rq_only` project:

```
# Search for "redis" in files (should only appear in comments/docs)
grep -r "redis" --include="*.py" --include="*.yml" --include="*.txt" . | grep -v "#" | grep -v valkey
```

**Verify:**

- [ ] Phase 8 – 8.1 Check for Leftover Redis References in RQ-Only Project: No hardcoded redis references in RQ-specific code
- [ ] Phase 8 – 8.1 Check for Leftover Redis References in RQ-Only Project: All RQ code uses VALKEY_URL or valkey service names

### 8.2 Check for Jinja2 Template Syntax Errors

```
cd /Users/millsks/UserLocal/apps/src/code/Public-Git/millsks/cookiecutter-django

# Try generating with various combinations
cookiecutter . --no-input use_rq=y use_celery=n
cookiecutter . --no-input use_rq=n use_celery=y  
cookiecutter . --no-input use_rq=y use_celery=y
cookiecutter . --no-input use_rq=n use_celery=n
```

**Verify:**

- [ ] Phase 8 – 8.2 Check for Jinja2 Template Syntax Errors: All combinations generate without Jinja2 errors
- [ ] Phase 8 – 8.2 Check for Jinja2 Template Syntax Errors: No syntax errors in template files
- [ ] Phase 8 – 8.2 Check for Jinja2 Template Syntax Errors: Generated projects have correct conditional logic

---

## Phase 9: Performance and Resource Usage

### 9.1 Check Resource Consumption

With services running:

```
docker stats
```

**Verify:**

- [ ] Phase 9 – 9.1 Check Resource Consumption: Valkey memory usage is reasonable (typically < 50MB idle)
- [ ] Phase 9 – 9.1 Check Resource Consumption: RQ worker memory usage is acceptable
- [ ] Phase 9 – 9.1 Check Resource Consumption: No memory leaks after processing multiple jobs

### 9.2 Test Queue Performance

```
docker compose -f docker-compose.local.yml exec django python manage.py shell
```

In Django shell:

```
import django_rq
import time

queue = django_rq.get_queue("default")

# Enqueue 100 jobs
start = time.time()
for i in range(100):
    queue.enqueue("test_rq_only.users.tasks.get_users_count")
end = time.time()

print(f"Enqueued 100 jobs in {end-start:.2f} seconds")
exit()
```

**Verify:**

- [ ] Phase 9 – 9.2 Test Queue Performance: Jobs enqueue quickly (< 1 second for 100 jobs)
- [ ] Phase 9 – 9.2 Test Queue Performance: Dashboard updates in real-time
- [ ] Phase 9 – 9.2 Test Queue Performance: Worker processes all jobs successfully

---

## Phase 10: Final Checks Before PR

### 10.1 Code Quality

- [ ] Phase 10 – 10.1 Code Quality: No TODO comments left in production code
- [ ] Phase 10 – 10.1 Code Quality: All files use consistent formatting
- [ ] Phase 10 – 10.1 Code Quality: No debug print statements in final code
- [ ] Phase 10 – 10.1 Code Quality: Scripts have proper shebang and error handling

### 10.2 Git Status

```
cd /Users/millsks/UserLocal/apps/src/code/Public-Git/millsks/cookiecutter-django
git status
```

**Review all changed files:**

- [ ] Phase 10 – 10.2 Git Status: No unintended file modifications
- [ ] Phase 10 – 10.2 Git Status: No local test projects committed
- [ ] Phase 10 – 10.2 Git Status: No sensitive data in commits
- [ ] Phase 10 – 10.2 Git Status: All new files are properly tracked

### 10.3 Run Template Tests

```
# If cookiecutter-django has a test suite
pytest tests/
```

**Verify:**

- [ ] Phase 10 – 10.3 Run Template Tests: All existing tests still pass
- [ ] Phase 10 – 10.3 Run Template Tests: No regressions introduced

### 10.4 Create Commit Message

Prepare a comprehensive commit message:

```
Add django-rq as optional task queue with Valkey backend

This adds django-rq as a simpler alternative to Celery for background
task processing, using Valkey (open-source Redis-compatible data store)
as the message broker.

Key changes:
- New cookiecutter option: use_rq (y/n)
- Separate Valkey service for RQ (parallel to Redis for Celery)
- RQ worker, scheduler, and dashboard services in Docker
- Complete documentation in docs/4-guides/using-django-rq.rst
- Example tasks and tests in users app
- Heroku Procfile integration

Architecture: When both use_celery and use_rq are enabled, Redis is
used exclusively for Celery, while Valkey is used exclusively for RQ.
This separation ensures no conflicts between the two systems.

Closes #XXXX
```

---

## Phase 11: PR Preparation

### 11.1 Create Summary Document

Document these key points for the PR description:

- [ ] Phase 11 – 11.1 Create Summary Document: List all files changed with brief explanation
- [ ] Phase 11 – 11.1 Create Summary Document: Explain Valkey vs Redis separation architecture
- [ ] Phase 11 – 11.1 Create Summary Document: Note any breaking changes (there should be none)
- [ ] Phase 11 – 11.1 Create Summary Document: List testing performed (reference this checklist)
- [ ] Phase 11 – 11.1 Create Summary Document: Screenshots of RQ Dashboard
- [ ] Phase 11 – 11.1 Create Summary Document: Performance notes

### 11.2 Prepare Examples

Take screenshots:

- [ ] Phase 11 – 11.2 Prepare Examples: RQ Dashboard with active jobs
- [ ] Phase 11 – 11.2 Prepare Examples: Docker services running (both redis and valkey)
- [ ] Phase 11 – 11.2 Prepare Examples: Example task code
- [ ] Phase 11 – 11.2 Prepare Examples: Documentation rendered in browser

### 11.3 Questions for Maintainers

Based on your testing, prepare questions:

- [ ] Phase 11 – 11.3 Questions for Maintainers: Should use_celery and use_rq be mutually exclusive?
- [ ] Phase 11 – 11.3 Questions for Maintainers: Is the documentation level appropriate?
- [ ] Phase 11 – 11.3 Questions for Maintainers: Any concerns about the Valkey dependency?
- [ ] Phase 11 – 11.3 Questions for Maintainers: Preferences on naming conventions?

---

## Sign-Off

Once all items are checked:

- [ ] Sign-Off: **All tests pass** - Every test case executed successfully
- [ ] Sign-Off: **Documentation complete** - All docs reviewed and accurate
- [ ] Sign-Off: **No regressions** - Existing functionality unaffected
- [ ] Sign-Off: **Ready for PR** - Code is clean and well-tested

**Tested by:** \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_
**Date:** \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_
**Test duration:** \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

**Notes/Issues found:**

---

---

---

**Overall assessment:**

- [ ] Overall assessment: Ready to submit PR
- [ ] Overall assessment: Minor issues to fix first
- [ ] Overall assessment: Major rework needed

---

## Quick Reference Commands

### Start local environment

```
docker compose -f docker-compose.local.yml up
```

### Access services

- [ ] Quick Reference Commands – Access services: Django: [http://localhost:8000](http://localhost:8000)
- [ ] Quick Reference Commands – Access services: RQ Dashboard: [http://localhost:9181](http://localhost:9181)
- [ ] Quick Reference Commands – Access services: Flower (if Celery enabled): [http://localhost:5555](http://localhost:5555)

### Common debugging commands

```
# Django shell
docker compose -f docker-compose.local.yml exec django python manage.py shell

# RQ worker logs
docker compose -f docker-compose.local.yml logs -f rqworker

# Valkey CLI
docker compose -f docker-compose.local.yml exec valkey valkey-cli

# List all queues
docker compose -f docker-compose.local.yml exec django python manage.py rqstats
```

### Generate fresh test project

```
cd /Users/millsks/UserLocal/apps/src/code/Public-Git/millsks
rm -rf test_rq_only  # Clean up old version
cookiecutter cookiecutter-django
# Answer prompts...
cd test_rq_only
docker compose -f docker-compose.local.yml up --build
```
