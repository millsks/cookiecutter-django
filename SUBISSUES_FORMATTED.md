# Preformatted Sub-Issues for Django-RQ Integration Testing

Each item below is formatted as a sub-issue title. Copy and paste to create sub-issues.

---

## 1.2 Review Documentation

1. `1.2 Review Documentation: **README.md**: Verify django-rq with Valkey is mentioned in Optional Integrations`
2. `1.2 Review Documentation: **docs/4-guides/using-django-rq.rst**: Review comprehensive guide for accuracy`
3. `1.2 Review Documentation: **docs/1-getting-started/project-generation-options.rst**: Check use_rq option is documented`
4. `1.2 Review Documentation: **docs/2-local-development/developing-locally-docker.rst**: Verify RQ section is present`
5. `1.2 Review Documentation: **docs/3-deployment/deployment-with-docker.rst**: Check Valkey service is mentioned`

---

## Test Case 1: RQ Only (No Celery)

1. `Test Case 1 RQ Only: docker-compose.local.yml contains valkey service (NOT redis)`
2. `Test Case 1 RQ Only: docker-compose.local.yml has rqworker, rqscheduler, rqdashboard services`
3. `Test Case 1 RQ Only: docker-compose.production.yml contains valkey service (NOT redis)`
4. `Test Case 1 RQ Only: .envs/.local/.django has VALKEY_URL=valkey://valkey:6379/0`
5. `Test Case 1 RQ Only: .envs/.production/.django has VALKEY_URL=valkey://valkey:6379/0`
6. `Test Case 1 RQ Only: config/settings/base.py has VALKEY_URL variable and RQ_QUEUES using it`
7. `Test Case 1 RQ Only: config/settings/base.py does NOT have REDIS_URL variable`
8. `Test Case 1 RQ Only: compose/local/django/rq/ directory exists with worker/start, scheduler/start, dashboard/start`
9. `Test Case 1 RQ Only: compose/production/django/rq/ directory exists with same scripts`
10. `Test Case 1 RQ Only: Scripts use ${VALKEY_URL} not ${REDIS_URL}`
11. `Test Case 1 RQ Only: test_rq_only/users/tasks.py has @django_rq.job decorator`
12. `Test Case 1 RQ Only: test_rq_only/users/tests/test_tasks.py has RQ test with is_async=False`
13. `Test Case 1 RQ Only: Procfile has worker: and scheduler: processes`

---

## Test Case 2: Celery Only (No RQ)

1. `Test Case 2 Celery Only: docker-compose.local.yml contains redis service (NOT valkey)`
2. `Test Case 2 Celery Only: docker-compose.local.yml has celery services, NO rq services`
3. `Test Case 2 Celery Only: .envs/.local/.django has REDIS_URL=redis://redis:6379/0`
4. `Test Case 2 Celery Only: .envs/.local/.django does NOT have VALKEY_URL`
5. `Test Case 2 Celery Only: config/settings/base.py has REDIS_URL and Celery config`
6. `Test Case 2 Celery Only: config/settings/base.py does NOT have RQ config or VALKEY_URL`
7. `Test Case 2 Celery Only: compose/local/django/rq/ directory does NOT exist`
8. `Test Case 2 Celery Only: compose/production/django/rq/ directory does NOT exist`
9. `Test Case 2 Celery Only: test_celery_only/users/tasks.py has @shared_task() decorator`
10. `Test Case 2 Celery Only: test_celery_only/users/tests/test_tasks.py has Celery test`

---

## Test Case 3: Both RQ and Celery

