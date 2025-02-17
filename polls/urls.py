"""
URL paths for the Polls App
"""

from django.urls import path
from . import views

app_name = "polls"

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("<int:pk>/topic/", views.topic_view, name="topic"),
    path("questions/", views.question_view, name="questions"),
    path("<int:pk>/", views.DetailView.as_view(), name="detail"),
    path("<int:pk>/results/", views.ResultsView.as_view(), name="results"),
    path("<int:question_id>/vote/", views.vote, name="vote"),
    path("add", views.add_question, name="add_question")
]
