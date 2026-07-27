"""Unit tests for GitHubTool (issue #50).

Week 8 reproduction: GitHubTool.execute returns repository metadata but does
not include a has_tests boolean. The test below asserts the field exists, so
it fails against the current code. That failure is the proof the issue is real
in my local environment. Week 9 adds the field and expands this file into full
coverage.
"""

from unittest.mock import Mock, patch

import pytest

from agent.tools.github_tool import GitHubTool


def _fake_repo_json() -> dict:
    """Return a minimal GitHub repo payload shaped like the real API response."""
    return {
        "name": "example",
        "description": "Example repository",
        "language": "Python",
        "stargazers_count": 3,
        "forks_count": 1,
        "open_issues_count": 0,
        "pushed_at": "2024-01-01T00:00:00Z",
        "topics": [],
        "homepage": "",
    }


@pytest.mark.unit
@patch("agent.tools.github_tool.httpx")
def test_output_includes_has_tests_field(mock_httpx):
    """Reproduce issue #50: the metadata output should carry a has_tests flag."""
    get_response = Mock()
    get_response.raise_for_status = Mock()
    get_response.json = Mock(return_value=_fake_repo_json())
    mock_httpx.get.return_value = get_response

    head_response = Mock()
    head_response.status_code = 200
    mock_httpx.head.return_value = head_response

    tool = GitHubTool()
    result = tool.execute({"github_username": "octocat", "repo_name": "example"})

    assert result.success is True
    assert "has_tests" in result.data  # fails today, which reproduces the gap
