import uuid
from datetime import datetime
from sqlalchemy import Column, String, Integer, Float, Boolean, Text, ForeignKey, DateTime, JSON
from sqlalchemy.orm import relationship
from app.database import Base

def generate_uuid():
    return str(uuid.uuid4())

class User(Base):
    __tablename__ = "users"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    email = Column(String(255), unique=True, nullable=False, index=True)
    github_username = Column(String(100), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    repositories = relationship("Repository", back_populates="user", cascade="all, delete-orphan")


class Repository(Base):
    __tablename__ = "repositories"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    user_id = Column(String(36), ForeignKey("users.id"), nullable=True)
    github_url = Column(String(512), nullable=False)
    owner = Column(String(100), nullable=False, index=True)
    repo_name = Column(String(100), nullable=False, index=True)
    default_branch = Column(String(50), default="main")
    description = Column(Text, nullable=True)
    stars = Column(Integer, default=0)
    forks = Column(Integer, default=0)
    is_private = Column(Boolean, default=False)
    primary_language = Column(String(50), nullable=True)
    file_count = Column(Integer, default=0)
    last_analyzed_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="repositories")
    analyses = relationship("AnalysisRun", back_populates="repository", cascade="all, delete-orphan", order_by="desc(AnalysisRun.created_at)")
    messages = relationship("MentorMessage", back_populates="repository", cascade="all, delete-orphan", order_by="MentorMessage.created_at")


class AnalysisRun(Base):
    __tablename__ = "analysis_runs"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    repository_id = Column(String(36), ForeignKey("repositories.id"), nullable=False, index=True)
    status = Column(String(20), default="completed")  # queued, processing, completed, failed
    overall_score = Column(Integer, default=0)
    category_scores = Column(JSON, default=dict)
    project_summary = Column(JSON, default=dict)
    quality_metrics = Column(JSON, default=dict)
    readme_analysis = Column(JSON, default=dict)
    execution_time_seconds = Column(Float, default=0.0)
    error_message = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    repository = relationship("Repository", back_populates="analyses")
    findings = relationship("CodeFinding", back_populates="analysis", cascade="all, delete-orphan")
    feature_gaps = relationship("FeatureGap", back_populates="analysis", cascade="all, delete-orphan")
    roadmap_items = relationship("RoadmapItem", back_populates="analysis", cascade="all, delete-orphan")
    interview_questions = relationship("InterviewQuestion", back_populates="analysis", cascade="all, delete-orphan")


class CodeFinding(Base):
    __tablename__ = "code_findings"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    analysis_id = Column(String(36), ForeignKey("analysis_runs.id"), nullable=False, index=True)
    category = Column(String(30), nullable=False)  # security, quality, architecture, testing, style
    severity = Column(String(20), nullable=False)  # critical, high, medium, low, info
    title = Column(String(255), nullable=False)
    file_path = Column(String(512), nullable=False)
    line_number = Column(Integer, nullable=True)
    snippet = Column(Text, nullable=True)
    explanation = Column(Text, nullable=False)
    recommendation = Column(Text, nullable=False)
    cwe_id = Column(String(50), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    analysis = relationship("AnalysisRun", back_populates="findings")


class FeatureGap(Base):
    __tablename__ = "feature_gaps"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    analysis_id = Column(String(36), ForeignKey("analysis_runs.id"), nullable=False, index=True)
    capability_name = Column(String(255), nullable=False)
    category = Column(String(100), nullable=False)
    status = Column(String(30), nullable=False)  # Implemented, Partially Implemented, Missing, Cannot Determine
    evidence_summary = Column(Text, nullable=False)
    affected_files = Column(JSON, default=list)
    importance = Column(String(20), default="medium")  # critical, high, medium, low
    created_at = Column(DateTime, default=datetime.utcnow)

    analysis = relationship("AnalysisRun", back_populates="feature_gaps")


class RoadmapItem(Base):
    __tablename__ = "roadmap_items"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    analysis_id = Column(String(36), ForeignKey("analysis_runs.id"), nullable=False, index=True)
    phase = Column(Integer, nullable=False)  # 1 to 6
    title = Column(String(255), nullable=False)
    category = Column(String(50), nullable=False)
    priority = Column(String(10), default="P1")  # P0, P1, P2, P3
    difficulty = Column(String(20), default="medium")  # easy, medium, hard
    dependencies = Column(JSON, default=list)
    affected_files = Column(JSON, default=list)
    impact = Column(Text, nullable=False)
    action_step = Column(Text, nullable=False)
    completed = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    analysis = relationship("AnalysisRun", back_populates="roadmap_items")


class MentorMessage(Base):
    __tablename__ = "mentor_messages"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    repository_id = Column(String(36), ForeignKey("repositories.id"), nullable=False, index=True)
    sender = Column(String(20), nullable=False)  # user, mentor
    message = Column(Text, nullable=False)
    citations = Column(JSON, default=list)  # list of {file, line, reason}
    created_at = Column(DateTime, default=datetime.utcnow)

    repository = relationship("Repository", back_populates="messages")


class InterviewQuestion(Base):
    __tablename__ = "interview_questions"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    analysis_id = Column(String(36), ForeignKey("analysis_runs.id"), nullable=False, index=True)
    category = Column(String(30), nullable=False)  # Basic, Architecture, Code, Database, Security, Advanced
    difficulty = Column(String(20), default="Intermediate")  # Beginner, Intermediate, Advanced
    question = Column(Text, nullable=False)
    expected_answer = Column(Text, nullable=False)
    relevant_file = Column(String(512), nullable=True)
    follow_up_question = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    analysis = relationship("AnalysisRun", back_populates="interview_questions")
