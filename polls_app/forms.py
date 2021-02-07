from django import forms
from .models import Choice


class ChoiceForm(forms.ModelForm):
    class Meta:
        model = Choice
        fields = ['choice_text']
        labels = {'choice_text': 'Your answer'}
