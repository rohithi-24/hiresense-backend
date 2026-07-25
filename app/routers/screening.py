import os
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app import models

from app.services.resume_parser import extract_text_from_pdf
from app.services.skill_extractor import extract_skills
from app.services.matcher import keyword_match
from app.services.scoring import calculate_score

router = APIRouter()


@router.post("/applications/{application_id}/screen")
def screen_application(application_id: int, db: Session = Depends(get_db)):
    application = db.query(models.Application).filter(
        models.Application.id == application_id
    ).first()
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")

    job = db.query(models.Job).filter(models.Job.id == application.job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    if not application.resume_path:
        raise HTTPException(status_code=400, detail="No resume uploaded for this application")

    if not os.path.exists(application.resume_path):
        raise HTTPException(status_code=404, detail=f"Resume file not found: {application.resume_path}")

    resume_text = extract_text_from_pdf(application.resume_path)
    candidate_skills = extract_skills(resume_text)

    job_text = (job.description or "").lower()
    job_skills = extract_skills(job_text)

    matching = keyword_match(job_skills, candidate_skills)
    score = calculate_score(job_skills, candidate_skills)

    application.ai_score = score
    db.commit()
    db.refresh(application)

    return {
        "application_id": application.id,
        "job_title": job.title,
        "candidate_skills": candidate_skills,
        "job_skills": job_skills,
        "matched_keywords": matching["matched_keywords"],
        "score": score,
    }


@router.post("/applications/screen-all")
def screen_all_pending(db: Session = Depends(get_db)):
    applications = db.query(models.Application).filter(
        models.Application.resume_path.isnot(None),
        (models.Application.ai_score == 0) | (models.Application.ai_score.is_(None)),
    ).all()

    results = []
    for application in applications:
        if not application.resume_path or not os.path.exists(application.resume_path):
            continue
        job = db.query(models.Job).filter(models.Job.id == application.job_id).first()
        if not job:
            continue

        resume_text = extract_text_from_pdf(application.resume_path)
        candidate_skills = extract_skills(resume_text)
        job_skills = extract_skills((job.description or "").lower())
        score = calculate_score(job_skills, candidate_skills)

        application.ai_score = score
        results.append({"application_id": application.id, "score": score})

    db.commit()
    return {"screened_count": len(results), "results": results}