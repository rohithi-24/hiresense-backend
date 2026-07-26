from app.database import SessionLocal
from app import models

DEMO_JOBS = [
    {
        "title": "Frontend Engineer",
        "company": "Gaint Clout",
        "location": "Hyderabad",
        "type": "Full-time",
        "salary": "₹6-10 LPA",
        "description": "Build and maintain our customer-facing web applications using React and TypeScript.",
    },
    {
        "title": "AI/ML Engineer",
        "company": "TechCorp",
        "location": "Remote",
        "type": "Internship",
        "salary": "₹25k/mo",
        "description": "Work on resume-scoring and job-matching models alongside our AI team.",
    },
    {
        "title": "Data Analyst",
        "company": "StartupXYZ",
        "location": "Hyderabad",
        "type": "Contract",
        "salary": "₹4-7 LPA",
        "description": "Analyze hiring funnel data and build dashboards for recruiting insights.",
    },
    {
        "title": "React Developer",
        "company": "InnoSoft",
        "location": "Hyderabad",
        "type": "Full-time",
        "salary": "₹7-12 LPA",
        "description": "Develop and ship new features for our applicant-facing product.",
    },
]


def seed_demo_jobs():
    db = SessionLocal()
    try:
        existing_titles = {j.title for j in db.query(models.Job).all()}
        for job_data in DEMO_JOBS:
            if job_data["title"] in existing_titles:
                continue
            db.add(models.Job(**job_data))
        db.commit()
    finally:
        db.close()