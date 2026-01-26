"""Tests for Pydantic schemas."""
import pytest
from datetime import datetime

from app.models.schemas import (
    GitHubWebhookPayload,
    AnalysisResponse,
    AnalysisSummary,
    AnalysisMetadata,
    IssueResponse,
    FeedbackCreate,
    MetricsResponse,
    ClaudeAnalysisResult,
    ClaudeIssue,
    Category,
    Severity,
    AnalysisStatus,
)


class TestGitHubWebhookPayload:
    """Test GitHub webhook payload schema."""

    def test_parse_pr_opened_payload(self):
        """Test parsing a PR opened webhook payload."""
        payload = {
            "action": "opened",
            "pull_request": {
                "number": 42,
                "title": "Add new feature",
                "html_url": "https://github.com/owner/repo/pull/42",
                "state": "open",
                "head": {"sha": "abc123"},
                "base": {"sha": "def456"},
                "user": {"login": "developer", "id": 12345},
                "additions": 100,
                "deletions": 20,
                "changed_files": 5
            },
            "repository": {
                "full_name": "owner/repo",
                "name": "repo",
                "private": False
            },
            "sender": {"login": "developer", "id": 12345}
        }

        parsed = GitHubWebhookPayload.model_validate(payload)

        assert parsed.action == "opened"
        assert parsed.pull_request.number == 42
        assert parsed.pull_request.title == "Add new feature"
        assert parsed.repository.full_name == "owner/repo"

    def test_parse_minimal_payload(self):
        """Test parsing minimal webhook payload."""
        payload = {
            "action": "created",
            "repository": {
                "full_name": "owner/repo",
                "name": "repo"
            },
            "sender": {"login": "user", "id": 1}
        }

        parsed = GitHubWebhookPayload.model_validate(payload)

        assert parsed.action == "created"
        assert parsed.pull_request is None


class TestAnalysisSchemas:
    """Test analysis-related schemas."""

    def test_analysis_summary(self):
        """Test AnalysisSummary schema."""
        summary = AnalysisSummary(
            critical=2,
            warnings=5,
            suggestions=3,
            total_issues=10
        )

        assert summary.critical == 2
        assert summary.warnings == 5
        assert summary.total_issues == 10

    def test_analysis_summary_defaults(self):
        """Test AnalysisSummary default values."""
        summary = AnalysisSummary()

        assert summary.critical == 0
        assert summary.warnings == 0
        assert summary.suggestions == 0
        assert summary.total_issues == 0

    def test_issue_response(self):
        """Test IssueResponse schema."""
        issue = IssueResponse(
            id="issue-123",
            category=Category.security,
            severity=Severity.critical,
            file_path="src/auth.js",
            line_number=42,
            title="Hardcoded secret",
            message="API key found in source",
            explanation="Secrets should not be in code",
            suggestion="Use environment variables",
            created_at=datetime.now()
        )

        assert issue.category == Category.security
        assert issue.severity == Severity.critical
        assert issue.line_number == 42


class TestFeedbackSchemas:
    """Test feedback-related schemas."""

    def test_feedback_create(self):
        """Test FeedbackCreate schema."""
        feedback = FeedbackCreate(
            issue_id="issue-123",
            is_helpful=False,
            reason="false_positive",
            comment="This is intentional"
        )

        assert feedback.issue_id == "issue-123"
        assert feedback.is_helpful is False
        assert feedback.reason == "false_positive"

    def test_feedback_create_minimal(self):
        """Test FeedbackCreate with minimal data."""
        feedback = FeedbackCreate(
            issue_id="issue-123",
            is_helpful=True
        )

        assert feedback.is_helpful is True
        assert feedback.reason is None


class TestClaudeSchemas:
    """Test Claude analysis result schemas."""

    def test_claude_issue(self):
        """Test ClaudeIssue schema."""
        issue = ClaudeIssue(
            category="security",
            severity="critical",
            file_path="src/api.js",
            line_number=100,
            title="SQL Injection",
            message="User input used directly in query"
        )

        assert issue.category == "security"
        assert issue.severity == "critical"

    def test_claude_analysis_result(self):
        """Test ClaudeAnalysisResult schema."""
        result = ClaudeAnalysisResult(
            issues=[
                ClaudeIssue(
                    category="quality",
                    severity="warning",
                    file_path="test.js",
                    title="Issue",
                    message="Message"
                )
            ],
            summary="Overall good code",
            has_tests=True,
            overall_quality="good"
        )

        assert len(result.issues) == 1
        assert result.has_tests is True
        assert result.overall_quality == "good"

    def test_claude_analysis_result_empty(self):
        """Test ClaudeAnalysisResult with no issues."""
        result = ClaudeAnalysisResult()

        assert result.issues == []
        assert result.has_tests is False


class TestEnums:
    """Test enum values."""

    def test_category_values(self):
        """Test Category enum values."""
        assert Category.security.value == "security"
        assert Category.quality.value == "quality"
        assert Category.testing.value == "testing"
        assert Category.docs.value == "docs"
        assert Category.performance.value == "performance"

    def test_severity_values(self):
        """Test Severity enum values."""
        assert Severity.critical.value == "critical"
        assert Severity.warning.value == "warning"
        assert Severity.suggestion.value == "suggestion"

    def test_analysis_status_values(self):
        """Test AnalysisStatus enum values."""
        assert AnalysisStatus.pending.value == "pending"
        assert AnalysisStatus.processing.value == "processing"
        assert AnalysisStatus.completed.value == "completed"
        assert AnalysisStatus.failed.value == "failed"
