from django.db import models
from django.contrib.auth.models import User
from resumes.models import Resume


class JobDescription(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    title = models.CharField(
        max_length=200
    )

    description = models.TextField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return self.title


class Analysis(models.Model):

    resume = models.ForeignKey(
        Resume,
        on_delete=models.CASCADE
    )

    job_description = models.ForeignKey(
        JobDescription,
        on_delete=models.CASCADE
    )

    ats_score = models.FloatField(
        default=0
    )

    matched_skills = models.TextField(
        blank=True
    )

    missing_skills = models.TextField(
        blank=True
    )

    recommendations = models.TextField(
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return f"{self.resume.title} - {self.ats_score}"


