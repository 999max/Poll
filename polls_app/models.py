from django.db import models
from django.contrib.auth.models import User


CHOICE_TYPES = (
    ('1', 'one answer'),
    ('N', 'N answers'),
    ('user_text', 'text_answers')
)


class Poll(models.Model):
    title = models.CharField(max_length=150, verbose_name='Poll title')
    question_text = models.TextField(verbose_name='Poll question text')
    date_added = models.DateTimeField(auto_now_add=True, verbose_name="Poll's start date")
    date_ended = models.DateTimeField(verbose_name="Poll's end date")
    answer_type = models.CharField(max_length=150, choices=CHOICE_TYPES, default='1')
    passed_users = models.ManyToManyField(User, blank=True)

    def __str__(self):
        return f"{self.question_text[:50]}"


class Choice(models.Model):
    question = models.ForeignKey(Poll, on_delete=models.PROTECT)
    choice_text = models.CharField(max_length=200, )
    votes = models.IntegerField(default=0)
    passed_users = models.ManyToManyField(User, blank=True)

    def __str__(self):
        return self.choice_text
