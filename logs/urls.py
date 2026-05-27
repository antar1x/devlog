from django.urls import path

from logs.views import TopicCreateView, TopicListView

urlpatterns = [
    path('topics/', TopicListView.as_view(), name='topic_list'),
    path('topics/create/', TopicCreateView.as_view(), name='topic_create'),
]