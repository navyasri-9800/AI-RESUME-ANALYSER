from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from resumes.models import Resume
from .matcher import calculate_match
from .models import Analysis


class AnalyzerTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='analyzeruser',
            password='Password123!'
        )
        self.resume = Resume.objects.create(
            user=self.user,
            title='Python Dev Resume',
            full_name='Alice Smith',
            email='alice@example.com',
            phone='9876543210',
            skills='Python, Django, PostgreSQL, Git'
        )

    def test_calculate_match(self):
        resume_text = "Experienced Python developer working with Django and Docker."
        job_text = "Looking for a Python and Django expert with Docker and AWS experience."
        match = calculate_match(resume_text, job_text)
        self.assertIn('python', match['matched'])
        self.assertIn('django', match['matched'])
        self.assertIn('docker', match['matched'])
        self.assertIn('aws', match['missing'])
        self.assertGreater(match['score'], 0)

    def test_analyze_resume_view(self):
        self.client.login(username='analyzeruser', password='Password123!')
        response = self.client.post(
            reverse('resume_analysis', kwargs={'resume_id': self.resume.id}),
            {
                'title': 'Python Backend Engineer',
                'description': 'Requires Python, Django, PostgreSQL, and AWS.'
            }
        )
        self.assertEqual(Analysis.objects.count(), 1)
        analysis = Analysis.objects.first()
        self.assertRedirects(response, reverse('analysis_result', kwargs={'analysis_id': analysis.id}))

    def test_history_view(self):
        self.client.login(username='analyzeruser', password='Password123!')
        response = self.client.get(reverse('history'))
        self.assertEqual(response.status_code, 200)
