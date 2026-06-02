from django.contrib.auth.models import User
from django.test import TestCase

from logs.forms import GoalForm, LogSessionForm, TopicForm
from logs.models import Topic


class LogsFormTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.topic = Topic.objects.create(
            user=self.user,
            name='Django'
        )

    def test_topic_form_is_valid(self):
        form = TopicForm(data={
            'name': 'Python',
        })

        self.assertTrue(form.is_valid())

    def test_topic_form_is_invalid_without_name(self):
        form = TopicForm(data={})

        self.assertFalse(form.is_valid())

    def test_log_session_form_is_valid(self):
        form = LogSessionForm(data={
            'topic': self.topic.pk,
            'date': '2026-06-01',
            'duration_minutes': 90,
            'difficulty': 3,
            'notes': 'Worked on Django forms',
        })

        self.assertTrue(form.is_valid())

    def test_log_session_form_is_invalid_without_required_fields(self):
        form = LogSessionForm(data={})

        self.assertFalse(form.is_valid())

    def test_goal_form_is_valid(self):
        form = GoalForm(data={
            'title': 'Learn Django',
            'target_hours': 20,
            'topic': self.topic.pk,
            'deadline': '2026-06-30',
        })

        self.assertTrue(form.is_valid())

    def test_goal_form_is_invalid_without_required_fields(self):
        form = GoalForm(data={})

        self.assertFalse(form.is_valid())