from django import forms

from logs.models import Topic


class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ('name', )

        