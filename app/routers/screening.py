import os

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app import models

from app.services.resume_parser import extract_text_from_pdf
from app.services.skill_extractor import extract_skills
from app.services.matcher import keyword_match
from app.services.scoring import calculate_score

router = APIRouter(
    prefix="/api/screening",
    tags=["AI Screening"]
)


@router.get("/test")
def test_screening():

    resume_text = """
    Python FastAPI PostgreSQL Docker
    """

    candidate_skills = extract_skills(resume_text)

    job_skills = [
        "python",
        "fastapi",
        "docker",
        "aws"
    ]

    matching = keyword_match(
        job_skills,
        candidate_skills
    )

    score = calculate_score(
        job_skills,
        candidate_skills
    )

    return {
        "candidate_skills": candidate_skills,
        "job_skills": job_skills,
        "matched_keywords": matching["matched_keywords"],
        "score": score
    }


@router.get("/applicant/{applicant_id}/job/{job_id}")
def screen_candidate(
    applicant_id: int,
    job_id: int,
    db: Session = Depends(get_db)
):

    applicant = (
        db.query(models.Applicant)
        .filter(models.Applicant.id == applicant_id)
        .first()
    )

    if not applicant:
        raise HTTPException(
            status_code=404,
            detail="Applicant not found"
        )

    job = (
        db.query(models.Job)
        .filter(models.Job.id == job_id)
        .first()
    )

    if not job:
        raise HTTPException(
            status_code=404,
            detail="Job not found"
        )

    if not applicant.resume_url:
        raise HTTPException(
            status_code=400,
            detail="Resume not uploaded"
        )

    resume_path = applicant.resume_url

    if not os.path.exists(resume_path):
        raise HTTPException(
            status_code=404,
            detail=f"Resume file not found: {resume_path}"
        )

    resume_text = extract_text_from_pdf(
        resume_path
    )

    candidate_skills = extract_skills(
        resume_text
    )

    job_skills = []

    if job.skills:
        job_skills = [
            skill.strip().lower()
            for skill in job.skills.split(",")
        ]

    matching = keyword_match(
        job_skills,
        candidate_skills
    )

    score = calculate_score(
        job_skills,
        candidate_skills
    )

    return {
        "applicant_id": applicant.id,
        "applicant_name": applicant.full_name,
        "job_id": job.id,
        "job_title": job.title,
        "candidate_skills": candidate_skills,
        "job_skills": job_skills,
        "matched_keywords": matching["matched_keywords"],
        "score": score
    }