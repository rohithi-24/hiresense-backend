import re

SKILLS_DATABASE = [
    "python", "java", "c++", "javascript", "typescript", "sql", "html", "css",
    "react", "next.js", "vue", "angular", "tailwind", "bootstrap",
    "fastapi", "django", "flask", "node.js", "express",
    "postgresql", "mysql", "mongodb", "sqlite",
    "aws", "azure", "gcp", "docker", "kubernetes", "git", "github",
    "pandas", "numpy", "matplotlib", "opencv", "pytorch", "tensorflow",
    "yolo", "scikit-learn", "nlp", "figma", "linux",
]

def extract_skills(text: str):
    text = text.lower()
    found_skills = []

    for skill in SKILLS_DATABASE:
        pattern = r"\b" + re.escape(skill) + r"\b"
        if re.search(pattern, text):
            found_skills.append(skill)

    return list(set(found_skills))