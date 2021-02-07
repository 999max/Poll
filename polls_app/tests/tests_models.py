from django.test import TestCase
from django.utils import timezone

from polls_app.models import Poll, Choice


class PollModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Poll.objects.create(title="Fish", question_text="How much is the fish?",
                            date_ended=timezone.now() + timezone.timedelta(days=3),
                            answer_type='1')

    def test_title_max_length(self):
        poll_1 = Poll.objects.get(pk=1)
        max_l = poll_1._meta.get_field('title').max_length
        self.assertEqual(max_l, 150)

    def test_date_added_exist(self):
        poll_1 = Poll.objects.get(pk=1)
        self.assertEqual(True, bool(poll_1.date_added))

    def test_date_added_lower_date_ended(self):
        poll_1 = Poll.objects.get(pk=1)
        self.assertLess(poll_1.date_added, poll_1.date_ended)

    def test_title_string(self):
        poll_1 = Poll.objects.get(pk=1)
        expected_name = f"{poll_1.question_text}"[:50]
        self.assertEqual(expected_name, str(poll_1))


class ChoiceModelTest(TestCase):
    def setUp(self):
        self.poll_1 = Poll.objects.create(title="Color", question_text="what color is the sun?",
                                          date_ended=timezone.now() + timezone.timedelta(days=1),
                                          answer_type='N')
        self.choice_1 = Choice.objects.create(question=self.poll_1, choice_text="Red")
        self.choice_2 = Choice.objects.create(question=self.poll_1, choice_text="Yellow")
        self.choice_3 = Choice.objects.create(question=self.poll_1, choice_text="Green")

        self.poll_2 = Poll.objects.create(title="Weather", question_text="What weather do you like?",
                                          date_ended=timezone.now() + timezone.timedelta(days=1),
                                          answer_type='1')
        self.choice_4 = Choice.objects.create(question=self.poll_2, choice_text="Sunny")
        self.choice_5 = Choice.objects.create(question=self.poll_2, choice_text="Rainy")
        self.choice_6 = Choice.objects.create(question=self.poll_2, choice_text="Fog")

    def test_choice_text_max_length(self):
        ch_1 = Choice.objects.get(pk=1)
        max_l = ch_1._meta.get_field('choice_text').max_length
        self.assertEqual(max_l, 200)

    def test_votes_counts_is_nill(self):
        for i in range(1, 7):
            choice = Choice.objects.get(pk=i)
            self.assertEqual(choice.votes, 0)

    def test_choice_text_string(self):
        for i in range(1, 7):
            choice = Choice.objects.get(pk=i)
            expected_text = f"{choice.choice_text}"
            self.assertEqual(expected_text, str(choice))
