import datetime
from django.test import TestCase

from polls_app.models import Poll


class PollModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Poll.objects.create(title="Fish", question_text="How much is the fish?",
                            date_ended=datetime.datetime.now() + datetime.timedelta(days=3),
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