1. `Test Case 3 Both Queues: docker-compose.local.yml contains BOTH redis and valkey services`
2. `Test Case 3 Both Queues: docker-compose.local.yml has volumes for both: local_redis_data and local_valkey_data`
3. `Test Case 3 Both Queues: Django service depends_on includes both redis and valkey`
4. `Test Case 3 Both Queues: Celery services depend on redis`
5. `Test Case 3 Both Queues: RQ services depend on valkey`
6. `Test Case 3 Both Queues: .envs/.local/.django has BOTH REDIS_URL (for Celery) and VALKEY_URL (for RQ)`
7. `Test Case 3 Both Queues: config/settings/base.py has both REDIS_URL and VALKEY_URL variables`
8. `Test Case 3 Both Queues: config/settings/base.py has Celery config using REDIS_URL`
9. `Test Case 3 Both Queues: config/settings/base.py has RQ config using VALKEY_URL`
10. `Test Case 3 Both Queues: Both compose/local/django/celery/ and compose/local/django/rq/ directories exist`

---

## Test Case 4: Neither (Baseline)

1. `Test Case 4 No Queues: docker-compose.local.yml has NO redis or valkey services`
2. `Test Case 4 No Queues: .envs/.local/.django has NO REDIS_URL or VALKEY_URL`
3. `Test Case 4 No Queues: config/settings/base.py has NO queue-related configuration`
4. `Test Case 4 No Queues: No compose/*/django/celery/ or compose/*/django/rq/ directories`
5. `Test Case 4 No Queues: test_no_queues/users/tasks.py has simple non-decorated function`

---

## 3.1 Docker Compose Startup

1. `3.1 Docker Compose Startup: All services start without errors`
2. `3.1 Docker Compose Startup: valkey service is running on port 6379`
3. `3.1 Docker Compose Startup: rqworker service starts and logs "Listening on queues: default, high, low"`
4. `3.1 Docker Compose Startup: rqscheduler service starts successfully`
5. `3.1 Docker Compose Startup: rqdashboard service starts on port 9181`
6. `3.1 Docker Compose Startup: NO redis service is running (since use_celery=n)`
7. `3.1 Docker Compose Startup: Django app accessible at http://localhost:8000`

---

## 3.2 Service Health Checks

1. `3.2 Service Health Checks: Valkey connection successful`
2. `3.2 Service Health Checks: No connection errors in logs`

---

## 3.3 RQ Dashboard Access

1. `3.3 RQ Dashboard Access: Dashboard loads without errors`
2. `3.3 RQ Dashboard Access: Shows 3 queues: default, high, low`
3. `3.3 RQ Dashboard Access: Shows workers count (should be 1+)`
4. `3.3 RQ Dashboard Access: Shows 0 jobs initially`

---

## 3.4 Enqueue and Process Test Job

1. `3.4 Enqueue and Process Test Job: Job enqueued successfully`
2. `3.4 Enqueue and Process Test Job: Job status changes to 'finished'`
3. `3.4 Enqueue and Process Test Job: Job result is an integer (user count)`
4. `3.4 Enqueue and Process Test Job: Worker logs show job processing`
5. `3.4 Enqueue and Process Test Job: Dashboard shows job in "Finished" tab`

---

## 3.5 Test Scheduled Jobs

1. `3.5 Test Scheduled Jobs: Job appears in Dashboard under "Scheduled" tab`
2. `3.5 Test Scheduled Jobs: After 30 seconds, job moves to "Finished"`
3. `3.5 Test Scheduled Jobs: Scheduler logs show job execution`

---

## 3.6 Test Multiple Queues

1. `3.6 Test Multiple Queues: Jobs appear in correct queues in Dashboard`
2. `3.6 Test Multiple Queues: Both jobs are processed successfully`

---

## 3.7 Test Hot Reload

1. `3.7 Test Hot Reload: Worker container restarts automatically (check logs)`
2. `3.7 Test Hot Reload: New jobs show the updated log message`
3. `3.7 Test Hot Reload: No manual restart required`

---

## 3.8 Run Unit Tests

1. `3.8 Run Unit Tests: All tests pass, including test_rq_only/users/tests/test_tasks.py`
2. `3.8 Run Unit Tests: RQ test uses synchronous mode (jobs execute immediately)`
3. `3.8 Run Unit Tests: No failures related to queue configuration`

