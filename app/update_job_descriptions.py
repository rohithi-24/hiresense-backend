from app.database import SessionLocal
from app import models

db = SessionLocal()

updates = {
    "Frontend Engineer": (
        "We're looking for a Frontend Engineer skilled in React, TypeScript, CSS, "
        "and Git to build responsive, modern web interfaces."
    ),
    "AI/ML Engineer": (
        "We are looking for an AI/ML engineer skilled in Python, PyTorch, OpenCV, "
        "and Pandas to build computer vision pipelines."
    ),
    "Data Analyst": (
        "Seeking a Data Analyst proficient in Python, SQL, Pandas, and Matplotlib "
        "to analyze datasets and build reporting dashboards."
    ),
    "React Developer": (
        "Seeking a React Developer with strong JavaScript, React, Tailwind, and "
        "GitHub experience to build and maintain scalable web applications."
    ),
}

for title, new_description in updates.items():
    job = db.query(models.Job).filter(models.Job.title == title).first()
    if job:
        job.description = new_description
        print(f"Updated: {title}")
    else:
        print(f"Not found, skipped: {title}")

db.commit()
db.close()
print("Done.")