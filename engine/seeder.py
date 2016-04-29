# initializes States and Candidates

import seed
from models import State, Candidate
import IPython
from django.db import IntegrityError

def initialize_states():
	statesAdded = 0
	for state in seed.states:
		s, created_s = State.objects.get_or_create(abbreviation=seed.states[state]["abbr"], name=seed.states[state]["name"])
		if created_s:
			statesAdded += 1

	print "New states added : {}".format(statesAdded)
	print "Total states in database : {}".format(State.objects.all().count())

def initialize_candidates():
	candidatesAdded = 0
	for candidate in seed.candidates:
		c, created_c = Candidate.objects.get_or_create( first_name=seed.candidates[candidate]["first"], last_name=seed.candidates[candidate]["last"], party=seed.candidates[candidate]["party"])
		if created_c:
			candidatesAdded += 1

        # match States with Candidate
        for state in State.objects.all():
            c.states.add(State.objects.get(name=state.name))
	print "New candidates added : {}".format(candidatesAdded)
	print "Total candidates in database : {}".format(Candidate.objects.all().count())

def initialize():
	initialize_states()
	initialize_candidates()
