from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import desc

from ..models.database import get_db, PRAnalysis, Issue, Feedback
from ..models.schemas import (
    AnalysisResponse,
    AnalysisListItem,
    AnalysisSummary,
    AnalysisMetadata,
    IssueResponse,
    FeedbackCreate,
    FeedbackResponse,
    Category,
    Severity,
    AnalysisStatus,
)

router = APIRouter()


def analysis_to_response(analysis: PRAnalysis) -> AnalysisResponse:
    """Convert database model to response schema."""
    issues = [
        IssueResponse(
            id=issue.id,
            category=Category(issue.category),
            severity=Severity(issue.severity),
            file_path=issue.file_path,
            line_number=issue.line_number,
            title=issue.title,
            message=issue.message,
            explanation=issue.explanation,
            suggestion=issue.suggestion,
            code_snippet=issue.code_snippet,
            is_helpful=issue.is_helpful,
            dismiss_reason=issue.dismiss_reason,
            github_comment_id=issue.github_comment_id,
            created_at=issue.created_at,
        )
        for issue in analysis.issues
    ]

    return AnalysisResponse(
        id=analysis.id,
        repo=analysis.repo,
        pr_number=analysis.pr_number,
        pr_title=analysis.pr_title,
        pr_url=analysis.pr_url,
        author=analysis.author,
        status=AnalysisStatus(analysis.status),
        error_message=analysis.error_message,
        summary=AnalysisSummary(
            critical=analysis.critical_count,
            warnings=analysis.warning_count,
            suggestions=analysis.suggestion_count,
            total_issues=analysis.critical_count + analysis.warning_count + analysis.suggestion_count,
        ),
        issues=issues,
        metadata=AnalysisMetadata(
            analyzed_at=analysis.analyzed_at,
            analysis_time_ms=analysis.analysis_time_ms,
            files_changed=analysis.files_changed,
            lines_added=analysis.lines_added,
            lines_removed=analysis.lines_removed,
            tokens_used=analysis.tokens_used,
        ),
    )


@router.get("/analyses", response_model=List[AnalysisListItem])
async def list_analyses(
    repo: Optional[str] = Query(None, description="Filter by repository"),
    status: Optional[str] = Query(None, description="Filter by status"),
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db)
):
    """List all analyses with optional filtering."""
    query = db.query(PRAnalysis)

    if repo:
        query = query.filter(PRAnalysis.repo == repo)
    if status:
        query = query.filter(PRAnalysis.status == status)

    analyses = query.order_by(desc(PRAnalysis.analyzed_at)).offset(offset).limit(limit).all()

    return [
        AnalysisListItem(
            id=a.id,
            repo=a.repo,
            pr_number=a.pr_number,
            pr_title=a.pr_title,
            author=a.author,
            status=AnalysisStatus(a.status),
            summary=AnalysisSummary(
                critical=a.critical_count,
                warnings=a.warning_count,
                suggestions=a.suggestion_count,
                total_issues=a.critical_count + a.warning_count + a.suggestion_count,
            ),
            analyzed_at=a.analyzed_at,
        )
        for a in analyses
    ]


@router.get("/analysis/{analysis_id}", response_model=AnalysisResponse)
async def get_analysis(
    analysis_id: str,
    db: Session = Depends(get_db)
):
    """Get a specific analysis by ID."""
    analysis = db.query(PRAnalysis).filter(PRAnalysis.id == analysis_id).first()

    if not analysis:
        raise HTTPException(status_code=404, detail="Analysis not found")

    return analysis_to_response(analysis)


@router.get("/pr/{repo:path}/{pr_number}", response_model=AnalysisResponse)
async def get_pr_analysis(
    repo: str,
    pr_number: int,
    db: Session = Depends(get_db)
):
    """Get the latest analysis for a specific PR."""
    analysis = (
        db.query(PRAnalysis)
        .filter(PRAnalysis.repo == repo, PRAnalysis.pr_number == pr_number)
        .order_by(desc(PRAnalysis.analyzed_at))
        .first()
    )

    if not analysis:
        raise HTTPException(status_code=404, detail="No analysis found for this PR")

    return analysis_to_response(analysis)


@router.post("/feedback", response_model=FeedbackResponse)
async def submit_feedback(
    feedback: FeedbackCreate,
    db: Session = Depends(get_db)
):
    """Submit feedback on an issue."""
    # Verify issue exists
    issue = db.query(Issue).filter(Issue.id == feedback.issue_id).first()
    if not issue:
        raise HTTPException(status_code=404, detail="Issue not found")

    # Get repo from analysis
    analysis = db.query(PRAnalysis).filter(PRAnalysis.id == issue.analysis_id).first()

    # Update issue
    issue.is_helpful = feedback.is_helpful
    if feedback.reason:
        issue.dismiss_reason = feedback.reason

    # Create feedback record
    feedback_record = Feedback(
        issue_id=feedback.issue_id,
        repo=analysis.repo if analysis else "",
        is_helpful=feedback.is_helpful,
        reason=feedback.reason,
        comment=feedback.comment,
    )
    db.add(feedback_record)
    db.commit()
    db.refresh(feedback_record)

    return FeedbackResponse(
        id=feedback_record.id,
        issue_id=feedback_record.issue_id,
        is_helpful=feedback_record.is_helpful,
        reason=feedback_record.reason,
        created_at=feedback_record.created_at,
    )
