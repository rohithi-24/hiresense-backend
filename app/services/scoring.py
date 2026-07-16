def calculate_score(job_skills, candidate_skills):

    if len(job_skills) == 0:
        return 0

    matched = len(
        set(job_skills) & set(candidate_skills)
    )

    score = (matched / len(job_skills)) * 100

    return round(score, 2)