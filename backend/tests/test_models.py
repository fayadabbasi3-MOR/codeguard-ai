"""Tests for database models."""
import pytest
from datetime import datetime

from app.models.database import PRAnalysis, Issue, Feedback, RepoConfig


class TestPRAnalysisModel:
    """Test PRAnalysis model."""

    def test_create_analysis(self, db_session):
        """Test creating a PR analysis."""
        analysis = PRAnalysis(
            repo="owner/repo",
            pr_number=1,
            pr_title="Test PR",
            status="pending"
        )
        db_session.add(analysis)
        db_session.commit()

        assert analysis.id is not None
        assert analysis.repo == "owner/repo"
        assert analysis.pr_number == 1
        assert analysis.status == "pending"
        assert analysis.analyzed_at is not None

    def test_analysis_defaults(self, db_session):
        """Test PR analysis default values."""
        analysis = PRAnalysis(repo="owner/repo", pr_number=1)
        db_session.add(analysis)
        db_session.commit()

        assert analysis.status == "pending"
        assert analysis.files_changed == 0
        assert analysis.lines_added == 0
        assert analysis.lines_removed == 0
        assert analysis.critical_count == 0
        assert analysis.warning_count == 0
        assert analysis.suggestion_count == 0

    def test_analysis_with_issues(self, db_session):
        """Test PR analysis with related issues."""
        analysis = PRAnalysis(repo="owner/repo", pr_number=1)
        db_session.add(analysis)
        db_session.commit()

        issue = Issue(
            analysis_id=analysis.id,
            category="security",
            severity="critical",
            file_path="test.js",
            title="Test issue",
            message="Test message"
        )
        db_session.add(issue)
        db_session.commit()

        db_session.refresh(analysis)
        assert len(analysis.issues) == 1
        assert analysis.issues[0].category == "security"


class TestIssueModel:
    """Test Issue model."""

    def test_create_issue(self, db_session):
        """Test creating an issue."""
        analysis = PRAnalysis(repo="owner/repo", pr_number=1)
        db_session.add(analysis)
        db_session.commit()

        issue = Issue(
            analysis_id=analysis.id,
            category="quality",
            severity="warning",
            file_path="src/file.js",
            line_number=42,
            title="Code smell",
            message="This could be improved",
            explanation="Here's why",
            suggestion="Do this instead"
        )
        db_session.add(issue)
        db_session.commit()

        assert issue.id is not None
        assert issue.category == "quality"
        assert issue.severity == "warning"
        assert issue.line_number == 42
        assert issue.is_helpful is None  # No feedback yet

    def test_issue_feedback(self, db_session):
        """Test updating issue feedback."""
        analysis = PRAnalysis(repo="owner/repo", pr_number=1)
        db_session.add(analysis)
        db_session.commit()

        issue = Issue(
            analysis_id=analysis.id,
            category="testing",
            severity="suggestion",
            file_path="test.js",
            title="Add test",
            message="Consider adding tests"
        )
        db_session.add(issue)
        db_session.commit()

        # Update with feedback
        issue.is_helpful = False
        issue.dismiss_reason = "false_positive"
        db_session.commit()

        db_session.refresh(issue)
        assert issue.is_helpful is False
        assert issue.dismiss_reason == "false_positive"


class TestFeedbackModel:
    """Test Feedback model."""

    def test_create_feedback(self, db_session):
        """Test creating feedback."""
        analysis = PRAnalysis(repo="owner/repo", pr_number=1)
        db_session.add(analysis)
        db_session.commit()

        issue = Issue(
            analysis_id=analysis.id,
            category="docs",
            severity="suggestion",
            file_path="README.md",
            title="Update docs",
            message="Docs need updating"
        )
        db_session.add(issue)
        db_session.commit()

        feedback = Feedback(
            issue_id=issue.id,
            repo="owner/repo",
            is_helpful=True,
            user="testuser"
        )
        db_session.add(feedback)
        db_session.commit()

        assert feedback.id is not None
        assert feedback.is_helpful is True
        assert feedback.created_at is not None


class TestRepoConfigModel:
    """Test RepoConfig model."""

    def test_create_config(self, db_session):
        """Test creating repo configuration."""
        config = RepoConfig(
            repo="owner/repo",
            enabled=True,
            enabled_rules=["security", "quality"],
            disabled_rules=["docs"],
        )
        db_session.add(config)
        db_session.commit()

        assert config.id is not None
        assert config.enabled is True
        assert "security" in config.enabled_rules
        assert "docs" in config.disabled_rules

    def test_config_defaults(self, db_session):
        """Test repo config default values."""
        config = RepoConfig(repo="owner/repo")
        db_session.add(config)
        db_session.commit()

        assert config.enabled is True
        assert config.auto_adjust_enabled is True
        assert config.enabled_rules == []
        assert config.disabled_rules == []
