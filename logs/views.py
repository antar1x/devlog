from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView, DeleteView

from logs.forms import TopicForm, LogSessionForm
from logs.models import Topic, LogSession


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
