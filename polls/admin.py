"""
Admin configuration for the Polls App.
"""


from django.contrib import admin
from .models import Topic, Question, Choice
# Register your models here.
admin.site.register(Topic)
admin.site.register(Question)
admin.site.register(Choice)
