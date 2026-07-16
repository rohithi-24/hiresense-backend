from fastapi import APIRouter, Depends, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import List, Optional
import shutil, os, random
from app.database import get_db
from app import models, schemas
from app.utils import get_current_user

router = APIRouter()

UPLOAD_DIR = "uploads/resumes"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/apply")
async def apply(
    job_id: int = Form(...),
    cover_letter: str = Form(""),
    skills: str = Form(""),
    resume: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    # Save resume file
    resume_path = ""
    if resume:
        filename = f"{current_user.id}_{job_id}_{resume.filename}"
        path = os.path.join(UPLOAD_DIR, filename)
        with open(path, "wb") as f:
            shutil.copyfileobj(resume.file, f)
        resume_path = path

    # Mock AI score (replace with real AI later)
    ai_score = round(random.uniform(55, 97), 1)

    app = models.Application(
        user_id=current_user.id,
        job_id=job_id,
        cover_letter=cover_letter,
        skills=skills,
        resume_path=resume_path,
        ai_score=ai_score,
        status="Under Review",
    )
    db.add(app); db.commit()
    return {"message": "Application submitted", "ai_score": ai_score}


@router.get("/my", response_model=List[schemas.ApplicationOut])
def my_applications(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    apps = db.query(models.Application).filter(models.Application.user_id == current_user.id).all()
    result = []
    for a in apps:
        job = db.query(models.Job).filter(models.Job.id == a.job_id).first()
        result.append(schemas.ApplicationOut(
            id=a.id,
            job_title=job.title if job else "Unknown",
            company=job.company if job else "Unknown",
            status=a.status,
            ai_score=a.ai_score,
            created_at=a.created_at,
        ))
    return result