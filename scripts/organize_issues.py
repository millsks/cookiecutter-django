"""
Script to organize GitHub issues by phase for the Django-RQ Integration Testing checklist.

This script:
1. Creates 11 new Phase issues (one per phase in issue #1's checklist)
2. Moves existing sub-issues from #1 to appropriate Phase issues based on title prefix
3. Links the new Phase issues as sub-issues to parent issue #1

Usage:
    export GITHUB_TOKEN="your_personal_access_token"
    python scripts/organize_issues.py

Requirements:
    pip install requests
"""

from __future__ import annotations

import os
import re
import sys
import time

import requests

# Configuration
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
OWNER = os.getenv("GITHUB_OWNER", "millsks")
REPO = os.getenv("GITHUB_REPO", "cookiecutter-django")
PARENT_ISSUE_NUMBER = 1

# API endpoints
REST_API_BASE = "https://api.github.com"
GRAPHQL_API = "https://api.github.com/graphql"

# HTTP Status codes
HTTP_OK = 200
HTTP_CREATED = 201
HTTP_RATE_LIMITED = 403

# Request timeout in seconds
REQUEST_TIMEOUT = 30


def get_headers():
    """Get headers for API requests."""
    if not GITHUB_TOKEN:
        raise ValueError(
            "GITHUB_TOKEN environment variable is required. "
            "Set it with: export GITHUB_TOKEN='your_token'",
        )
    return {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }


# Phase definitions based on issue #1's checklist
PHASES = {
    1: {
        "title": "Phase 1: Pre-Generation Validation",
        "description": (
            "## Phase 1: Pre-Generation Validation\n\n"
            "Review template files and documentation before generating test projects.\n\n"
            "### 1.1 Review Template Files\n"
            "- cookiecutter.json\n"
            "- hooks/post_gen_project.py\n"
            "- requirements/base.txt\n\n"
            "### 1.2 Review Documentation\n"
            "- README.md\n"
            "- docs/4-guides/using-django-rq.rst\n"
            "- docs/1-getting-started/project-generation-options.rst\n"
            "- docs/2-local-development/developing-locally-docker.rst\n"
            "- docs/3-deployment/deployment-with-docker.rst\n"
        ),
        "prefix_patterns": [
            r"Phase 1",
        ],
    },
    2: {
        "title": "Phase 2: Generate Test Projects",
        "description": (
            "## Phase 2: Generate Test Projects\n\n"
            "Generate and validate test projects for all configuration combinations.\n\n"
            "### Test Cases:\n"
            "1. RQ Only (No Celery)\n"
            "2. Celery Only (No RQ)\n"
            "3. Both RQ and Celery\n"
            "4. Neither (Baseline)\n"
        ),
        "prefix_patterns": [
            r"Phase 2",
        ],
    },
    3: {
        "title": "Phase 3: Local Development Testing (RQ Only)",
        "description": (
            "## Phase 3: Local Development Testing\n\n"
            "Test RQ-only configuration with Docker Compose.\n\n"
            "### Tests:\n"
            "- 3.1 Docker Compose Startup\n"
            "- 3.2 Service Health Checks\n"
            "- 3.3 RQ Dashboard Access\n"
            "- 3.4 Enqueue and Process Test Job\n"
            "- 3.5 Test Scheduled Jobs\n"
            "- 3.6 Test Multiple Queues\n"
            "- 3.7 Test Hot Reload\n"
            "- 3.8 Run Unit Tests\n"
        ),
        "prefix_patterns": [
            r"Phase 3",
        ],
    },
    4: {
        "title": "Phase 4: Production Configuration Testing",
        "description": (
            "## Phase 4: Production Configuration Testing\n\n"
            "Review and test production Docker Compose configuration.\n\n"
            "### Tests:\n"
            "- 4.1 Review Production Docker Compose\n"
            "- 4.2 Review Production Environment Variables\n"
            "- 4.3 Test Production Build (Optional)\n"
        ),
        "prefix_patterns": [
            r"Phase 4",
        ],
    },
    5: {
        "title": "Phase 5: Dual Queue Testing (Both RQ and Celery)",
        "description": (
            "## Phase 5: Dual Queue Testing\n\n"
            "Test configuration with both RQ and Celery enabled.\n\n"
            "### Tests:\n"
            "- 5.1 Verify Service Separation\n"
            "- 5.2 Test Isolated Task Processing\n"
            "- 5.3 Check Logs for Correct Backend Usage\n"
        ),
        "prefix_patterns": [
            r"Phase 5",
        ],
    },
    6: {
        "title": "Phase 6: Documentation Review",
        "description": (
            "## Phase 6: Documentation Review\n\n"
            "Review and test all documentation.\n\n"
            "### Tests:\n"
            "- 6.1 Read Through All Documentation\n"
            "- 6.2 Documentation Build Test\n"
        ),
        "prefix_patterns": [
            r"Phase 6",
        ],
    },
    7: {
        "title": "Phase 7: Edge Cases and Error Handling",
        "description": (
            "## Phase 7: Edge Cases and Error Handling\n\n"
            "Test error scenarios and edge cases.\n\n"
            "### Tests:\n"
            "- 7.1 Test Failed Jobs\n"
            "- 7.2 Test Valkey Connection Failure\n"
            "- 7.3 Test Environment Variable Errors\n"
        ),
        "prefix_patterns": [
            r"Phase 7",
        ],
    },
    8: {
        "title": "Phase 8: Cleanup and File Audit",
        "description": (
            "## Phase 8: Cleanup and File Audit\n\n"
            "Check for leftover references and template errors.\n\n"
            "### Tests:\n"
            "- 8.1 Check for Leftover Redis References\n"
            "- 8.2 Check for Jinja2 Template Syntax Errors\n"
        ),
        "prefix_patterns": [
            r"Phase 8",
        ],
    },
    9: {
        "title": "Phase 9: Performance and Resource Usage",
        "description": (
            "## Phase 9: Performance and Resource Usage\n\n"
            "Check resource consumption and performance.\n\n"
            "### Tests:\n"
            "- 9.1 Check Resource Consumption\n"
            "- 9.2 Test Queue Performance\n"
        ),
        "prefix_patterns": [
            r"Phase 9",
        ],
    },
    10: {
        "title": "Phase 10: Final Checks Before PR",
        "description": (
            "## Phase 10: Final Checks Before PR\n\n"
            "Final code quality and git checks.\n\n"
            "### Tests:\n"
            "- 10.1 Code Quality\n"
            "- 10.2 Git Status\n"
            "- 10.3 Run Template Tests\n"
            "- 10.4 Create Commit Message\n"
        ),
        "prefix_patterns": [
            r"Phase 10",
        ],
    },
    11: {
        "title": "Phase 11: PR Preparation",
        "description": (
            "## Phase 11: PR Preparation\n\n"
            "Prepare PR documentation and examples.\n\n"
            "### Tasks:\n"
            "- 11.1 Create Summary Document\n"
            "- 11.2 Prepare Examples\n"
            "- 11.3 Questions for Maintainers\n"
        ),
        "prefix_patterns": [
            r"Phase 11",
        ],
    },
}


