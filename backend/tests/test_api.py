"""Tests for API endpoints."""
import pytest
from fastapi import status


class TestHealthEndpoints:
    """Test health check endpoints."""

    def test_root_endpoint(self, client):
        """Test root endpoint returns API info."""
        response = client.get("/")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["name"] == "CodeGuard API"
        assert data["status"] == "running"
        assert "version" in data

    def test_health_endpoint(self, client):
        """Test health endpoint returns healthy status."""
        response = client.get("/health")
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["status"] == "healthy"


class TestAnalysisEndpoints:
    """Test analysis-related endpoints."""

    def test_list_analyses_empty(self, client):
        """Test listing analyses when none exist."""
        response = client.get("/api/analyses")
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == []

    def test_list_analyses_with_data(self, client, sample_pr_analysis):
        """Test listing analyses returns data."""
        response = client.get("/api/analyses")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data) == 1
        assert data[0]["repo"] == "test-owner/test-repo"
        assert data[0]["pr_number"] == 42

    def test_list_analyses_filter_by_repo(self, client, sample_pr_analysis):
        """Test filtering analyses by repository."""
        response = client.get("/api/analyses?repo=test-owner/test-repo")
        assert response.status_code == status.HTTP_200_OK
        assert len(response.json()) == 1

        response = client.get("/api/analyses?repo=other/repo")
        assert response.status_code == status.HTTP_200_OK
        assert len(response.json()) == 0

    def test_list_analyses_filter_by_status(self, client, sample_pr_analysis):
        """Test filtering analyses by status."""
        response = client.get("/api/analyses?status=completed")
        assert response.status_code == status.HTTP_200_OK
        assert len(response.json()) == 1

        response = client.get("/api/analyses?status=pending")
        assert response.status_code == status.HTTP_200_OK
        assert len(response.json()) == 0

    def test_get_analysis_by_id(self, client, sample_pr_analysis):
        """Test getting a specific analysis by ID."""
        response = client.get(f"/api/analysis/{sample_pr_analysis.id}")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["id"] == sample_pr_analysis.id
        assert data["repo"] == "test-owner/test-repo"
        assert data["pr_number"] == 42
        assert data["summary"]["critical"] == 1
        assert data["summary"]["warnings"] == 2
        assert data["summary"]["suggestions"] == 1
        assert data["summary"]["total_issues"] == 4
        assert len(data["issues"]) == 4

    def test_get_analysis_not_found(self, client):
        """Test getting non-existent analysis returns 404."""
        response = client.get("/api/analysis/non-existent-id")
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_get_pr_analysis(self, client, sample_pr_analysis):
        """Test getting analysis by repo and PR number."""
        response = client.get("/api/pr/test-owner/test-repo/42")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["pr_number"] == 42

    def test_get_pr_analysis_not_found(self, client):
        """Test getting analysis for non-existent PR returns 404."""
        response = client.get("/api/pr/test-owner/test-repo/999")
        assert response.status_code == status.HTTP_404_NOT_FOUND


class TestFeedbackEndpoints:
    """Test feedback-related endpoints."""

    def test_submit_feedback_helpful(self, client, sample_pr_analysis):
        """Test submitting positive feedback on an issue."""
        response = client.post("/api/feedback", json={
            "issue_id": "issue-1",
            "is_helpful": True,
        })
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["issue_id"] == "issue-1"
        assert data["is_helpful"] is True

    def test_submit_feedback_not_helpful(self, client, sample_pr_analysis):
        """Test submitting negative feedback with reason."""
        response = client.post("/api/feedback", json={
            "issue_id": "issue-2",
            "is_helpful": False,
            "reason": "false_positive",
            "comment": "This is intentional for debugging"
        })
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["is_helpful"] is False
        assert data["reason"] == "false_positive"

    def test_submit_feedback_invalid_issue(self, client):
        """Test submitting feedback for non-existent issue returns 404."""
        response = client.post("/api/feedback", json={
            "issue_id": "non-existent",
            "is_helpful": True,
        })
        assert response.status_code == status.HTTP_404_NOT_FOUND


class TestMetricsEndpoints:
    """Test metrics-related endpoints."""

    def test_get_metrics_empty(self, client):
        """Test getting metrics when no data exists."""
        response = client.get("/api/metrics")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["total_prs_analyzed"] == 0
        assert data["total_issues_found"] == 0

    def test_get_metrics_with_data(self, client, sample_pr_analysis):
        """Test getting metrics with data."""
        response = client.get("/api/metrics")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["total_prs_analyzed"] == 1
        assert data["total_issues_found"] == 4
        assert data["issues_by_severity"]["critical"] == 1
        assert data["issues_by_severity"]["warning"] == 2
        assert data["issues_by_severity"]["suggestion"] == 1
        assert data["issues_by_category"]["security"] == 1
        assert data["issues_by_category"]["quality"] == 2
        assert data["issues_by_category"]["docs"] == 1

    def test_get_metrics_filter_by_repo(self, client, sample_pr_analysis):
        """Test filtering metrics by repository."""
        response = client.get("/api/metrics?repo=test-owner/test-repo")
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["total_prs_analyzed"] == 1

        response = client.get("/api/metrics?repo=other/repo")
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["total_prs_analyzed"] == 0

    def test_get_metrics_filter_by_days(self, client, sample_pr_analysis):
        """Test filtering metrics by time range."""
        response = client.get("/api/metrics?days=7")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data["daily_metrics"]) <= 7

    def test_list_repos(self, client, sample_pr_analysis):
        """Test listing repositories with analyses."""
        response = client.get("/api/repos")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data) == 1
        assert data[0]["repo"] == "test-owner/test-repo"
        assert data[0]["analysis_count"] == 1

    def test_list_repos_empty(self, client):
        """Test listing repos when none have analyses."""
        response = client.get("/api/repos")
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == []


class TestWebhookEndpoints:
    """Test webhook-related endpoints."""

    def test_webhook_ignored_event(self, client):
        """Test webhook ignores non-PR events."""
        response = client.post(
            "/webhook/github",
            json={
                "action": "created",
                "repository": {"full_name": "test/repo", "name": "repo", "private": False},
                "sender": {"login": "user", "id": 1}
            },
            headers={"X-GitHub-Event": "issues"}
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["status"] == "ignored"

    def test_webhook_ignored_action(self, client):
        """Test webhook ignores non-relevant PR actions."""
        response = client.post(
            "/webhook/github",
            json={
                "action": "closed",
                "pull_request": {
                    "number": 1,
                    "title": "Test",
                    "html_url": "https://github.com/test/repo/pull/1",
                    "state": "closed",
                    "head": {"sha": "abc123"},
                    "base": {"sha": "def456"},
                    "user": {"login": "user", "id": 1}
                },
                "repository": {"full_name": "test/repo", "name": "repo", "private": False},
                "sender": {"login": "user", "id": 1}
            },
            headers={"X-GitHub-Event": "pull_request"}
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["status"] == "ignored"

    def test_test_analysis_endpoint(self, client):
        """Test manual analysis trigger endpoint."""
        response = client.post(
            "/webhook/test",
            params={"repo": "test/repo", "pr_number": 1}
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["status"] == "processing"
        assert "analysis_id" in data
