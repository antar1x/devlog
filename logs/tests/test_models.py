from django.contrib.auth.models import User
from django.test import TestCase

from logs.models import Goal, LogSession, Topic


class LogsModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.topic = Topic.objects.create(
            user=self.user,
            name='Django'
        )

    def test_topic_str_returns_name(self):
        self.assertEqual(str(self.topic), 'Django')

    def test_log_session_str_contains_user_topic_and_date(self):
        session = LogSession.objects.create(
            user=self.user,
            topic=self.topic,
            date='2026-06-01',
            duration_minutes=60,
            difficulty=3,
            notes='Models practice',
        )

        self.assertEqual(
            str(session),
            'testuser - Django - 2026-06-01'
        )

    def test_goal_str_contains_username_and_title(self):
        goal = Goal.objects.create(
            user=self.user,
            topic=self.topic,
            title='Learn Django',
            target_hours=20,
            deadline='2026-06-30',
        )

        self.assertEqual(str(goal), 'testuser - Learn Django')
