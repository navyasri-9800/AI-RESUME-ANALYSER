from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Resume(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    title = models.CharField(
        max_length=200
    )

    full_name = models.CharField(
        max_length=200
    )

    email = models.EmailField()

    phone = models.CharField(
        max_length=20
    )

    location = models.CharField(
        max_length=200,
        blank=True
    )

    linkedin = models.URLField(
        blank=True
    )

    github = models.URLField(
        blank=True
    )

    summary = models.TextField(
        blank=True
    )

    skills = models.TextField(
        blank=True
    )

    experience = models.TextField(
        blank=True
    )

    education = models.TextField(
        blank=True
    )

    projects = models.TextField(
        blank=True
    )

    certifications = models.TextField(
        blank=True
    )

    resume_file = models.FileField(
        upload_to='resumes/',
        blank=True,
        null=True
    )

    extracted_text = models.TextField(
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return self.title