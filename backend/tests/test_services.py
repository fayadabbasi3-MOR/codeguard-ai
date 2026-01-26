"""Tests for service modules."""
import pytest
from unittest.mock import Mock, patch, MagicMock

from app.services.analyzer import AnalyzerService
from app.services.github import GitHubService
from app.models.schemas import ClaudeAnalysisResult, IssueResponse, Category, Severity
from datetime import datetime


class TestAnalyzerService:
    """Test Claude analyzer service."""

    def test_init_without_api_key(self):
        """Test analyzer initializes without API key."""
        with patch('app.services.analyzer.settings') as mock_settings:
            mock_settings.anthropic_api_key = ""
            service = AnalyzerService()
            assert service.client is None

    def test_parse_response_valid_json(self):
        """Test parsing valid JSON response from Claude."""
        service = AnalyzerService()
        service.client = None  # Don't need actual client for this test

        response = '''{
            "issues": [
                {
                    "category": "security",
                    "severity": "critical",
                    "file_path": "src/auth.js",
                    "line_number": 23,
                    "title": "Hardcoded API key",
                    "message": "API key found in source code",
                    "explanation": "Keys can be extracted from version control",
                    "suggestion": "Use environment variables"
                }
            ],
            "summary": "Found 1 security issue",
            "has_tests": true,
            "overall_quality": "needs_improvement"
        }'''

        result = service._parse_response(response)

        assert len(result.issues) == 1
        assert result.issues[0].category == "security"
        assert result.issues[0].severity == "critical"
        assert result.has_tests is True
        assert result.overall_quality == "needs_improvement"

    def test_parse_response_empty_issues(self):
        """Test parsing response with no issues."""
        service = AnalyzerService()
        service.client = None

        response = '''{
            "issues": [],
            "summary": "No issues found",
            "has_tests": true,
            "overall_quality": "good"
        }'''

        result = service._parse_response(response)

        assert len(result.issues) == 0
        assert result.summary == "No issues found"

    def test_parse_response_invalid_json(self):
        """Test parsing invalid JSON response."""
        service = AnalyzerService()
        service.client = None

        response = "This is not valid JSON"

        result = service._parse_response(response)

        assert len(result.issues) == 0
        assert "Invalid JSON" in result.summary or "parse" in result.summary.lower()

    def test_parse_response_with_text_around_json(self):
        """Test parsing response with text before/after JSON."""
        service = AnalyzerService()
        service.client = None

        response = '''Here is my analysis:
        {
            "issues": [
                {
                    "category": "quality",
                    "severity": "warning",
                    "file_path": "test.js",
                    "title": "Test issue",
                    "message": "Test message"
                }
            ],
            "summary": "Found 1 issue"
        }
        Let me know if you need more details.'''

        result = service._parse_response(response)

        assert len(result.issues) == 1
        assert result.issues[0].category == "quality"


class TestGitHubService:
    """Test GitHub service."""

    def test_init_without_token(self):
        """Test service initializes without token."""
        with patch('app.services.github.settings') as mock_settings:
            mock_settings.github_token = ""
            service = GitHubService()
            assert service.client is None

    def test_get_pr_diff_no_client(self):
        """Test getting PR diff without client returns error."""
        service = GitHubService()
        service.client = None

        diff, info = service.get_pr_diff("owner/repo", 1)

        assert diff == ""
        assert "error" in info

    def test_format_review_comment_no_issues(self):
        """Test formatting review comment with no issues."""
        service = GitHubService()

        comment = service.format_review_comment([], "No issues found")

        assert "CodeGuard Review" in comment
        assert "No issues found" in comment
        assert "Great job" in comment

    def test_format_review_comment_with_issues(self):
        """Test formatting review comment with issues."""
        service = GitHubService()

        issues = [
            IssueResponse(
                id="1",
                category=Category.security,
                severity=Severity.critical,
                file_path="src/auth.js",
                line_number=23,
                title="Hardcoded secret",
                message="API key in source",
                explanation="Bad practice",
                suggestion="Use env vars",
                created_at=datetime.now()
            ),
            IssueResponse(
                id="2",
                category=Category.quality,
                severity=Severity.warning,
                file_path="src/utils.js",
                line_number=45,
                title="Console log",
                message="Debug log in prod",
                created_at=datetime.now()
            ),
        ]

        comment = service.format_review_comment(issues)

        assert "CodeGuard Review" in comment
        assert "2 issues found" in comment
        assert "Critical Issues" in comment
        assert "Warnings" in comment
        assert "Hardcoded secret" in comment
        assert "src/auth.js" in comment

    def test_format_issue(self):
        """Test formatting a single issue."""
        service = GitHubService()

        issue = IssueResponse(
            id="1",
            category=Category.security,
            severity=Severity.critical,
            file_path="src/api.js",
            line_number=100,
            title="SQL Injection",
            message="User input in query",
            explanation="Can lead to data breach",
            suggestion="Use parameterized queries",
            created_at=datetime.now()
        )

        formatted = service._format_issue(issue)

        assert "src/api.js" in formatted
        assert "line 100" in formatted
        assert "SQL Injection" in formatted
        assert "Use parameterized queries" in formatted

    def test_post_review_comment_no_client(self):
        """Test posting comment without client returns None."""
        service = GitHubService()
        service.client = None

        result = service.post_review_comment("owner/repo", 1, "Test comment")

        assert result is None
