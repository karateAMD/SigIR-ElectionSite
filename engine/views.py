from django.shortcuts import render
from django.http import HttpResponse
from .models import State, Candidate, Tweet
from retriever import get_tweets as GetTweets

def index(request):
	states_list = State.objects.order_by('name');
	context = {
		'states_list' : states_list,
	}
	return render(request, 'engine/index.html', context);

def get_tweets(request):
	GetTweets.initialize()
	return render(request, 'engine/tweets.html');
