from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView

from logs.forms import TopicForm
from logs.models import Topic


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