def make_request(method: str, url: str, **kwargs) -> requests.Response:
    """Make an API request with rate limiting handling."""
    headers = get_headers()
    timeout = kwargs.pop("timeout", REQUEST_TIMEOUT)
    response = requests.request(method, url, headers=headers, timeout=timeout, **kwargs)

    # Handle rate limiting
    if response.status_code == HTTP_RATE_LIMITED:
        reset_time = response.headers.get("X-RateLimit-Reset")
        if reset_time:
            wait_time = max(int(reset_time) - int(time.time()), 0) + 1
            print(f"Rate limited. Waiting {wait_time} seconds...")
            time.sleep(wait_time)
            return make_request(method, url, timeout=timeout, **kwargs)

    return response


def get_all_issues() -> list[dict]:
    """Get all open issues from the repository."""
    issues = []
    page = 1
    per_page = 100

    while True:
        url = f"{REST_API_BASE}/repos/{OWNER}/{REPO}/issues"
        params = {
            "state": "open",
            "per_page": per_page,
            "page": page,
        }
        response = make_request("GET", url, params=params)

        if response.status_code != HTTP_OK:
            print(f"Error fetching issues: {response.status_code}")
            print(response.json())
            sys.exit(1)

        page_issues = response.json()
        if not page_issues:
            break

        # Filter out pull requests (they have 'pull_request' key)
        issues.extend([i for i in page_issues if "pull_request" not in i])
        page += 1

    return issues


