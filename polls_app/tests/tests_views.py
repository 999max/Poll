import datetime

from django.test import TestCase
from django.utils import timezone

from polls_app.models import Poll, Choice
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
                                date_ended=datetime.datetime.now() + datetime.timedelta(seconds=i+10),
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
        self.poll_1 = Poll.objects.create(title=f"poll_zero", question_text=f"question poll_zero",
                            date_ended=timezone.now(),
                            answer_type='1')
        self.poll_2 = Poll.objects.create(title=f"poll_2", question_text=f"question poll_2",
                            date_ended=timezone.now()+timezone.timedelta(days=1),
                            answer_type='1')

    def test_poll_view_get_by_name(self):
        response = self.client.get(reverse('polls_app:poll', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 200)

    def test_poll_is_closed_for_inactive_poll(self):
        response = self.client.get(reverse('polls_app:poll', kwargs={'pk': 1}))
        self.assertContains(response, 'Voting was closed at')
        self.assertNotContains(response, 'Make your answer')

    def test_poll_is_not_closed_for_active_poll(self):
        response = self.client.get(reverse('polls_app:poll', kwargs={'pk': 2}))
        self.assertNotContains(response, 'Voting was closed at')
        self.assertContains(response, 'Make your answer')
