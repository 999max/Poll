from datetime import datetime

from django import forms
from django.forms import SelectDateWidget
from extra_views import InlineFormSet

from .models import Choice, Poll


class ChoiceForm(forms.ModelForm):
    class Meta:
        model = Choice
        fields = ['choice_text']
        labels = {'choice_text': 'Your answer'}


class ChoiceUserInline(InlineFormSet):
    model = Choice
    exclude = ('votes', 'passed_users')
    factory_kwargs = {'extra': 5}


class PollForm(forms.ModelForm):
    class Meta:
        model = Poll
        fields = ['title', 'question_text', 'date_ended', 'answer_type']
        widgets = {
            'date_ended': forms.DateTimeInput(format=('%Y-%m-%d %H:%M:%S'), attrs={'value': datetime.now()}),
        }

