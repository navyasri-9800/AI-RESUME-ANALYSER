from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from resumes.models import Resume

from .models import JobDescription, Analysis
from .forms import JobDescriptionForm
from .matcher import calculate_match

# Create your views here.
@login_required
def analyze_resume(request, resume_id):

    resume = get_object_or_404(
        Resume,
        id=resume_id,
        user=request.user
    )

    if request.method == 'POST':

        form = JobDescriptionForm(
            request.POST
        )

        if form.is_valid():

            job = form.save(
                commit=False
            )

            job.user = request.user

            job.save()

            resume_text = resume.extracted_text
            if not resume_text or not resume_text.strip():
                resume_text = " ".join([
                    resume.summary or "",
                    resume.skills or "",
                    resume.experience or "",
                    resume.projects or "",
                    resume.education or "",
                    resume.certifications or "",
                ])

            result = calculate_match(
                resume_text,
                job.description
            )

            recommendations = []

            if result['missing']:

                recommendations.append(
                    "Review the missing skills and add them only if you genuinely have those skills."
                )

            if not resume.summary:

                recommendations.append(
                    "Add a professional summary."
                )

            if not resume.projects:

                recommendations.append(
                    "Add relevant projects."
                )

            analysis = Analysis.objects.create(

                resume=resume,

                job_description=job,

                ats_score=result['score'],

                matched_skills=", ".join(
                    result['matched']
                ),

                missing_skills=", ".join(
                    result['missing']
                ),

                recommendations="\n".join(
                    recommendations
                )
            )

            return redirect(
                'analysis_result',
                analysis_id=analysis.id
            )

    else:

        form = JobDescriptionForm()

    return render(
        request,
        'job_description.html',
        {
            'resume': resume,
            'form': form
        }
    )


@login_required
def analysis_result(
    request,
    analysis_id
):

    analysis = get_object_or_404(
        Analysis,
        id=analysis_id,
        resume__user=request.user
    )

    matched_skills = [
        skill.strip()
        for skill in analysis.matched_skills.split(',')
        if skill.strip()
    ]
    missing_skills = [
        skill.strip()
        for skill in analysis.missing_skills.split(',')
        if skill.strip()
    ]

    return render(
        request,
        'analysis.html',
        {
            'analysis': analysis,
            'matched_skills': matched_skills,
            'missing_skills' : missing_skills,
        }
    )


@login_required
def history(request):
    analyses = Analysis.objects.filter(resume__user=request.user).select_related('resume', 'job_description').order_by('-created_at')
    resumes = Resume.objects.filter(user=request.user).order_by('-created_at')

    return render(
        request,
        'history.html',
        {
            'analyses': analyses,
            'resumes': resumes,
        }
    )