SKILLS_DATABASE = [
    "python",
    "java",
    "c++",
    "sql",
    "postgresql",
    "fastapi",
    "django",
    "flask",
    "docker",
    "aws",
    "javascript",
    "react"
]

def extract_skills(text: str):
    text = text.lower()

    found_skills = []

    for skill in SKILLS_DATABASE:
        if skill in text:
            found_skills.append(skill)

    return list(set(found_skills))