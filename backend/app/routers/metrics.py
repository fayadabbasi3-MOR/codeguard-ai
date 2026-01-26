from datetime import datetime, timedelta
from typing import Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, and_

from ..models.database import get_db, PRAnalysis, Issue
from ..models.schemas import (
    MetricsResponse,
    IssuesByCategory,
    IssuesBySeverity,
    DailyMetrics,
)

router = APIRouter()

# Estimate: 3 minutes saved per issue caught
MINUTES_SAVED_PER_ISSUE = 3


@router.get("/metrics", response_model=MetricsResponse)
async def get_metrics(
    repo: Optional[str] = Query(None, description="Filter by repository"),
    days: int = Query(30, ge=1, le=365, description="Number of days to include"),
    db: Session = Depends(get_db)
):
    """Get dashboard metrics."""
    # Date range filter
    start_date = datetime.utcnow() - timedelta(days=days)

    # Base query filters
    analysis_filters = [PRAnalysis.analyzed_at >= start_date]
    if repo:
        analysis_filters.append(PRAnalysis.repo == repo)

    # Total PRs analyzed
    total_prs = db.query(func.count(PRAnalysis.id)).filter(
        and_(*analysis_filters, PRAnalysis.status == "completed")
    ).scalar() or 0

    # Total issues found
    if repo:
        issue_query = (
            db.query(func.count(Issue.id))
            .join(PRAnalysis)
            .filter(and_(*analysis_filters))
        )
    else:
        issue_query = (
            db.query(func.count(Issue.id))
            .join(PRAnalysis)
            .filter(PRAnalysis.analyzed_at >= start_date)
        )
    total_issues = issue_query.scalar() or 0

    # Issues by category
    category_counts = {"security": 0, "quality": 0, "testing": 0, "docs": 0, "performance": 0}
    if repo:
        categories = (
            db.query(Issue.category, func.count(Issue.id))
            .join(PRAnalysis)
            .filter(and_(*analysis_filters))
            .group_by(Issue.category)
            .all()
        )
    else:
        categories = (
            db.query(Issue.category, func.count(Issue.id))
            .join(PRAnalysis)
            .filter(PRAnalysis.analyzed_at >= start_date)
            .group_by(Issue.category)
            .all()
        )
    for category, count in categories:
        if category in category_counts:
            category_counts[category] = count

    # Issues by severity
    severity_counts = {"critical": 0, "warning": 0, "suggestion": 0}
    if repo:
        severities = (
            db.query(Issue.severity, func.count(Issue.id))
            .join(PRAnalysis)
            .filter(and_(*analysis_filters))
            .group_by(Issue.severity)
            .all()
        )
    else:
        severities = (
            db.query(Issue.severity, func.count(Issue.id))
            .join(PRAnalysis)
            .filter(PRAnalysis.analyzed_at >= start_date)
            .group_by(Issue.severity)
            .all()
        )
    for severity, count in severities:
        if severity in severity_counts:
            severity_counts[severity] = count

    # Average issues per PR
    avg_issues = total_issues / total_prs if total_prs > 0 else 0

    # Estimated time saved (3 minutes per issue)
    time_saved_hours = (total_issues * MINUTES_SAVED_PER_ISSUE) / 60

    # Daily metrics for chart
    daily_metrics = []
    for i in range(min(days, 30)):  # Max 30 days for daily breakdown
        day = datetime.utcnow() - timedelta(days=i)
        day_start = day.replace(hour=0, minute=0, second=0, microsecond=0)
        day_end = day_start + timedelta(days=1)

        day_filters = [
            PRAnalysis.analyzed_at >= day_start,
            PRAnalysis.analyzed_at < day_end,
            PRAnalysis.status == "completed",
        ]
        if repo:
            day_filters.append(PRAnalysis.repo == repo)

        prs_count = db.query(func.count(PRAnalysis.id)).filter(and_(*day_filters)).scalar() or 0

        issues_count = db.query(func.sum(
            PRAnalysis.critical_count + PRAnalysis.warning_count + PRAnalysis.suggestion_count
        )).filter(and_(*day_filters)).scalar() or 0

        critical_count = db.query(func.sum(PRAnalysis.critical_count)).filter(
            and_(*day_filters)
        ).scalar() or 0

        daily_metrics.append(DailyMetrics(
            date=day_start.strftime("%Y-%m-%d"),
            prs_analyzed=prs_count,
            issues_found=int(issues_count),
            critical_issues=int(critical_count),
        ))

    # Reverse to get chronological order
    daily_metrics.reverse()

    # Top issues (most common issue titles)
    top_issues_query = (
        db.query(Issue.title, Issue.category, Issue.severity, func.count(Issue.id).label("count"))
        .join(PRAnalysis)
        .filter(PRAnalysis.analyzed_at >= start_date)
    )
    if repo:
        top_issues_query = top_issues_query.filter(PRAnalysis.repo == repo)

    top_issues = (
        top_issues_query
        .group_by(Issue.title, Issue.category, Issue.severity)
        .order_by(func.count(Issue.id).desc())
        .limit(10)
        .all()
    )

    top_issues_list = [
        {
            "title": title,
            "category": category,
            "severity": severity,
            "count": count,
        }
        for title, category, severity, count in top_issues
    ]

    return MetricsResponse(
        total_prs_analyzed=total_prs,
        total_issues_found=total_issues,
        issues_by_category=IssuesByCategory(**category_counts),
        issues_by_severity=IssuesBySeverity(**severity_counts),
        avg_issues_per_pr=round(avg_issues, 2),
        estimated_time_saved_hours=round(time_saved_hours, 1),
        daily_metrics=daily_metrics,
        top_issues=top_issues_list,
    )


@router.get("/repos")
async def list_repos(db: Session = Depends(get_db)):
    """List all repositories with analyses."""
    repos = (
        db.query(PRAnalysis.repo, func.count(PRAnalysis.id).label("count"))
        .group_by(PRAnalysis.repo)
        .order_by(func.count(PRAnalysis.id).desc())
        .all()
    )

    return [{"repo": repo, "analysis_count": count} for repo, count in repos]
