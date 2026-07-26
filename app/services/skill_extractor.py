import re

def extract_skills(text: str) -> list[str]:
    """
    Extracts relevant technical and professional skills from the given text 
    using keyword matching and pattern extraction.
    """
    if not text:
        return []

    # Common skills dictionary/list to match against the text
    common_skills = [
        "python", "java", "javascript", "typescript", "c++", "c#", "go", "rust", 
        "ruby", "php", "swift", "kotlin", "sql", "nosql", "mongodb", "postgresql", 
        "mysql", "fastapi", "flask", "django", "react", "vue", "angular", "node.js", 
        "docker", "kubernetes", "aws", "gcp", "azure", "git", "ci/cd", "machine learning", 
        "data science", "nlp", "pandas", "numpy", "pytorch", "tensorflow", "html", "css"
    ]

    found_skills = set()
    lower_text = text.lower()

    # Search for standard keywords
    for skill in common_skills:
        # Use word boundary regex to avoid partial matches
        pattern = r'\b' + re.escape(skill) + r'\b'
        if re.search(pattern, lower_text):
            found_skills.add(skill.title())

    return list(found_skills)