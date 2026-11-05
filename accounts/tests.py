from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User


class AccountsTests(TestCase):

    def setUp(self):
        self.username = 'testuser'
        self.password = 'TestPass123!'
        self.user = User.objects.create_user(
            username=self.username,
            email='test@example.com',
            password=self.password
        )

    def test_home_view(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_login_view(self):
        response = self.client.post(reverse('login'), {
            'username': self.username,
            'password': self.password,
        })
        self.assertRedirects(response, reverse('dashboard'))

    def test_logout_view(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(reverse('logout'))
        self.assertRedirects(response, reverse('login'))

    def test_dashboard_login_required(self):
        response = self.client.get(reverse('dashboard'))
        self.assertNotEqual(response.status_code, 200)
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)

    def test_profile_view(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)

        response = self.client.post(reverse('profile'), {
            'email': 'updated@example.com',
            'first_name': 'Jane',
            'last_name': 'Doe',
        })
        self.assertEqual(response.status_code, 200)
        self.user.refresh_from_db()
        self.assertEqual(self.user.email, 'updated@example.com')
        self.assertEqual(self.user.first_name, 'Jane')
