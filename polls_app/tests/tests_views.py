import datetime

from django.test import TestCase

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
        for i in range(3):
            Poll.objects.create(title=f"poll_{i}", question_text=f"question poll{i}",
                                date_ended=datetime.datetime.now() + datetime.timedelta(seconds=i+10),
                                answer_type='1')
        Poll.objects.create(title=f"poll_zero", question_text=f"question poll_zero",
                            date_ended=datetime.datetime.now(),
                            answer_type='1')

    def test_polls_view_exist(self):
        response = self.client.get('/polls/')
        self.assertEqual(response.status_code, 200)

    def test_polls_view_get_by_name(self):
        response = self.client.get(reverse('polls_app:polls'))
        self.assertEqual(response.status_code, 200)

    def test_polls_view_context(self):
        response = self.client.get('/polls/')

        self.assertEqual(response.template_name[0], 'polls_app/polls.html')
        self.assertEqual(len(response.context['object_list']), 4)
        self.assertEqual(response.context['object_list'], response.context['polls'])

        self.assertEqual(response.context['object_list'][0].id, 1)
        self.assertEqual(response.context['object_list'][1].id, 2)
        self.assertEqual(response.context['object_list'][2].id, 3)
        self.assertEqual(response.context['object_list'][3].id, 4)

        self.assertEqual(response.context['object_list'][0].title, 'poll_0')
        self.assertEqual(response.context['object_list'][1].title, 'poll_1')
        self.assertEqual(response.context['object_list'][2].title, 'poll_2')
        self.assertEqual(response.context['object_list'][3].title, 'poll_zero')

        self.assertEqual(response.context['object_list'][0].question_text, 'question poll0')
        self.assertEqual(response.context['object_list'][1].question_text, 'question poll1')

