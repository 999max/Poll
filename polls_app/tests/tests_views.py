from django.test import TestCase, Client
from django.utils import timezone

from polls_app.models import Poll, Choice
from polls_app.views import make_vote, make_text_vote
from django.urls import reverse



class IndexTestView(TestCase):

    def test_index_view_exist(self):
        response = self.client.get('')
        self.assertEqual(response.status_code, 200)

    def test_index_view_get_by_name(self):
        response = self.client.get(reverse('polls_app:index'))
        self.assertEqual(response.status_code, 200)


class PollsTestView(TestCase):
    @classmethod
    def setUpTestData(cls):
        Poll.objects.create(title=f"poll_zero", question_text=f"question poll_zero",
                            date_ended=timezone.now(),
                            answer_type='1')
        for i in range(3):
            Poll.objects.create(title=f"poll_{i}", question_text=f"question poll{i}",
                                date_ended=timezone.now() + timezone.timedelta(seconds=i + 10),
                                answer_type='1')

    def test_polls_view_exist(self):
        response = self.client.get('/polls/')
        self.assertEqual(response.template_name[0], 'polls_app/polls.html')
        self.assertEqual(response.status_code, 200)

    def test_polls_view_get_by_name(self):
        response = self.client.get(reverse('polls_app:polls'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'polls_app/polls.html')

    def test_polls_view_context(self):
        response = self.client.get('/polls/')

        self.assertEqual(len(response.context['object_list']), 3)
        self.assertEqual(response.context['object_list'], response.context['polls'])

        self.assertEqual(response.context['object_list'][0].id, 2)
        self.assertEqual(response.context['object_list'][1].id, 3)
        self.assertEqual(response.context['object_list'][2].id, 4)

        self.assertEqual(response.context['object_list'][0].title, 'poll_0')
        self.assertEqual(response.context['object_list'][1].title, 'poll_1')
        self.assertEqual(response.context['object_list'][2].title, 'poll_2')

        self.assertEqual(response.context['object_list'][0].question_text, 'question poll0')
        self.assertEqual(response.context['object_list'][1].question_text, 'question poll1')
        self.assertEqual(response.context['object_list'][1].question_text, 'question poll1')

    def test_polls_view_contains_correct_html(self):
        response = self.client.get('/polls/')
        self.assertContains(response, 'All Polls')
        for i in range(3):
            self.assertContains(response, f"poll_{i}")

    def test_polls_view_does_not_contains_incorrect_html(self):
        response = self.client.get('/polls/')
        self.assertNotContains(response, 'Results')
        self.assertNotContains(response, 'poll_zero')


class PollTestView(TestCase):
    def setUp(self):
        self.poll_1 = Poll.objects.create(title="poll_zero", question_text="question poll_zero",
                                          date_ended=timezone.now(),
                                          answer_type='1')
        self.poll_2 = Poll.objects.create(title="poll_2", question_text="question poll_2",
                                          date_ended=timezone.now() + timezone.timedelta(seconds=10),
                                          answer_type='1')
        self.choice_1_1 = Choice.objects.create(question=self.poll_1, choice_text="choice 11")
        self.choice_1_2 = Choice.objects.create(question=self.poll_1, choice_text="choice 12")
        self.choice_2_1 = Choice.objects.create(question=self.poll_2, choice_text="choice 21")
        self.choice_2_2 = Choice.objects.create(question=self.poll_2, choice_text="choice 22")

    def test_poll_view_exists(self):
        for i in range(1, 3):
            response = self.client.get(f"/polls/poll/{i}/")
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response, 'polls_app/poll.html')

    def test_poll_view_get_by_name(self):
        response = self.client.get(reverse('polls_app:poll', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 200)

    def test_poll_view_does_not_exist(self):
        for i in range(3, 10):
            response = self.client.get(f"/polls/poll/{i}/")
            self.assertNotEqual(response.status_code, 200)

    def test_poll_is_closed_for_inactive_poll(self):
        response = self.client.get(reverse('polls_app:poll', kwargs={'pk': 1}))
        self.assertContains(response, 'Voting was closed at')
        self.assertNotContains(response, 'Make your answer')

    def test_poll_is_not_closed_for_active_poll(self):
        response = self.client.get(reverse('polls_app:poll', kwargs={'pk': 2}))
        self.assertNotContains(response, 'Voting was closed at')
        self.assertContains(response, 'Make your answer')

    def test_choices_are_exist(self):
        response = self.client.get(reverse('polls_app:poll', kwargs={'pk': 2}))
        self.assertContains(response, 'choice 21')
        self.assertContains(response, 'choice 22')

    def test_choices_for_expired_question_are_not_exist(self):
        response = self.client.get(reverse('polls_app:poll', kwargs={'pk': 1}))
        self.assertNotContains(response, 'choice 11')
        self.assertNotContains(response, 'choice 12')


class CompletedPollsTestView(TestCase):
    def setUp(self):
        self.poll_1 = Poll.objects.create(title=f"poll_zero_1", question_text=f"question poll_zero",
                                          date_ended=timezone.now(),
                                          answer_type='1')
        self.poll_2 = Poll.objects.create(title=f"poll_zero_2", question_text=f"question poll_zero_2",
                                          date_ended=timezone.now(),
                                          answer_type='1')
        self.poll_3 = Poll.objects.create(title=f"poll_3", question_text=f"question poll_3",
                                          date_ended=timezone.now() + timezone.timedelta(seconds=10),
                                          answer_type='1')
        self.poll_4 = Poll.objects.create(title=f"poll_4", question_text=f"question poll_4",
                                          date_ended=timezone.now() + timezone.timedelta(days=10),
                                          answer_type='1')
        self.completed_polls = Poll.objects.filter(pk__lte=2)

    def test_completed_view_exist(self):
        response = self.client.get('/polls/completed/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.template_name[0], 'polls_app/completed.html')

    def test_completed_view_get_by_name(self):
        response = self.client.get(reverse('polls_app:completed'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'polls_app/completed.html')

    def test_if_first_two_cases_exist(self):
        response = self.client.get('/polls/completed/')
        self.assertContains(response, 'poll_zero_1')
        self.assertContains(response, 'poll_zero_2')

    def test_if_last_two_cases_does_not_exist(self):
        response = self.client.get('/polls/completed/')
        self.assertNotContains(response, 'poll_3')
        self.assertNotContains(response, 'poll_4')


class ResultsTestView(TestCase):
    def setUp(self):
        self.poll_1 = Poll.objects.create(title="poll_zero_1", question_text="question poll_1",
                                          date_ended=timezone.now(),
                                          answer_type='N')
        self.poll_2 = Poll.objects.create(title="poll_zero_2", question_text="question poll_2",
                                          date_ended=timezone.now(),
                                          answer_type='1')
        self.choice_1_1 = Choice.objects.create(question=self.poll_1, choice_text="choice 11")
        self.choice_1_2 = Choice.objects.create(question=self.poll_1, choice_text="choice 12")
        self.choice_2_1 = Choice.objects.create(question=self.poll_2, choice_text="choice 21")
        self.choice_2_2 = Choice.objects.create(question=self.poll_2, choice_text="choice 22")

    def test_results_view_exist(self):
        for i in range(1, 3):
            response = self.client.get(f"/polls/{i}/results/")
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.template_name[0], 'polls_app/results.html')

    def test_results_view_get_by_name(self):
        response = self.client.get(reverse('polls_app:results', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 200)

    def test_results_view_does_not_exsit(self):
        for i in range(3, 7):
            response = self.client.get(f"/polls/{i}/results/")
            self.assertNotEqual(response.status_code, 200)

    def test_if_every_cases_are_exist(self):
        for i in (1, 2):
            response = self.client.get(reverse('polls_app:results', kwargs={'pk': i}))
            self.assertContains(response, f"question poll_{i}")


