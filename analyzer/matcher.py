from resumes.nlp import extract_skills


def calculate_match(resume_text, job_text):

    resume_skills = set(
        extract_skills(resume_text)
    )

    job_skills = set(
        extract_skills(job_text)
    )

    if not job_skills:

        return {
            'score': 0,
            'matched': [],
            'missing': []
        }

    matched = resume_skills.intersection(
        job_skills
    )

    missing = job_skills.difference(
        resume_skills
    )

    score = (
        len(matched) /
        len(job_skills)
    ) * 100

    return {
        'score': round(score, 2),
        'matched': sorted(matched),
        'missing': sorted(missing)
    }