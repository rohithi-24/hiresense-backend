import re

def extract_skills_from_description(job_description_text):
    """Automatically extracts required skills from the job description text."""
    if not job_description_text:
        return []
    common_skills = [
        "React", "Next.js", "TypeScript", "Node.js", "GraphQL", 
        "Tailwind", "Python", "FastAPI", "JavaScript", "Docker", "AWS", "SQL", "Django"
    ]
    return [
        skill for skill in common_skills 
        if re.search(r'\b' + re.escape(skill) + r'\b', job_description_text, re.IGNORECASE)
    ]

def calculate_resume_score(job_skills, candidate_skills):
    """Calculates a precise percentage score based on skill overlap."""
    if not job_skills:
        return 0.0
    job_skills_lower = {s.lower() for s in job_skills}
    candidate_skills_lower = {s.lower() for s in candidate_skills}
    matches = job_skills_lower.intersection(candidate_skills_lower)
    return round((len(matches) / len(job_skills_lower)) * 100, 2)