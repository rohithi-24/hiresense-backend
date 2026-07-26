import re

# Comprehensive list of technical skills to look for in resumes and job descriptions
SKILL_KEYWORDS = [
    "python", "javascript", "typescript", "react", "next.js", "tailwind", "tailwind css",
    "fastapi", "django", "node.js", "sql", "postgresql", "mysql", "docker", "git",
    "aws", "html", "html5", "css", "css3", "restful api", "sqlalchemy", "c++", "java"
]

def extract_skills(text: str) -> list:
    """
    Scans the given text for known technical skills and returns a list of unique matches.
    """
    if not text:
        return []
    
    text_lower = text.lower()
    found_skills = set()
    
    for skill in SKILL_KEYWORDS:
        pattern = r'\b' + re.escape(skill) + r'\b'
        if re.search(pattern, text_lower):
            found_skills.add(skill.lower())
            
    return list(found_skills)