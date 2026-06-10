from django.contrib.auth.models import User
from django.db import models


class Topic(models.Model):
    name = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class LogSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    date = models.DateField()
    duration_minutes = models.PositiveIntegerField()
    notes = models.TextField(blank=True)
    difficulty = models.IntegerField(choices=[(i, i) for i in range(1, 6)])

    def __str__(self):
        return f"{self.user.username} - {self.topic.name} - {self.date}"


class Goal(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    target_hours = models.PositiveIntegerField()
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    deadline = models.DateField()
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {self.title}"
