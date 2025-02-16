"""
Model definitions for the Polls App
"""


import datetime
from django.db import models
from django.utils import timezone


class Topic(models.Model):
    """Topics are categories to help sort questions."""
    topic_name = models.CharField(max_length=200)
    pub_date = models.DateTimeField("date published")

    def __str__(self):
        return str(self.topic_name)


class Question(models.Model):
    """Questions are what users can vote on."""
    topic = models.ManyToManyField(Topic)
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField("date published")

    def __str__(self):
        return str(self.question_text)

    def was_published_recently(self):
        """function that returns true or false"""
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now


class Choice(models.Model):
    """Choices are the possible answers to vote on."""
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return str(self.choice_text)
