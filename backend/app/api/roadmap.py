from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.entities import RoadmapItem
from app.schemas.analysis import RoadmapItemSchema

router = APIRouter(prefix="/roadmap", tags=["Roadmap"])

@router.get("/{analysis_id}")
def get_roadmap(analysis_id: str, db: Session = Depends(get_db)):
    """Retrieves all 6 phases of the personalized roadmap."""
    items = (
        db.query(RoadmapItem)
        .filter(RoadmapItem.analysis_id == analysis_id)
        .order_by(RoadmapItem.phase.asc(), RoadmapItem.priority.asc())
        .all()
    )
    return [
        RoadmapItemSchema(
            id=item.id,
            phase=item.phase,
            title=item.title,
            category=item.category,
            priority=item.priority,
            difficulty=item.difficulty,
            dependencies=item.dependencies or [],
            affected_files=item.affected_files or [],
            impact=item.impact,
            action_step=item.action_step,
            completed=item.completed
        )
        for item in items
    ]

@router.post("/item/{item_id}/toggle")
def toggle_roadmap_item(item_id: str, db: Session = Depends(get_db)):
    """Toggles checklist status for a roadmap improvement step."""
    item = db.query(RoadmapItem).filter(RoadmapItem.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Roadmap item not found.")
    
    item.completed = not item.completed
    db.commit()
    db.refresh(item)

    return {"id": item.id, "completed": item.completed}
