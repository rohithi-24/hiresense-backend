from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.utils import get_current_user
from app import models

router = APIRouter()

@router.get("/me/stats")
def get_my_stats(db: Session = Depends(get_db), user=Depends(get_current_user)):
    applications = db.query(models.Application).filter(
        models.Application.user_id == user.id
    ).all()

    scored = [a.ai_score for a in applications if a.ai_score]
    avg_score = round(sum(scored) / len(scored), 1) if scored else 0

    return {
        "ai_score_avg": avg_score,
        "profile_views": user.profile_views or 0,
    }


@router.post("/me/track-view")
def track_profile_view(user_id: int, db: Session = Depends(get_db)):
    target = db.query(models.User).filter(models.User.id == user_id).first()
    if target:
        target.profile_views = (target.profile_views or 0) + 1
        db.commit()
    return {"ok": True}