---

## 4.1 Review Production Docker Compose

1. `4.1 Review Production Docker Compose: Contains valkey service with correct image: docker.io/valkey/valkey:8.0`
2. `4.1 Review Production Docker Compose: Volume production_valkey_data is defined`
3. `4.1 Review Production Docker Compose: rqworker, rqscheduler, rqdashboard services are present`
4. `4.1 Review Production Docker Compose: RQ services use correct command paths (/start-rqworker, etc.)`
5. `4.1 Review Production Docker Compose: NO redis service present (since use_celery=n)`

---

## 4.2 Review Production Environment Variables

1. `4.2 Review Production Environment Variables: Contains VALKEY_URL=valkey://valkey:6379/0`
2. `4.2 Review Production Environment Variables: Does NOT contain REDIS_URL (since use_celery=n)`
3. `4.2 Review Production Environment Variables: Placeholder values for other settings present`

---

## 4.3 Test Production Build

1. `4.3 Test Production Build: Build completes without errors`
2. `4.3 Test Production Build: Django image includes RQ startup scripts`
3. `4.3 Test Production Build: Script permissions are correct (executable)`

---

## 5.1 Verify Service Separation

1. `5.1 Verify Service Separation: Both redis and valkey services are running`
2. `5.1 Verify Service Separation: Celery worker connects to redis`
3. `5.1 Verify Service Separation: RQ worker connects to valkey`
4. `5.1 Verify Service Separation: Flower accessible at http://localhost:5555`
5. `5.1 Verify Service Separation: RQ Dashboard accessible at http://localhost:9181`

---

## 5.2 Test Isolated Task Processing

1. `5.2 Test Isolated Task Processing: Both tasks execute successfully`
2. `5.2 Test Isolated Task Processing: Celery task appears in Flower (http://localhost:5555)`
3. `5.2 Test Isolated Task Processing: RQ job appears in RQ Dashboard (http://localhost:9181)`
4. `5.2 Test Isolated Task Processing: No cross-contamination (Celery doesn't see RQ jobs and vice versa)`

---

## 5.3 Check Logs for Correct Backend Usage

1. `5.3 Check Logs for Correct Backend Usage: Celery worker logs show redis:6379 connection`
2. `5.3 Check Logs for Correct Backend Usage: RQ worker logs show valkey:6379 connection`
3. `5.3 Check Logs for Correct Backend Usage: No connection errors`

---

## 6.1 Read Through All Documentation

1. `6.1 Read Through All Documentation: docs/4-guides/using-django-rq.rst: Read completely, check for typos/accuracy`
2. `6.1 Read Through All Documentation: Verify all code examples are correct`
3. `6.1 Read Through All Documentation: Check that architecture diagram makes sense`
4. `6.1 Read Through All Documentation: Confirm troubleshooting section is helpful`
5. `6.1 Read Through All Documentation: Validate external links work`

---

## 6.2 Documentation Build Test

1. `6.2 Documentation Build Test: Docs build without errors`
2. `6.2 Documentation Build Test: using-django-rq.rst renders correctly at http://localhost:9000`
3. `6.2 Documentation Build Test: No Sphinx warnings about the new file`
4. `6.2 Documentation Build Test: Navigation includes the new guide`
5. `6.2 Documentation Build Test: All internal references resolve`

---

## 7.1 Test Failed Jobs

1. `7.1 Test Failed Jobs: Job status is 'failed'`
2. `7.1 Test Failed Jobs: Exception info is captured`
3. `7.1 Test Failed Jobs: Failed job appears in Dashboard "Failed" tab`
4. `7.1 Test Failed Jobs: Worker doesn't crash`

---

## 7.2 Test Valkey Connection Failure

1. `7.2 Test Valkey Connection Failure: Clear error message about connection failure`
2. `7.2 Test Valkey Connection Failure: Django app doesn't crash`
3. `7.2 Test Valkey Connection Failure: Worker logs show connection retry attempts`

