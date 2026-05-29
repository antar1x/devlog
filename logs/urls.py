from django.urls import path

from logs.views import TopicCreateView, TopicListView, LogSessionListView, LogSessionCreateView, LogSessionUpdateView, \
    LogSessionDeleteView, DashboardView, GoalListView, GoalCreateView, GoalUpdateView, GoalDeleteView

urlpatterns = [
    path('topics/', TopicListView.as_view(), name='topic_list'),
    path('topics/create/', TopicCreateView.as_view(), name='topic_create'),
    path('sessions/', LogSessionListView.as_view(), name='session_list'),
    path('sessions/create/', LogSessionCreateView.as_view(), name='session_create'),
    path('sessions/<int:pk>/edit/', LogSessionUpdateView.as_view(), name='session_edit'),
    path('sessions/<int:pk>/delete/', LogSessionDeleteView.as_view(), name='session_delete'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('goals/', GoalListView.as_view(), name='goal_list'),
    path('goals/create/', GoalCreateView.as_view(), name='goal_create'),
    path('goals/<int:pk>/edit/', GoalUpdateView.as_view(), name='goal_edit'),
    path('goals/<int:pk>/delete/', GoalDeleteView.as_view(), name='goal_delete'),
]