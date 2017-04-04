import datetime

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

from .models import Question

class QuestionMethodTests(TestCase):

	def test_was_published_with_future_question(self):
		time = timezone.now() + datetime.timedelta(days=30)
		future_question = Question(pub_date = time)
		self.assertIs(future_question.was_published_recently(),False)

	def test_was_published_with_recent_question(self):
		time = timezone.now() - datetime.timedelta(hours=1)
		recent_question = Question(pub_date = time)
		self.assertIs(recent_question.was_published_recently(),True)


def createQuestion(text,days):
	time = timezone.now() + datetime.timedelta(days=days)
	return Question.objects.create(question_text=text,pub_date=time)

class QuestionViewTests(TestCase):
	def test_index_view_with_no_questions(self):
		response = self.client.get(reverse('polls:index'))
		self.assertEqual(response.status_code,200)
		self.assertContains(response,"No polls are available.")
		self.assertQuerysetEqual(response.context['latest_question_list'],[])

	def test_index_view_with_one_future_question(self):
		createQuestion("future Question",6)
		response = self.client.get(reverse('polls:index'))
		self.assertEqual(response.status_code,200)
		self.assertContains(response,"No polls are available.")
		self.assertQuerysetEqual(response.context['latest_question_list'],[])

	def test_index_view_with_one_past_question(self):
		createQuestion("past",-10)
		response = self.client.get(reverse('polls:index'))
		self.assertEqual(response.status_code,200)
		
		self.assertQuerysetEqual(response.context['latest_question_list'],['<Question: past>'])

	def test_index_view_with_one_past_question_and_one_future_question(self):
		createQuestion("past",-10)
		createQuestion("future",10)
		response = self.client.get(reverse('polls:index'))
		self.assertEqual(response.status_code,200)
		
		self.assertQuerysetEqual(response.context['latest_question_list'],['<Question: past>'])

	def test_index_view_with_two_past_questions(self):
		createQuestion("past",-10)
		createQuestion("yesteryear",-20)
		response = self.client.get(reverse('polls:index'))
		self.assertEqual(response.status_code,200)
		
		self.assertQuerysetEqual(response.context['latest_question_list'],['<Question: past>','<Question: yesteryear>'])

class QuestionIndexDetailTests(TestCase):
	def test_detail_view_with_a_future_question(self):
		question = createQuestion("future",10)
		url = reverse('polls:detail',args=(question.id,))
		response= self.client.get(url)
		self.assertEqual(response.status_code,404)

	def test_detail_view_with_a_past_question(self):
		question = createQuestion("past",-10)
		url = reverse('polls:detail',args=(question.id,))
		response= self.client.get(url)
		self.assertContains(response,question.question_text)