---

## 7.3 Test Environment Variable Errors

1. `7.3 Test Environment Variable Errors: Clear error messages about connection issues`
2. `7.3 Test Environment Variable Errors: Dashboard shows connection problem`

---

## 8.1 Check for Leftover Redis References

1. `8.1 Check for Leftover Redis References: No hardcoded redis references in RQ-specific code`
2. `8.1 Check for Leftover Redis References: All RQ code uses VALKEY_URL or valkey service names`

---

## 8.2 Check for Jinja2 Template Syntax Errors

1. `8.2 Check for Jinja2 Template Syntax Errors: All combinations generate without Jinja2 errors`
2. `8.2 Check for Jinja2 Template Syntax Errors: No syntax errors in template files`
3. `8.2 Check for Jinja2 Template Syntax Errors: Generated projects have correct conditional logic`

---

## 9.1 Check Resource Consumption

1. `9.1 Check Resource Consumption: Valkey memory usage is reasonable (typically < 50MB idle)`
2. `9.1 Check Resource Consumption: RQ worker memory usage is acceptable`
3. `9.1 Check Resource Consumption: No memory leaks after processing multiple jobs`

---

## 9.2 Test Queue Performance

1. `9.2 Test Queue Performance: Jobs enqueue quickly (< 1 second for 100 jobs)`
2. `9.2 Test Queue Performance: Dashboard updates in real-time`
3. `9.2 Test Queue Performance: Worker processes all jobs successfully`

---

## 10.1 Code Quality

1. `10.1 Code Quality: No TODO comments left in production code`
2. `10.1 Code Quality: All files use consistent formatting`
3. `10.1 Code Quality: No debug print statements in final code`
4. `10.1 Code Quality: Scripts have proper shebang and error handling`

---

## 10.2 Git Status

1. `10.2 Git Status: No unintended file modifications`
2. `10.2 Git Status: No local test projects committed`
3. `10.2 Git Status: No sensitive data in commits`
4. `10.2 Git Status: All new files are properly tracked`

---

## 10.3 Run Template Tests

1. `10.3 Run Template Tests: All existing tests still pass`
2. `10.3 Run Template Tests: No regressions introduced`

---

## 11.1 Create Summary Document

1. `11.1 Create Summary Document: List all files changed with brief explanation`
2. `11.1 Create Summary Document: Explain Valkey vs Redis separation architecture`
3. `11.1 Create Summary Document: Note any breaking changes (there should be none)`
4. `11.1 Create Summary Document: List testing performed (reference this checklist)`
5. `11.1 Create Summary Document: Screenshots of RQ Dashboard`
6. `11.1 Create Summary Document: Performance notes`

---

## 11.2 Prepare Examples

1. `11.2 Prepare Examples: RQ Dashboard with active jobs`
2. `11.2 Prepare Examples: Docker services running (both redis and valkey)`
3. `11.2 Prepare Examples: Example task code`
4. `11.2 Prepare Examples: Documentation rendered in browser`

---

## 11.3 Questions for Maintainers

1. `11.3 Questions for Maintainers: Should use_celery and use_rq be mutually exclusive?`
2. `11.3 Questions for Maintainers: Is the documentation level appropriate?`
3. `11.3 Questions for Maintainers: Any concerns about the Valkey dependency?`
4. `11.3 Questions for Maintainers: Preferences on naming conventions?`

---

## Sign-Off

1. `Sign-Off: All tests pass - Every test case executed successfully`
2. `Sign-Off: Documentation complete - All docs reviewed and accurate`
3. `Sign-Off: No regressions - Existing functionality unaffected`
4. `Sign-Off: Ready for PR - Code is clean and well-tested`

---

## Overall Assessment

1. `Overall Assessment: Ready to submit PR`
2. `Overall Assessment: Minor issues to fix first`
3. `Overall Assessment: Major rework needed`

---

**Total: 127 sub-issues**
