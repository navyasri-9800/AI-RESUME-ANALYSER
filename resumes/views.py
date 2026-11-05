from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from .models import Resume
from .forms import ResumeForm
from .parser import extract_text

# Create your views here.

@login_required
def create_resume(request):

    if request.method == 'POST':

        form = ResumeForm(request.POST)

        if form.is_valid():

            resume = form.save(
                commit=False
            )

            resume.user = request.user

            resume.save()

            return redirect(
                'resume_preview',
                resume_id=resume.id
            )

    else:

        form = ResumeForm()

    return render(
        request,
        'resume_builder.html',
        {'form': form}
    )


@login_required
def resume_preview(request, resume_id):

    resume = get_object_or_404(
        Resume,
        id=resume_id,
        user=request.user
    )

    return render(
        request,
        'resume_preview.html',
        {
            'resume': resume
        }
    )


@login_required
def upload_resume(request):

    if request.method == 'POST':

        file = request.FILES.get(
            'resume_file'
        )

        if not file:

            return render(
                request,
                'upload.html',
                {
                    'error':
                    'Please select a resume.'
                }
            )

        allowed_types = [
            'application/pdf',
            'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
        ]

        if file.content_type not in allowed_types:

            return render(
                request,
                'upload.html',
                {
                    'error':
                    'Only PDF and DOCX files are allowed.'
                }
            )

        resume = Resume.objects.create(

            user=request.user,

            title=file.name,

            full_name=request.user.username,

            email=request.user.email,

            phone='',

            resume_file=file
        )

        resume.extracted_text = extract_text(
            resume.resume_file.path
        )

        resume.save()

        return redirect(
            'resume_analysis',
            resume_id=resume.id
        )

    return render(
        request,
        'upload.html'
    )