from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from logs.models import Goal, LogSession, Topic


class LogsViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='user1',
            password='testpass123'
        )
        self.other_user = User.objects.create_user(
            username='user2',
            password='testpass123'
        )

        self.topic = Topic.objects.create(
            user=self.user,
            name='Django'
        )
        self.other_topic = Topic.objects.create(
            user=self.other_user,
            name='React'
        )

        self.session = LogSession.objects.create(
            user=self.user,
            topic=self.topic,
            date='2026-06-01',
            duration_minutes=120,
            difficulty=3,
            notes='Django CBV',
        )
        self.other_session = LogSession.objects.create(
            user=self.other_user,
            topic=self.other_topic,
            date='2026-06-01',
            duration_minutes=60,
            difficulty=2,
            notes='React basics',
        )

        self.goal = Goal.objects.create(
            user=self.user,
            topic=self.topic,
            title='Learn Django',
            target_hours=2,
            deadline='2026-06-30',
        )

    def test_topic_list_requires_login(self):
        response = self.client.get(reverse('topic_list'))

        self.assertEqual(response.status_code, 302)

    def test_topic_list_shows_only_current_user_topics(self):
        self.client.login(username='user1', password='testpass123')

        response = self.client.get(reverse('topic_list'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Django')
        self.assertNotContains(response, 'React')

    def test_topic_create_creates_topic_for_current_user(self):
        self.client.login(username='user1', password='testpass123')

        response = self.client.post(reverse('topic_create'), {
            'name': 'SQL',
        })

        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            Topic.objects.filter(user=self.user, name='SQL').exists()
        )

    def test_session_list_requires_login(self):
        response = self.client.get(reverse('session_list'))

        self.assertEqual(response.status_code, 302)

    def test_session_list_shows_only_current_user_sessions(self):
        self.client.login(username='user1', password='testpass123')

        response = self.client.get(reverse('session_list'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Django')
        self.assertNotContains(response, 'React')

    def test_session_create_creates_session_for_current_user(self):
        self.client.login(username='user1', password='testpass123')

        response = self.client.post(reverse('session_create'), {
            'topic': self.topic.pk,
            'date': '2026-06-02',
            'duration_minutes': 45,
            'difficulty': 4,
            'notes': 'Testing session create',
        })

        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            LogSession.objects.filter(
                user=self.user,
                topic=self.topic,
                duration_minutes=45,
            ).exists()
        )

    def test_session_create_topic_queryset_contains_only_current_user_topics(self):
        self.client.login(username='user1', password='testpass123')

        response = self.client.get(reverse('session_create'))
        form = response.context['form']

        self.assertIn(self.topic, form.fields['topic'].queryset)
        self.assertNotIn(self.other_topic, form.fields['topic'].queryset)

    def test_user_cannot_edit_other_user_session(self):
        self.client.login(username='user1', password='testpass123')

        response = self.client.get(
            reverse('session_edit', args=[self.other_session.pk])
        )

        self.assertEqual(response.status_code, 404)

    def test_user_can_delete_own_session(self):
        self.client.login(username='user1', password='testpass123')

        response = self.client.post(
            reverse('session_delete', args=[self.session.pk])
        )

        self.assertEqual(response.status_code, 302)
        self.assertFalse(
            LogSession.objects.filter(pk=self.session.pk).exists()
        )

    def test_user_cannot_delete_other_user_session(self):
        self.client.login(username='user1', password='testpass123')

        response = self.client.post(
            reverse('session_delete', args=[self.other_session.pk])
        )

        self.assertEqual(response.status_code, 404)

    def test_dashboard_requires_login(self):
        response = self.client.get(reverse('dashboard'))

        self.assertEqual(response.status_code, 302)

    def test_dashboard_shows_current_user_statistics(self):
        self.client.login(username='user1', password='testpass123')

        response = self.client.get(reverse('dashboard'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['total_sessions'], 1)
        self.assertEqual(response.context['total_minutes'], 120)
        self.assertEqual(response.context['total_topics'], 1)

    def test_goal_list_requires_login(self):
        response = self.client.get(reverse('goal_list'))

        self.assertEqual(response.status_code, 302)

    def test_goal_list_shows_progress_fields(self):
        self.client.login(username='user1', password='testpass123')

        response = self.client.get(reverse('goal_list'))
        goals = list(response.context['goals'])
        goal = goals[0]

        self.assertEqual(goal.current_minutes, 120)
        self.assertEqual(goal.target_minutes, 120)
        self.assertEqual(goal.progress_percent, 100)
        self.assertTrue(goal.is_completed_now)

    def test_goal_create_creates_goal_for_current_user(self):
        self.client.login(username='user1', password='testpass123')

        response = self.client.post(reverse('goal_create'), {
            'title': 'Learn ORM',
            'target_hours': 10,
            'topic': self.topic.pk,
            'deadline': '2026-07-01',
        })

        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            Goal.objects.filter(user=self.user, title='Learn ORM').exists()
        )

    def test_user_cannot_edit_other_user_goal(self):
        other_goal = Goal.objects.create(
            user=self.other_user,
            topic=self.other_topic,
            title='Learn React',
            target_hours=10,
            deadline='2026-07-01',
        )

        self.client.login(username='user1', password='testpass123')

        response = self.client.get(
            reverse('goal_edit', args=[other_goal.pk])
        )

        self.assertEqual(response.status_code, 404)

    def test_user_cannot_delete_other_user_goal(self):
        other_goal = Goal.objects.create(
            user=self.other_user,
            topic=self.other_topic,
            title='Learn React',
            target_hours=10,
            deadline='2026-07-01',
        )

        self.client.login(username='user1', password='testpass123')

        response = self.client.post(
            reverse('goal_delete', args=[other_goal.pk])
        )

        self.assertEqual(response.status_code, 404)