from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.entities import InterviewQuestion
from app.schemas.analysis import InterviewQuestionSchema

router = APIRouter(prefix="/interview", tags=["Interview Preparation"])

@router.get("/{analysis_id}")
def get_interview_questions(analysis_id: str, db: Session = Depends(get_db)):
    """Retrieves project-specific viva and interview questions."""
    questions = (
        db.query(InterviewQuestion)
        .filter(InterviewQuestion.analysis_id == analysis_id)
        .order_by(InterviewQuestion.category.asc())
        .all()
    )
    return [
        InterviewQuestionSchema(
            id=q.id,
            category=q.category,
            difficulty=q.difficulty,
            question=q.question,
            expected_answer=q.expected_answer,
            relevant_file=q.relevant_file,
            follow_up_question=q.follow_up_question
        )
        for q in questions
    ]
