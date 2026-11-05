from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Resume
from .nlp import extract_skills


class ResumesTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='resumeuser',
            password='Password123!'
        )

    def test_extract_skills_nlp(self):
        text = "Candidate has strong knowledge of Python, Django, C++, and Docker."
        skills = extract_skills(text)
        self.assertIn('python', skills)
        self.assertIn('django', skills)
        self.assertIn('c++', skills)
        self.assertIn('docker', skills)
        self.assertNotIn('c', skills)

    def test_create_resume(self):
        self.client.login(username='resumeuser', password='Password123!')
        response = self.client.post(reverse('create_resume'), {
            'title': 'Software Engineer Resume',
            'full_name': 'Jane Doe',
            'email': 'jane@example.com',
            'phone': '1234567890',
            'skills': 'Python, Django',
        })
        self.assertEqual(Resume.objects.count(), 1)
        resume = Resume.objects.first()
        self.assertRedirects(response, reverse('resume_preview', kwargs={'resume_id': resume.id}))
