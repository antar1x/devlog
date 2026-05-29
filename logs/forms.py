from django import forms
from django.http import request

from logs.models import Topic, LogSession, Goal


class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ('name', )

class LogSessionForm(forms.ModelForm):
    class Meta:
        model = LogSession
        fields = ('topic', 'date', 'duration_minutes', 'difficulty', 'notes')
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'notes': forms.Textarea(attrs={'rows': 4}),
        }

class GoalForm(forms.ModelForm):
    class Meta:
        model = Goal
        fields = ('title', 'target_hours', 'topic', 'deadline' )
        widgets = {
            'deadline': forms.DateInput(attrs={'type': 'date'}),
        }
