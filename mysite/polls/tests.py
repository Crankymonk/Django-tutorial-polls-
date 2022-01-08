import datetime 

from django.test import TestCase
from django.utils import timezone

from polls import models

# Create your tests here.

class QuestionModelTests(TestCase):

    def test_was_published_recently_with_feauture_question(self):
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = models.Question(pub_date=time)
        self.assertFalse(future_question.was_published_recently())

    def test_was_published_recently_with_old_question(self):
        time = timezone.now() - datetime.timedelta(days=30)
        old_question = models.Question(pub_date=time)
        self.assertFalse(old_question.was_published_recently())

    def test_was_published_recently_with_recent_question(self):
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = models.Question(pub_date=time)
        self.assertTrue(recent_question.was_published_recently())