def get_sub_issues(parent_issue_number: int) -> list[dict]:
    """Get sub-issues of a parent issue using GraphQL."""
    query = """
    query($owner: String!, $repo: String!, $issueNumber: Int!) {
        repository(owner: $owner, name: $repo) {
            issue(number: $issueNumber) {
                id
                subIssues(first: 100) {
                    nodes {
                        id
                        number
                        title
                    }
                    pageInfo {
                        hasNextPage
                        endCursor
                    }
                }
            }
        }
    }
    """
    variables = {
        "owner": OWNER,
        "repo": REPO,
        "issueNumber": parent_issue_number,
    }

    response = make_request("POST", GRAPHQL_API, json={"query": query, "variables": variables})

    if response.status_code != HTTP_OK:
        print(f"Error in GraphQL query: {response.status_code}")
        print(response.text)
        return []

    data = response.json()
    if "errors" in data:
        print(f"GraphQL errors: {data['errors']}")
        return []

    issue_data = data.get("data", {}).get("repository", {}).get("issue", {})
    if not issue_data:
        return []

    return issue_data.get("subIssues", {}).get("nodes", [])


def create_issue(title: str, body: str) -> dict | None:
    """Create a new issue."""
    url = f"{REST_API_BASE}/repos/{OWNER}/{REPO}/issues"
    data = {
        "title": title,
        "body": body,
    }

    response = make_request("POST", url, json=data)

    if response.status_code == HTTP_CREATED:
        issue = response.json()
        print(f"Created issue #{issue['number']}: {title}")
        return issue
    print(f"Error creating issue: {response.status_code}")
    print(response.json())
    return None


def get_issue_node_id(issue_number: int) -> str | None:
    """Get the GraphQL node ID for an issue."""
    query = """
    query($owner: String!, $repo: String!, $issueNumber: Int!) {
        repository(owner: $owner, name: $repo) {
            issue(number: $issueNumber) {
                id
            }
        }
    }
    """
    variables = {
        "owner": OWNER,
        "repo": REPO,
        "issueNumber": issue_number,
    }

    response = make_request("POST", GRAPHQL_API, json={"query": query, "variables": variables})

    if response.status_code != HTTP_OK:
        return None

    data = response.json()
    return data.get("data", {}).get("repository", {}).get("issue", {}).get("id")


def add_sub_issue(parent_id: str, child_id: str) -> bool:
    """Add a sub-issue to a parent issue using GraphQL mutation."""
    mutation = """
    mutation($parentId: ID!, $childId: ID!) {
        addSubIssue(input: {issueId: $parentId, subIssueId: $childId}) {
            issue {
                id
                number
            }
            subIssue {
                id
                number
            }
        }
    }
    """
    variables = {
        "parentId": parent_id,
        "childId": child_id,
    }

    response = make_request("POST", GRAPHQL_API, json={"query": mutation, "variables": variables})

    if response.status_code != HTTP_OK:
        print(f"Error adding sub-issue: {response.status_code}")
        print(response.text)
        return False

    data = response.json()
    if "errors" in data:
        print(f"GraphQL errors: {data['errors']}")
        return False

    return True


def remove_sub_issue(parent_id: str, child_id: str) -> bool:
    """Remove a sub-issue from a parent issue using GraphQL mutation."""
    mutation = """
    mutation($parentId: ID!, $childId: ID!) {
        removeSubIssue(input: {issueId: $parentId, subIssueId: $childId}) {
            issue {
                id
                number
            }
            subIssue {
                id
                number
            }
        }
    }
    """
    variables = {
        "parentId": parent_id,
        "childId": child_id,
    }

    response = make_request("POST", GRAPHQL_API, json={"query": mutation, "variables": variables})

    if response.status_code != HTTP_OK:
        print(f"Error removing sub-issue: {response.status_code}")
        print(response.text)
        return False

    data = response.json()
    if "errors" in data:
        print(f"GraphQL errors: {data['errors']}")
        return False

    return True


def get_phase_for_issue(title: str) -> int | None:
    """Determine which phase an issue belongs to based on its title."""
    for phase_num, phase_config in PHASES.items():
        for pattern in phase_config["prefix_patterns"]:
            if re.search(pattern, title, re.IGNORECASE):
                return phase_num
    return None


def create_phase_issues() -> dict:
    """Create Phase issues and return a mapping of phase_number -> issue data."""
    print("Creating Phase issues...")
    phase_issues = {}

    for phase_num, phase_config in PHASES.items():
        print(f"  Creating {phase_config['title']}...")
        issue = create_issue(phase_config["title"], phase_config["description"])
        if issue:
            phase_issues[phase_num] = {
                "number": issue["number"],
                "node_id": issue["node_id"],
                "title": issue["title"],
            }
        time.sleep(0.5)  # Rate limiting

    return phase_issues


