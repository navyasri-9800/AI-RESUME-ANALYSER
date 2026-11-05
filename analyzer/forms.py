from django import forms
from .models import JobDescription


class JobDescriptionForm(forms.ModelForm):

    class Meta:

        model = JobDescription

        fields = [
            'title',
            'description'
        ]

        widgets = {

            'description': forms.Textarea(
                attrs={
                    'rows': 12,
                    'placeholder':
                    'Paste the complete job description here...'
                }
            )
        }