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


class PollView(generic.DetailView):
    model = Poll
    template_name = 'polls_app/poll.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_expired'] = timezone.now() >= Poll.objects.get(pk=self.kwargs.get('pk')).date_ended
        if self.object.answer_type == 'user_text':
            context['form'] = ChoiceForm()
        return context


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
    poll.passed_users.add(request.user)
    return redirect('polls_app:results', pk=pk)


def make_text_vote(request, pk):
    poll = get_object_or_404(Poll, pk=pk)
    form = ChoiceForm(data=request.POST)
    if form.is_valid():
        user_choice = form.save(commit=False)
        user_choice.question = poll
        user_choice.votes += 1
        user_choice.save()
        user_choice.passed_users.add(request.user)
    poll.passed_users.add(request.user)
    return redirect('polls_app:results', pk=pk)


class ResultsView(generic.DetailView):
    model = Poll
    template_name = "polls_app/results.html"


# serializers
class PollViewSet(viewsets.ModelViewSet):
    serializer_class = PollSerializer
    queryset = Poll.objects.all()


class ChoiceViewSet(viewsets.ModelViewSet):
    serializer_class = ChoiceSerializer
    queryset = Choice.objects.all()