def link_phases_to_parent(parent_node_id: str, phase_issues: dict) -> None:
    """Link Phase issues as sub-issues of parent issue #1."""
    print(f"Linking Phase issues to parent issue #{PARENT_ISSUE_NUMBER}...")
    for phase_num in sorted(phase_issues.keys()):
        phase_data = phase_issues[phase_num]
        print(f"  Linking Phase {phase_num} (#{phase_data['number']}) to #{PARENT_ISSUE_NUMBER}...")
        success = add_sub_issue(parent_node_id, phase_data["node_id"])
        if success:
            print("    ✓ Linked successfully")
        else:
            print("    ✗ Failed to link")
        time.sleep(0.5)


def move_sub_issues_to_phases(
    parent_node_id: str,
    existing_sub_issues: dict,
    phase_issues: dict,
) -> tuple[int, int]:
    """Move existing sub-issues to appropriate Phase issues."""
    print("Moving existing sub-issues to Phase issues...")
    moved_count = 0
    skipped_count = 0

    for issue_num, issue_data in existing_sub_issues.items():
        title = issue_data["title"]
        phase_num = get_phase_for_issue(title)

        if phase_num and phase_num in phase_issues:
            phase_data = phase_issues[phase_num]
            print(f"  Moving #{issue_num} to Phase {phase_num}...")

            # Remove from parent issue #1
            remove_success = remove_sub_issue(parent_node_id, issue_data["id"])

            # Add to Phase issue
            add_success = add_sub_issue(phase_data["node_id"], issue_data["id"])

            if remove_success and add_success:
                print(f"    ✓ Moved to Phase {phase_num} (#{phase_data['number']})")
                moved_count += 1
            else:
                print("    ✗ Failed to move")
            time.sleep(0.3)
        else:
            print(f"  Skipping #{issue_num}: No matching phase found")
            skipped_count += 1

    return moved_count, skipped_count


def print_summary(phase_issues: dict, moved_count: int, skipped_count: int) -> None:
    """Print summary of operations."""
    print("=" * 60)
    print("Summary")
    print("=" * 60)
    print(f"Phase issues created: {len(phase_issues)}")
    print(f"Sub-issues moved: {moved_count}")
    print(f"Sub-issues skipped: {skipped_count}")
    print()
    print("Phase issues created:")
    for phase_num in sorted(phase_issues.keys()):
        phase_data = phase_issues[phase_num]
        print(f"  Phase {phase_num}: #{phase_data['number']} - {phase_data['title']}")
    print()
    print("Done!")


def main():
    """Main function to organize issues by phase."""
    print("=" * 60)
    print("GitHub Issue Organization Script")
    print("=" * 60)
    print(f"Repository: {OWNER}/{REPO}")
    print(f"Parent Issue: #{PARENT_ISSUE_NUMBER}")
    print()

    # Step 1: Get the parent issue node ID
    print("Step 1: Getting parent issue node ID...")
    parent_node_id = get_issue_node_id(PARENT_ISSUE_NUMBER)
    if not parent_node_id:
        print(f"Error: Could not find issue #{PARENT_ISSUE_NUMBER}")
        sys.exit(1)
    print(f"Parent issue node ID: {parent_node_id}")
    print()

    # Step 2: Get all current sub-issues of the parent
    print("Step 2: Getting current sub-issues of parent...")
    current_sub_issues = get_sub_issues(PARENT_ISSUE_NUMBER)
    print(f"Found {len(current_sub_issues)} sub-issues")
    existing_sub_issues = {si["number"]: si for si in current_sub_issues}
    print()

    # Step 3: Create Phase issues
    print("Step 3: ", end="")
    phase_issues = create_phase_issues()
    print()

    # Step 4: Add Phase issues as sub-issues of parent issue #1
    print("Step 4: ", end="")
    link_phases_to_parent(parent_node_id, phase_issues)
    print()

    # Step 5: Move existing sub-issues to appropriate Phase issues
    print("Step 5: ", end="")
    moved_count, skipped_count = move_sub_issues_to_phases(
        parent_node_id, existing_sub_issues, phase_issues,
    )
    print()

    # Print summary
    print_summary(phase_issues, moved_count, skipped_count)


if __name__ == "__main__":
    main()
