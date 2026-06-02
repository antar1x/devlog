from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from logs.models import Goal, LogSession, Topic


class AccountViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )

    def test_register_page_opens(self):
        response = self.client.get(reverse('register'))

        self.assertEqual(response.status_code, 200)

    def test_register_creates_user(self):
        response = self.client.post(reverse('register'), {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'StrongPass123',
            'password2': 'StrongPass123',
        })

        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_login_page_opens(self):
        response = self.client.get(reverse('login'))

        self.assertEqual(response.status_code, 200)

    def test_profile_settings_requires_login(self):
        response = self.client.get(reverse('profile_settings'))

        self.assertEqual(response.status_code, 302)

    def test_profile_settings_opens_for_logged_user(self):
        self.client.login(username='testuser', password='testpass123')

        response = self.client.get(reverse('profile_settings'))

        self.assertEqual(response.status_code, 200)

    def test_profile_settings_updates_profile(self):
        self.client.login(username='testuser', password='testpass123')

        response = self.client.post(reverse('profile_settings'), {
            'bio': 'Updated bio',
            'is_public': 'on',
        })

        self.user.profile.refresh_from_db()

        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.user.profile.bio, 'Updated bio')
        self.assertTrue(self.user.profile.is_public)

    def test_public_profile_opens_when_profile_is_public(self):
        self.user.profile.is_public = True
        self.user.profile.save()

        response = self.client.get(reverse('public_profile', args=[self.user.username]))

        self.assertEqual(response.status_code, 200)

    def test_public_profile_returns_404_when_profile_is_private(self):
        self.user.profile.is_public = False
        self.user.profile.save()

        response = self.client.get(reverse('public_profile', args=[self.user.username]))

        self.assertEqual(response.status_code, 404)

    def test_profile_search_finds_public_user(self):
        self.user.profile.is_public = True
        self.user.profile.save()

        response = self.client.post(reverse('profiles'), {
            'username': self.user.username,
        })

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.user.username)

    def test_public_profile_shows_user_statistics(self):
        topic = Topic.objects.create(user=self.user, name='Django')
        LogSession.objects.create(
            user=self.user,
            topic=topic,
            date='2026-06-01',
            duration_minutes=90,
            difficulty=3,
            notes='CBV practice',
        )
        Goal.objects.create(
            user=self.user,
            topic=topic,
            title='Learn Django',
            target_hours=10,
            deadline='2026-06-30',
        )

        response = self.client.get(reverse('public_profile', args=[self.user.username]))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Django')
        self.assertContains(response, '90')
        self.assertContains(response, 'Learn Django')