from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def index(request):
	return HttpResponse("Hello ,World! You are at the polls index! :D ")

def detail(request,question_id):
	return HttpResponse("You are looking at question %s."% question_id)

def results(request,question_id):
	return HttpResponse("You are looking at the results for the question %s"%question_id)

def vote(request,question_id):
	return HttpRespose("You're voting on question %s"%question_id)
