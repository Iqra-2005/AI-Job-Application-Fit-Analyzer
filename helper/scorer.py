def calculate_match(resume_data, jd_data):
    resume_skills = set(map(str.lower, resume_data["skills"]))
    jd_skills = set(map(str.lower, jd_data["required_skills"]))

    matched_skills = resume_skills.intersection(jd_skills)
    missing_skills = jd_skills - resume_skills

    skill_score = (len(matched_skills) / max(len(jd_skills), 1)) * 100

    experience_gap = resume_data["experience_years"] - jd_data["min_experience"]

    if skill_score >= 75 and experience_gap >= 0:
        decision = "Apply"
    elif skill_score >= 50:
        decision = "Apply After Upskilling"
    else:
        decision = "Not Recommended"

    return {
        "skill_score": round(skill_score, 2),
        "matched_skills": list(matched_skills),
        "missing_skills": list(missing_skills),
        "experience_gap": experience_gap,
        "decision": decision
    }
