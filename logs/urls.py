from django.urls import path

from logs import views

urlpatterns = [
    path('topics/', views.topic_list, name='topic_list'),
    path('topics/create/', views.topic_create, name='topic_create'),
]
