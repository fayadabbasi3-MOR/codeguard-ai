import hashlib
import hmac
from fastapi import APIRouter, Request, HTTPException, BackgroundTasks, Depends
from sqlalchemy.orm import Session

from ..config import get_settings
from ..models.database import get_db, PRAnalysis, Issue
from ..models.schemas import GitHubWebhookPayload, WebhookResponse, Category, Severity
from ..services.analyzer import get_analyzer_service
from ..services.github import get_github_service

router = APIRouter()
settings = get_settings()


def verify_signature(payload: bytes, signature: str) -> bool:
    """Verify GitHub webhook signature."""
    if not settings.github_webhook_secret:
        return True  # Skip verification if no secret configured (dev mode)

    expected = hmac.new(
        settings.github_webhook_secret.encode(),
        payload,
        hashlib.sha256
    ).hexdigest()

    return hmac.compare_digest(f"sha256={expected}", signature)


async def process_pr_analysis(
    analysis_id: str,
    repo: str,
    pr_number: int,
    db: Session
):
    """Background task to analyze a PR."""
    analyzer = get_analyzer_service()
    github = get_github_service()

    # Update status to processing
    analysis = db.query(PRAnalysis).filter(PRAnalysis.id == analysis_id).first()
    if not analysis:
        return

    analysis.status = "processing"
    db.commit()

    try:
        # Fetch PR diff
        diff, pr_info = github.get_pr_diff(repo, pr_number)

        if "error" in pr_info:
            analysis.status = "failed"
            analysis.error_message = pr_info["error"]
            db.commit()
            return

        # Update analysis with PR info
        analysis.pr_title = pr_info.get("title")
        analysis.author = pr_info.get("author")
        analysis.pr_url = pr_info.get("url")
        analysis.files_changed = pr_info.get("changed_files", 0)
        analysis.lines_added = pr_info.get("additions", 0)
        analysis.lines_removed = pr_info.get("deletions", 0)

        # Analyze with Claude
        result, analysis_time_ms, tokens_used = await analyzer.analyze_diff(
            repo=repo,
            pr_title=analysis.pr_title or "",
            author=analysis.author or "",
            diff=diff
        )

        analysis.analysis_time_ms = analysis_time_ms
        analysis.tokens_used = tokens_used

        # Create issues
        critical_count = 0
        warning_count = 0
        suggestion_count = 0

        for issue_data in result.issues:
            issue = Issue(
                analysis_id=analysis_id,
                category=issue_data.category,
                severity=issue_data.severity,
                file_path=issue_data.file_path,
                line_number=issue_data.line_number,
                title=issue_data.title,
                message=issue_data.message,
                explanation=issue_data.explanation,
                suggestion=issue_data.suggestion,
            )
            db.add(issue)

            if issue_data.severity == "critical":
                critical_count += 1
            elif issue_data.severity == "warning":
                warning_count += 1
            else:
                suggestion_count += 1

        analysis.critical_count = critical_count
        analysis.warning_count = warning_count
        analysis.suggestion_count = suggestion_count
        analysis.status = "completed"

        db.commit()

        # Post review comment to GitHub
        db.refresh(analysis)
        issues_response = []
        for issue in analysis.issues:
            from ..models.schemas import IssueResponse
            issues_response.append(IssueResponse(
                id=issue.id,
                category=Category(issue.category),
                severity=Severity(issue.severity),
                file_path=issue.file_path,
                line_number=issue.line_number,
                title=issue.title,
                message=issue.message,
                explanation=issue.explanation,
                suggestion=issue.suggestion,
                is_helpful=issue.is_helpful,
                dismiss_reason=issue.dismiss_reason,
                github_comment_id=issue.github_comment_id,
                created_at=issue.created_at,
            ))

        comment_body = github.format_review_comment(issues_response, result.summary)
        github.post_review_comment(repo, pr_number, comment_body)

    except Exception as e:
        print(f"Error processing PR: {e}")
        analysis.status = "failed"
        analysis.error_message = str(e)
        db.commit()


@router.post("/github", response_model=WebhookResponse)
async def github_webhook(
    request: Request,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """Handle GitHub webhook events."""
    # Get raw body for signature verification
    body = await request.body()

    # Verify signature (optional in dev mode)
    signature = request.headers.get("X-Hub-Signature-256", "")
    if settings.github_webhook_secret and not verify_signature(body, signature):
        raise HTTPException(status_code=401, detail="Invalid signature")

    # Parse payload
    try:
        payload = GitHubWebhookPayload.model_validate_json(body)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid payload: {e}")

    # Only process PR events
    event_type = request.headers.get("X-GitHub-Event", "")
    if event_type != "pull_request":
        return WebhookResponse(
            status="ignored",
            message=f"Event type '{event_type}' not processed"
        )

    # Only process opened and synchronize actions
    if payload.action not in ["opened", "synchronize", "reopened"]:
        return WebhookResponse(
            status="ignored",
            message=f"Action '{payload.action}' not processed"
        )

    if not payload.pull_request:
        return WebhookResponse(
            status="ignored",
            message="No pull request in payload"
        )

    # Create analysis record
    analysis = PRAnalysis(
        repo=payload.repository.full_name,
        pr_number=payload.pull_request.number,
        pr_title=payload.pull_request.title,
        pr_url=payload.pull_request.html_url,
        author=payload.pull_request.user.login,
        status="pending",
    )
    db.add(analysis)
    db.commit()
    db.refresh(analysis)

    # Queue background analysis
    background_tasks.add_task(
        process_pr_analysis,
        analysis.id,
        payload.repository.full_name,
        payload.pull_request.number,
        db
    )

    return WebhookResponse(
        status="processing",
        message="Analysis queued",
        analysis_id=analysis.id
    )


@router.post("/test", response_model=WebhookResponse)
async def test_analysis(
    repo: str,
    pr_number: int,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """Manually trigger analysis for testing."""
    # Create analysis record
    analysis = PRAnalysis(
        repo=repo,
        pr_number=pr_number,
        status="pending",
    )
    db.add(analysis)
    db.commit()
    db.refresh(analysis)

    # Queue background analysis
    background_tasks.add_task(
        process_pr_analysis,
        analysis.id,
        repo,
        pr_number,
        db
    )

    return WebhookResponse(
        status="processing",
        message="Analysis queued",
        analysis_id=analysis.id
    )
