from django import forms

from logs.models import Topic, LogSession


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
