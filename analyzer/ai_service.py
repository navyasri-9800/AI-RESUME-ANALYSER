def improve_summary(summary, job_description):

    if not summary:

        return (
            "Add a concise professional summary "
            "highlighting your relevant skills, "
            "experience, and career focus."
        )

    return (
        "Consider tailoring your professional "
        "summary to the skills and responsibilities "
        "mentioned in the target job description."
    )


def improve_project(description):

    if not description:

        return (
            "Add 2-4 achievement-focused bullet points "
            "describing your actual contribution."
        )

    return (
        "Rewrite the project using concise action verbs, "
        "technologies used, your contribution, and "
        "measurable results where truthful."
    )