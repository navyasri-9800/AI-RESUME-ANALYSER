from django import forms
from .models import Resume


class ResumeForm(forms.ModelForm):

    class Meta:

        model = Resume

        fields = [
            'title',
            'full_name',
            'email',
            'phone',
            'location',
            'linkedin',
            'github',
            'summary',
            'skills',
            'experience',
            'education',
            'projects',
            'certifications',
        ]

        widgets = {

            'summary': forms.Textarea(
                attrs={
                    'rows': 5
                }
            ),

            'skills': forms.Textarea(
                attrs={
                    'rows': 4,
                    'placeholder':
                    'Python, Django, SQL, React...'
                }
            ),

            'experience': forms.Textarea(
                attrs={
                    'rows': 6
                }
            ),

            'education': forms.Textarea(
                attrs={
                    'rows': 5
                }
            ),

            'projects': forms.Textarea(
                attrs={
                    'rows': 6
                }
            ),

            'certifications': forms.Textarea(
                attrs={
                    'rows': 4
                }
            ),
        }