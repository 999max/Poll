from rest_framework import serializers
from .models import Poll, Choice


class PollSerializer(serializers.ModelSerializer):
    # add user??
    class Meta:
        model = Poll
        fields = '__all__'


class ChoiceSerializer(serializers.ModelSerializer):
    question = PollSerializer  # like this!
    # add user??
    class Meta:
        model = Choice
        fields = '__all__'