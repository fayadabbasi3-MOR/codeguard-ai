from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum


# Enums
class AnalysisStatus(str, Enum):
    pending = "pending"
    processing = "processing"
    completed = "completed"
    failed = "failed"


class Severity(str, Enum):
    critical = "critical"
    warning = "warning"
    suggestion = "suggestion"


class Category(str, Enum):
    security = "security"
    quality = "quality"
    testing = "testing"
    docs = "docs"
    performance = "performance"


# GitHub Webhook Schemas
class GitHubUser(BaseModel):
    login: str
    id: int


class GitHubRepo(BaseModel):
    full_name: str
    name: str
    private: bool = False


class GitHubCommit(BaseModel):
    sha: str
    ref: Optional[str] = None


class GitHubPullRequest(BaseModel):
    number: int
    title: str
    html_url: str
    state: str
    head: GitHubCommit
    base: GitHubCommit
    user: GitHubUser
    additions: Optional[int] = 0
    deletions: Optional[int] = 0
    changed_files: Optional[int] = 0


class GitHubWebhookPayload(BaseModel):
    action: str
    pull_request: Optional[GitHubPullRequest] = None
    repository: GitHubRepo
    sender: GitHubUser


# Issue Schemas
class IssueBase(BaseModel):
    category: Category
    severity: Severity
    file_path: str
    line_number: Optional[int] = None
    title: str
    message: str
    explanation: Optional[str] = None
    suggestion: Optional[str] = None
    code_snippet: Optional[str] = None


class IssueCreate(IssueBase):
    pass


class IssueResponse(IssueBase):
    id: str
    is_helpful: Optional[bool] = None
    dismiss_reason: Optional[str] = None
    github_comment_id: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True


# Analysis Schemas
class AnalysisSummary(BaseModel):
    critical: int = 0
    warnings: int = 0
    suggestions: int = 0
    total_issues: int = 0


class AnalysisMetadata(BaseModel):
    analyzed_at: datetime
    analysis_time_ms: int
    files_changed: int
    lines_added: int
    lines_removed: int
    tokens_used: int


class AnalysisCreate(BaseModel):
    repo: str
    pr_number: int
    pr_title: Optional[str] = None
    pr_url: Optional[str] = None
    author: Optional[str] = None


class AnalysisResponse(BaseModel):
    id: str
    repo: str
    pr_number: int
    pr_title: Optional[str] = None
    pr_url: Optional[str] = None
    author: Optional[str] = None
    status: AnalysisStatus
    error_message: Optional[str] = None
    summary: AnalysisSummary
    issues: List[IssueResponse] = []
    metadata: AnalysisMetadata

    class Config:
        from_attributes = True


class AnalysisListItem(BaseModel):
    id: str
    repo: str
    pr_number: int
    pr_title: Optional[str] = None
    author: Optional[str] = None
    status: AnalysisStatus
    summary: AnalysisSummary
    analyzed_at: datetime

    class Config:
        from_attributes = True


# Webhook Response
class WebhookResponse(BaseModel):
    status: str
    message: str
    analysis_id: Optional[str] = None


# Feedback Schemas
class FeedbackCreate(BaseModel):
    issue_id: str
    is_helpful: bool
    reason: Optional[str] = None
    comment: Optional[str] = None


class FeedbackResponse(BaseModel):
    id: str
    issue_id: str
    is_helpful: bool
    reason: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True


# Metrics Schemas
class IssuesByCategory(BaseModel):
    security: int = 0
    quality: int = 0
    testing: int = 0
    docs: int = 0
    performance: int = 0


class IssuesBySeverity(BaseModel):
    critical: int = 0
    warning: int = 0
    suggestion: int = 0


class DailyMetrics(BaseModel):
    date: str
    prs_analyzed: int = 0
    issues_found: int = 0
    critical_issues: int = 0


class MetricsResponse(BaseModel):
    total_prs_analyzed: int = 0
    total_issues_found: int = 0
    issues_by_category: IssuesByCategory
    issues_by_severity: IssuesBySeverity
    avg_issues_per_pr: float = 0.0
    estimated_time_saved_hours: float = 0.0
    daily_metrics: List[DailyMetrics] = []
    top_issues: List[Dict[str, Any]] = []


# Claude Analysis Response (internal)
class ClaudeIssue(BaseModel):
    category: str
    severity: str
    file_path: str
    line_number: Optional[int] = None
    title: str
    message: str
    explanation: Optional[str] = None
    suggestion: Optional[str] = None


class ClaudeAnalysisResult(BaseModel):
    issues: List[ClaudeIssue] = []
    summary: Optional[str] = None
    has_tests: bool = False
    overall_quality: Optional[str] = None
