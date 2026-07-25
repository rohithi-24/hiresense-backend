from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app import models
from app.auth import get_current_user

router = APIRouter()


def log_activity(db: Session, user_id: int, action: str):
    entry = models.ActivityLog(user_id=user_id, action=action)
    db.add(entry)
    db.commit()


def require_admin(current_user=Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    return current_user


@router.get("/admin/reports")
def generate_reports(db: Session = Depends(get_db), current_user=Depends(require_admin)):
    users = db.query(models.User).all()
    jobs = db.query(models.Job).all()
    applications = db.query(models.Application).all()

    log_activity(db, current_user.id, "Generated Reports")

    return {
        "total_users": len(users),
        "total_jobs": len(jobs),
        "total_applications": len(applications),
        "users": [{"id": u.id, "name": u.name, "email": u.email, "role": u.role} for u in users],
        "jobs": [{"id": j.id, "title": j.title, "company": j.company} for j in jobs],
        "applications": [
            {
                "id": a.id,
                "job_id": a.job_id,
                "user_id": a.user_id,
                "status": a.status,
                "ai_score": a.ai_score,
            }
            for a in applications
        ],
    }


@router.get("/admin/activity-logs")
def get_activity_logs(limit: int = 20, db: Session = Depends(get_db), current_user=Depends(require_admin)):
    logs = (
        db.query(models.ActivityLog)
        .order_by(models.ActivityLog.created_at.desc())
        .limit(limit)
        .all()
    )
    return [
        {"id": l.id, "user_id": l.user_id, "action": l.action, "created_at": l.created_at.isoformat()}
        for l in logs
    ]