import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.models.database import Base, get_db


# Create in-memory SQLite database for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(scope="function")
def db_session():
    """Create a fresh database for each test."""
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    yield db
    db.close()
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db_session):
    """Create a test client with database override."""
    app.dependency_overrides[get_db] = override_get_db
    Base.metadata.create_all(bind=engine)

    with TestClient(app) as test_client:
        yield test_client

    Base.metadata.drop_all(bind=engine)
    app.dependency_overrides.clear()


@pytest.fixture
def sample_pr_analysis(db_session):
    """Create a sample PR analysis for testing."""
    from app.models.database import PRAnalysis, Issue
    from datetime import datetime

    analysis = PRAnalysis(
        id="test-analysis-123",
        repo="test-owner/test-repo",
        pr_number=42,
        pr_title="Test PR",
        pr_url="https://github.com/test-owner/test-repo/pull/42",
        author="test-user",
        status="completed",
        files_changed=3,
        lines_added=100,
        lines_removed=20,
        analysis_time_ms=2500,
        tokens_used=500,
        critical_count=1,
        warning_count=2,
        suggestion_count=1,
    )
    db_session.add(analysis)

    # Add sample issues
    issues = [
        Issue(
            id="issue-1",
            analysis_id="test-analysis-123",
            category="security",
            severity="critical",
            file_path="src/api/auth.js",
            line_number=23,
            title="Hardcoded API key",
            message="API key is hardcoded in source",
            explanation="Hardcoded secrets can be extracted from version control",
            suggestion="Move to environment variable",
        ),
        Issue(
            id="issue-2",
            analysis_id="test-analysis-123",
            category="quality",
            severity="warning",
            file_path="src/utils/helpers.js",
            line_number=45,
            title="Console.log in production",
            message="console.log found in production code",
            explanation="Can leak sensitive data and impact performance",
            suggestion="Remove or use proper logging library",
        ),
        Issue(
            id="issue-3",
            analysis_id="test-analysis-123",
            category="quality",
            severity="warning",
            file_path="src/components/Dashboard.jsx",
            line_number=127,
            title="Long function",
            message="Function is 78 lines long",
            explanation="Long functions are harder to maintain",
            suggestion="Break into smaller functions",
        ),
        Issue(
            id="issue-4",
            analysis_id="test-analysis-123",
            category="docs",
            severity="suggestion",
            file_path="README.md",
            line_number=None,
            title="Update documentation",
            message="README hasn't been updated with new endpoints",
            explanation="Outdated docs cause confusion",
            suggestion="Add new API endpoints to README",
        ),
    ]

    for issue in issues:
        db_session.add(issue)

    db_session.commit()
    db_session.refresh(analysis)

    return analysis
