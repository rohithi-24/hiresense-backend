def keyword_match(job_skills, candidate_skills):
    if not job_skills:
        return {"matched_keywords": [], "match_count": 0, "score": 0}

    matched = list(set(job_skills) & set(candidate_skills))
    
    # Calculate a percentage score (0 to 100) based on how many job skills were found
    score = round((len(matched) / len(job_skills)) * 100)

    return {
        "matched_keywords": matched,
        "match_count": len(matched),
        "score": score
    }