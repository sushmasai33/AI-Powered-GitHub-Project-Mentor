from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.entities import Repository, AnalysisRun, CodeFinding, FeatureGap, MentorMessage
from app.schemas.analysis import MentorChatRequest, MentorChatResponse, CitationSchema
from app.services.rag_service import RAGMentorService
from app.services.sample_repos_data import SAMPLE_REPOSITORIES

router = APIRouter(prefix="/mentor", tags=["AI Mentor"])

@router.post("/chat", response_model=MentorChatResponse)
def chat_with_mentor(request: MentorChatRequest, db: Session = Depends(get_db)):
    """Converses with the repository-grounded AI mentor with RAG citations and injection defenses."""
    repo = db.query(Repository).filter(Repository.id == request.repository_id).first()
    if not repo:
        raise HTTPException(status_code=404, detail="Repository not found.")

    latest_analysis = (
        db.query(AnalysisRun)
        .filter(AnalysisRun.repository_id == repo.id)
        .order_by(AnalysisRun.created_at.desc())
        .first()
    )

    findings = []
    gaps = []
    if latest_analysis:
        findings = [
            {
                "title": f.title,
                "category": f.category,
                "severity": f.severity,
                "file_path": f.file_path,
                "line_number": f.line_number,
                "explanation": f.explanation,
                "recommendation": f.recommendation
            }
            for f in db.query(CodeFinding).filter(CodeFinding.analysis_id == latest_analysis.id).all()
        ]
        gaps = [
            {
                "capability_name": g.capability_name,
                "category": g.category,
                "status": g.status,
                "evidence_summary": g.evidence_summary,
                "affected_files": g.affected_files
            }
            for g in db.query(FeatureGap).filter(FeatureGap.analysis_id == latest_analysis.id).all()
        ]

    # Resolve file contents
    sample_key = f"{repo.owner}/{repo.repo_name}"
    file_contents = {}
    if sample_key in SAMPLE_REPOSITORIES:
        file_contents = SAMPLE_REPOSITORIES[sample_key].get("file_contents", {})
    else:
        # Fallback to files from quality_metrics
        file_contents = {
            "README.md": f"# {repo.repo_name}\n{repo.description or ''}",
            "main": f"Primary language: {repo.primary_language}"
        }

    rag_service = RAGMentorService(file_contents=file_contents)

    project_summary = latest_analysis.project_summary if latest_analysis else {}
    scoring_data = {
        "overall_score": latest_analysis.overall_score if latest_analysis else 70,
        "category_scores": latest_analysis.category_scores if latest_analysis else {}
    }

    # Record User Message
    user_msg_record = MentorMessage(
        repository_id=repo.id,
        sender="user",
        message=request.message,
        citations=[]
    )
    db.add(user_msg_record)

    response = rag_service.answer_query(
        query=request.message,
        project_summary=project_summary,
        scoring_data=scoring_data,
        security_findings=findings,
        feature_gaps=gaps
    )

    # Record Mentor Message
    mentor_msg_record = MentorMessage(
        repository_id=repo.id,
        sender="mentor",
        message=response.message,
        citations=[c.model_dump() for c in response.citations]
    )
    db.add(mentor_msg_record)
    db.commit()

    return response

@router.get("/history/{repo_id}")
def get_chat_history(repo_id: str, db: Session = Depends(get_db)):
    """Retrieves conversation transcript for repository."""
    messages = (
        db.query(MentorMessage)
        .filter(MentorMessage.repository_id == repo_id)
        .order_by(MentorMessage.created_at.asc())
        .all()
    )
    return [
        {
            "id": m.id,
            "sender": m.sender,
            "message": m.message,
            "citations": m.citations or [],
            "created_at": m.created_at
        }
        for m in messages
    ]
