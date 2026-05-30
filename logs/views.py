from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView, DeleteView, TemplateView

from logs.forms import TopicForm, LogSessionForm, GoalForm
from logs.models import Topic, LogSession, Goal


class TopicListView(LoginRequiredMixin, ListView):
    model = Topic
    template_name = 'logs/topic_list.html'
    context_object_name = 'topics'

    def get_queryset(self):
        return Topic.objects.filter(user=self.request.user)


class TopicCreateView(LoginRequiredMixin, CreateView):
    model = Topic
    form_class = TopicForm
    template_name = 'logs/topic_form.html'
    success_url = reverse_lazy('topic_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class LogSessionListView(LoginRequiredMixin, ListView):
    model = LogSession
    template_name = 'logs/session_list.html'
    context_object_name = 'sessions'

    def get_queryset(self):
        return LogSession.objects.filter(user=self.request.user).select_related('topic')


class LogSessionCreateView(LoginRequiredMixin, CreateView):
    model = LogSession
    form_class = LogSessionForm
    template_name = 'logs/session_form.html'
    success_url = reverse_lazy('session_list')

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['topic'].queryset = Topic.objects.filter(user=self.request.user)
        return form

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class LogSessionUpdateView(LoginRequiredMixin, UpdateView):
    model = LogSession
    form_class = LogSessionForm
    template_name = 'logs/session_form.html'
    success_url = reverse_lazy('session_list')

    def get_queryset(self):
        return LogSession.objects.filter(user=self.request.user)

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['topic'].queryset = Topic.objects.filter(user=self.request.user)
        return form

class LogSessionDeleteView(LoginRequiredMixin, DeleteView):
    model = LogSession
    success_url = reverse_lazy('session_list')
    template_name = 'logs/session_confirm_delete.html'

    def get_queryset(self):
        return LogSession.objects.filter(user=self.request.user)

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'logs/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        sessions = LogSession.objects.filter(user=self.request.user)

        total_sessions = sessions.count()
        total_minutes = sessions.aggregate(
            total=Sum('duration_minutes')
        )['total'] or 0

        total_hours = total_minutes / 60

        total_topics = Topic.objects.filter(
            user=self.request.user
        ).count()

        last_5_sessions = sessions.select_related('topic').order_by('-date')[:5]

        statistic = sessions.values('topic__name').annotate(
            total_minutes=Sum('duration_minutes')
        ).order_by('-total_minutes')

        context['total_sessions'] = total_sessions
        context['total_minutes'] = total_minutes
        context['total_hours'] = total_hours
        context['total_topics'] = total_topics
        context['last_5_sessions'] = last_5_sessions
        context['statistic'] = statistic

        return context

class GoalListView(LoginRequiredMixin, ListView):
    model = Goal
    template_name = 'logs/goal_list.html'
    context_object_name = 'goals'
    def get_queryset(self):
        goals = Goal.objects.filter(user=self.request.user).select_related('topic')

        for goal in goals:
            total_minutes = LogSession.objects.filter(
                user=self.request.user,
                topic=goal.topic
            ).aggregate(total=Sum('duration_minutes'))['total'] or 0

            goal.current_minutes = total_minutes
            goal.target_minutes = goal.target_hours * 60
            goal.progress_percent = min(100,
                                        round(total_minutes / goal.target_minutes * 100)) if goal.target_minutes else 0
            goal.is_completed_now = total_minutes >= goal.target_minutes

        return goals



class GoalCreateView(LoginRequiredMixin, CreateView):
    model = Goal
    form_class = GoalForm
    template_name = 'logs/goal_form.html'
    success_url = reverse_lazy('goal_list')

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['topic'].queryset = Topic.objects.filter(user=self.request.user)
        return form

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class GoalUpdateView(LoginRequiredMixin, UpdateView):
    model = Goal
    form_class = GoalForm
    template_name = 'logs/goal_form.html'
    success_url = reverse_lazy('goal_list')

    def get_queryset(self):
        return Goal.objects.filter(user=self.request.user)

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['topic'].queryset = Topic.objects.filter(user=self.request.user)
        return form


class GoalDeleteView(LoginRequiredMixin, DeleteView):
    model = Goal
    success_url = reverse_lazy('goal_list')
    template_name = 'logs/goal_confirm_delete.html'
    def get_queryset(self):
        return Goal.objects.filter(user=self.request.user)
