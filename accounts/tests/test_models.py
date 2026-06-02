from django.contrib.auth.models import User
from django.test import TestCase


class ProfileModelTests(TestCase):
    def test_profile_created_automatically_after_user_creation(self):
        user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )

        self.assertTrue(hasattr(user, 'profile'))
        self.assertEqual(user.profile.user, user)

    def test_profile_is_public_by_default(self):
        user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )

        self.assertTrue(user.profile.is_public)

    def test_profile_str_returns_username(self):
        user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )

        self.assertEqual(str(user.profile), 'testuser')