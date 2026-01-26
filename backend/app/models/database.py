from sqlalchemy import create_engine, Column, String, Integer, Float, Boolean, DateTime, Text, ForeignKey, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
import uuid

from ..config import get_settings

settings = get_settings()

engine = create_engine(
    settings.database_url,
    connect_args={"check_same_thread": False}  # SQLite specific
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def generate_uuid():
    return str(uuid.uuid4())


class PRAnalysis(Base):
    __tablename__ = "pr_analyses"

    id = Column(String, primary_key=True, default=generate_uuid)
    repo = Column(String, nullable=False, index=True)
    pr_number = Column(Integer, nullable=False)
    pr_title = Column(String, nullable=True)
    pr_url = Column(String, nullable=True)
    author = Column(String, nullable=True)

    # Analysis metadata
    analyzed_at = Column(DateTime, default=datetime.utcnow)
    status = Column(String, default="pending")  # pending, processing, completed, failed
    error_message = Column(Text, nullable=True)

    # Stats
    files_changed = Column(Integer, default=0)
    lines_added = Column(Integer, default=0)
    lines_removed = Column(Integer, default=0)
    analysis_time_ms = Column(Integer, default=0)
    tokens_used = Column(Integer, default=0)

    # Summary counts
    critical_count = Column(Integer, default=0)
    warning_count = Column(Integer, default=0)
    suggestion_count = Column(Integer, default=0)

    # Relationships
    issues = relationship("Issue", back_populates="analysis", cascade="all, delete-orphan")


class Issue(Base):
    __tablename__ = "issues"

    id = Column(String, primary_key=True, default=generate_uuid)
    analysis_id = Column(String, ForeignKey("pr_analyses.id"), nullable=False)

    # Issue details
    category = Column(String, nullable=False)  # security, quality, testing, docs
    severity = Column(String, nullable=False)  # critical, warning, suggestion
    file_path = Column(String, nullable=False)
    line_number = Column(Integer, nullable=True)

    # Content
    title = Column(String, nullable=False)
    message = Column(Text, nullable=False)
    explanation = Column(Text, nullable=True)
    suggestion = Column(Text, nullable=True)
    code_snippet = Column(Text, nullable=True)

    # Feedback
    is_helpful = Column(Boolean, nullable=True)
    dismiss_reason = Column(String, nullable=True)

    # GitHub comment tracking
    github_comment_id = Column(String, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    analysis = relationship("PRAnalysis", back_populates="issues")


class Feedback(Base):
    __tablename__ = "feedback"

    id = Column(String, primary_key=True, default=generate_uuid)
    issue_id = Column(String, ForeignKey("issues.id"), nullable=False)
    repo = Column(String, nullable=False, index=True)

    # Feedback data
    is_helpful = Column(Boolean, nullable=False)
    reason = Column(String, nullable=True)
    comment = Column(Text, nullable=True)

    # Metadata
    user = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class RepoConfig(Base):
    __tablename__ = "repo_configs"

    id = Column(String, primary_key=True, default=generate_uuid)
    repo = Column(String, nullable=False, unique=True, index=True)

    # Settings
    enabled = Column(Boolean, default=True)
    enabled_rules = Column(JSON, default=list)
    disabled_rules = Column(JSON, default=list)
    severity_overrides = Column(JSON, default=dict)
    custom_prompts = Column(JSON, default=dict)

    # Learning mode
    auto_adjust_enabled = Column(Boolean, default=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


def init_db():
    """Create all database tables."""
    Base.metadata.create_all(bind=engine)


def get_db():
    """Dependency for FastAPI to get database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
