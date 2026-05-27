from django.contrib import admin

from logs.models import Topic, Goal, LogSession

admin.site.register(Topic)
admin.site.register(Goal)
admin.site.register(LogSession)
