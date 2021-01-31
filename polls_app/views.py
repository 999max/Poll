from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.views import generic
from rest_framework import viewsets
from .models import Poll, Choice
from .forms import ChoiceForm
from .serializers import PollSerializer, ChoiceSerializer


def index(request):
    return render(request, 'polls_app/index.html')


class PollsView(generic.ListView):
    template_name = "polls_app/polls.html"
    context_object_name = "polls"

    def get_queryset(self):
        return Poll.objects.filter(date_ended__gte=timezone.now())


def poll(request, pk):
    poll = get_object_or_404(Poll, pk=pk)
    choices = poll.choice_set.all()
    answer_type = poll.answer_type  # FIXME?
    time_expired = timezone.now() > poll.date_ended
    context = {'poll': poll, 'choices': choices,
               'time_expired': time_expired, 'answer_type': answer_type}
    return render(request, 'polls_app/poll.html', context)


def text_poll(request, pk):
    poll = get_object_or_404(Poll, pk=pk)
    time_expired = timezone.now() > poll.date_ended
    form = ChoiceForm()
    context = {'poll': poll, 'time_expired': time_expired, 'form': form}
    return render(request, 'polls_app/text_poll.html', context)


class CompletedPollsView(generic.ListView):
    template_name = "polls_app/completed.html"
    context_object_name = "polls"

    def get_queryset(self):
        return Poll.objects.filter(date_ended__lte=timezone.now())


def make_vote(request, pk):
    poll = get_object_or_404(Poll, pk=pk)
    request_data = request.POST
    for key, choice_id in request_data.items():
        if 'choice' in key:
            selected_choice = poll.choice_set.get(pk=choice_id)
            selected_choice.votes += 1
            selected_choice.passed_users.add(request.user)
            selected_choice.save()

    return redirect('polls_app:results', pk=pk)


def make_text_vote(request, pk):
    poll = get_object_or_404(Poll, pk=pk)
    form = ChoiceForm(data=request.POST)
    if form.is_valid():
        user_choice = form.save(commit=False)
        user_choice.question = poll
        user_choice.votes += 1
        # user_choice.passed_users.add(request.user)  # FIXME
        user_choice.save()
    return redirect('polls_app:results', pk=pk)


def results(request, pk):
    poll = get_object_or_404(Poll, pk=pk)
    context = {'poll': poll}
    return render(request, 'polls_app/results.html', context)


##  serializers
class PollViewSet(viewsets.ModelViewSet):
    serializer_class = PollSerializer
    queryset = Poll.objects.all()


class ChoiceViewSet(viewsets.ModelViewSet):
    serializer_class = ChoiceSerializer
    queryset = Choice.objects.all()
