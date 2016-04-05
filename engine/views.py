from django.shortcuts import render
from django.http import HttpResponse
from .models import State, SearchTerm, Candidate, Tweet

def index(request):
	states_list = State.objects.order_by('name');
	context = {
		'states_list' : states_list,
	}
	return render(request, 'engine/index.html', context);
