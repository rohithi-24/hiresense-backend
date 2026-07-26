from app.database import SessionLocal
from app import models
from datetime import datetime

db = SessionLocal()

jobs = [
    models.Job(title="Frontend Engineer", company="Gaint Clout", location="Hyderabad", type="Full-time", salary="₹6-10 LPA", description="Build beautiful UIs with React and Next.js."),
    models.Job(title="AI/ML Engineer", company="TechCorp", location="Remote", type="Internship", salary="₹25k/mo", description="Work on cutting-edge AI models and pipelines."),
    models.Job(title="Data Analyst", company="StartupXYZ", location="Hyderabad", type="Contract", salary="₹4-7 LPA", description="Analyze data and build dashboards."),
    models.Job(title="React Developer", company="InnoSoft", location="Hyderabad", type="Full-time", salary="₹7-12 LPA", description="Build and maintain React applications."),
]

for job in jobs:
    db.add(job)

db.commit()
db.close()
print("Jobs seeded successfully!")