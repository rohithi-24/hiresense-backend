from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app import models, schemas
from app.utils import get_current_user, require_role

router = APIRouter()


@router.get("/", response_model=List[schemas.JobOut])
def list_jobs(db: Session = Depends(get_db)):
    jobs = db.query(models.Job).all()
    result = []
    for j in jobs:
        count = db.query(models.Application).filter(models.Application.job_id == j.id).count()
        out = schemas.JobOut.model_validate(j)
        out.applicant_count = count
        result.append(out)
    return result


@router.post("/", response_model=schemas.JobOut)
def create_job(job: schemas.JobCreate, db: Session = Depends(get_db), _=Depends(require_role("admin"))):
    new_job = models.Job(**job.dict())
    db.add(new_job); db.commit(); db.refresh(new_job)
    return new_job


@router.delete("/{job_id}")
def delete_job(job_id: int, db: Session = Depends(get_db), _=Depends(require_role("admin"))):
    job = db.query(models.Job).filter(models.Job.id == job_id).first()
    if job: db.delete(job); db.commit()
    return {"ok": True}