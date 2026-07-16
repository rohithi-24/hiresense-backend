from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app import models, schemas
from app.utils import require_role

router = APIRouter()


@router.get("/", response_model=List[schemas.ApplicantOut])
def list_applicants(db: Session = Depends(get_db), _=Depends(require_role("admin"))):
    apps = db.query(models.Application).all()
    result = []
    for a in apps:
        user = db.query(models.User).filter(models.User.id == a.user_id).first()
        job = db.query(models.Job).filter(models.Job.id == a.job_id).first()
        result.append(schemas.ApplicantOut(
            id=a.id,
            name=user.name if user else "Unknown",
            email=user.email if user else "Unknown",
            applied_for=job.title if job else None,
            status=a.status,
            ai_score=a.ai_score,
            date=a.created_at.strftime("%b %d") if a.created_at else None,
        ))
    return result


@router.patch("/{app_id}/status")
def update_status(app_id: int, update: schemas.StatusUpdate, db: Session = Depends(get_db), _=Depends(require_role("admin"))):
    app = db.query(models.Application).filter(models.Application.id == app_id).first()
    if not app: raise HTTPException(status_code=404, detail="Application not found")
    app.status = update.status
    db.commit()
    return {"ok": True}