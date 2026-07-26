from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.job import Job
from pydantic import BaseModel

router = APIRouter(prefix="/jobs", tags=["Jobs"])

class JobCreate(BaseModel):
    title: str
    description: str
    location: str
    job_type: str

class JobResponse(JobCreate):
    id: int

    class Config:
        from_attributes = True

@router.get("/", response_model=List[JobResponse])
def get_jobs(db: Session = Depends(get_db)):
    return db.query(Job).all()

@router.post("/", response_model=JobResponse, status_code=status.HTTP_201_CREATED)
def create_job(job: JobCreate, db: Session = Depends(get_db)):
    new_job = Job(**job.dict())
    db.add(new_job)
    db.commit()
    db.refresh(new_job)
    return new_job

@router.put("/{job_id}", response_model=JobResponse)
def update_job(job_id: int, job: JobCreate, db: Session = Depends(get_db)):
    db_job = db.query(Job).filter(Job.id == job_id).first()
    if not db_job:
        raise HTTPException(status_code=404, detail="Job not found")
    for key, value in job.dict().items():
        setattr(db_job, key, value)
    db.commit()
    db.refresh(db_job)
    return db_job

@router.delete("/{job_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_job(job_id: int, db: Session = Depends(get_db)):
    db_job = db.query(Job).filter(Job.id == job_id).first()
    if not db_job:
        raise HTTPException(status_code=404, detail="Job not found")
    db.delete(db_job)
    db.commit()
    return None