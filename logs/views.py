from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View


from django.shortcuts import render

from logs.models import Topic


class TopicListView(LoginRequiredMixin, View):
    def get(self, request):
        topics = Topic.objects.filter(user=request.user)
        return render(request, )