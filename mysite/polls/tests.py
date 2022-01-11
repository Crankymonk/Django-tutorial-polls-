import datetime 

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

from polls import models

# Create your tests here.

def create_question(question_text, days):
    time = timezone.now() + datetime.timedelta(days=days)
    return models.Question.objects.create(question_text=question_text, pub_date=time)

class QuestionIndex(TestCase):
    
    def test_no_question(self):
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No polls are available.')
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_past_question(self):
        question = create_question(question_text='Past Question', days=-45)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            [question]
            )

    def test_future_question(self):
            create_question(question_text='Past Question', days=1)
            response = self.client.get(reverse('polls:index'))
            self.assertContains(response, 'No polls are available.')
            self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_future_and_past_question(self):
        question = create_question(question_text='Past Question', days=-45)
        create_question(question_text='Past Question', days=1)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            [question]
            )

    def test_two_past_question(self):
        question1 = create_question(question_text='Past Question 1', days=-30)
        question2 = create_question(question_text='Past Question 2', days=-15)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            [question2, question1]
            )


class QuestionDetailViewTests(TestCase):

    def test_future_question(self):
        feauture_question = create_question(question_text='Feauture question', days=30)
        url = reverse('polls:detail', args=(feauture_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        past_question = create_question(question_text='Past question', days=-30)
        url = reverse('polls:detail', args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)

class QuestionModelTests(TestCase):

    def test_was_published_recently_with_feauture_question(self):
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = models.Question(pub_date=time)
        self.assertFalse(future_question.was_published_recently())

    def test_was_published_recently_with_old_question(self):
        time = timezone.now() - datetime.timedelta(days=40)
        old_question = models.Question(pub_date=time)
        self.assertFalse(old_question.was_published_recently())

    def test_was_published_recently_with_recent_question(self):
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = models.Question(pub_date=time)
        self.assertTrue(recent_question.was_published_recently())