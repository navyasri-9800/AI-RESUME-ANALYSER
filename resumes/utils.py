def resume_structure_score(resume):

    score = 0

    if resume.full_name:
        score += 10

    if resume.email:
        score += 10

    if resume.phone:
        score += 10

    if resume.summary:
        score += 15

    if resume.skills:
        score += 15

    if resume.education:
        score += 15

    if resume.projects:
        score += 15

    if resume.experience:
        score += 10

    return score