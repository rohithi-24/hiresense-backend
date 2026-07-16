def keyword_match(job_skills, candidate_skills):

    matched = list(
        set(job_skills) & set(candidate_skills)
    )

    return {
        "matched_keywords": matched,
        "match_count": len(matched)
    }