import os
from django.db import IntegrityError


states = {  "AL" : { "name" : "alabama", "abbr" : "AL", "search_terms" : ["alabama, al"], "tweets" : [], "count" : 0},
        	"AK" : { "name" : "alaska" , "abbr" : "AK", "search_terms" : ["alaska", "ak"], "tweets" : [], "count" : 0},
			"AZ" : { "name" : "arizona" , "abbr" : "AZ", "search_terms" : ["arizona", "az"], "tweets" : [], "count" : 0},
     		"AR" : { "name" : "arkansas" , "abbr" : "AR", "search_terms" : ["arkansas", "ar"], "tweets" : [], "count" : 0},
			"CA" : { "name" : "california" , "abbr" : "CA", "search_terms" : ["california", "ca"], "tweets" : [], "count" : 0},
			"CO" : { "name" : "colorado" , "abbr" : "CO", "search_terms" : ["colorado"], "tweets" : [], "count" : 0},
			"CT" : { "name" : "connecticut" , "abbr" : "CT", "search_terms" : ["connecticut", "ct"], "tweets" : [], "count" : 0},
			"DE" : { "name" : "delaware", "abbr" : "DE" , "serach_terms" : ["delaware", "de"], "tweets" : [], "count" : 0},
			"FL" : { "name" : "florida" , "abbr" : "FL", "search_terms" : ["florida", "fl"], "tweets" : [], "count" : 0},
			"GA" : { "name" : "georgia", "abbr" : "GA", "search_terms" : ["georgia", "ga"], "tweets" : [], "count" : 0},
			"HI" : { "name" : "hawaii" , "abbr" : "HI", "search_terms" : ["hawaii", "hi"], "tweets" : [], "count" : 0},
			"ID" : { "name" : "idaho" , "abbr" : "ID", "search_terms" : ["idaho", "id"], "tweets" : [], "count" : 0},
			"IL" : { "name" : "illinois" , "abbr" : "IL", "search_terms" : ["illinois", "il"], "tweets" : [], "count" : 0},
			"IN" : { "name" : "indiana" , "abbr" : "IN", "search_terms" : ["indiana", "in"], "tweets" : [], "count" : 0},
			"IA" : { "name" : "iowa" , "abbr" : "IA" , "search_terms" : ["iowa", "ia"], "tweets" : [], "count" : 0},
			"KS" : { "name" : "kansas" , "abbr" : "KS", "search_terms" : ["kansas", "ks"], "tweets" : [], "count" : 0},
			"KY" : { "name" : "kentucky" , "abbr" : "KY", "search_terms" : ["kentucky", "ky"], "tweets" : [], "count" : 0},
			"LA" : { "name" : "louisiana" , "abbr" : "LA", "search_terms" : ["louisiana", "la"], "tweets" : [], "count" : 0},
			"ME" : { "name" : "maine" , "abbr" : "ME", "search_terms" : ["maine", "me"], "tweets" : [], "count" : 0},
			"MD" : { "name" : "maryland" , "abbr" : "MD", "search_terms" : ["maryland", "md"], "tweets" : [], "count" : 0},
			"MA" : { "name" : "massachusetts" , "abbr" : "MA", "search_terms" : ["massachusetts", "ma"], "tweets" : [], "count" : 0},
			"MI" : { "name" : "michigan" , "abbr" : "MI", "search_terms" : ["michigan", "mi"], "tweets" : [], "count" : 0},
			"MN" : { "name" : "minnesota" , "abbr" : "MN", "search_terms" : ["minnesota", "mn"], "tweets" : [], "count" : 0},
			"MS" : { "name" : "mississippi" , "abbr" : "MS", "search_terms" : ["mississippi", "ms"], "tweets" : [], "count" : 0},
			"MO" : { "name" : "missouri" , "abbr" : "MO", "search_terms" : ["missouri", "mo"], "tweets" : [], "count" : 0},
			"MT" : { "name" : "montana" , "abbr" : "MT", "search_terms" : ["montana", "mt"], "tweets" : [], "count" : 0},
			"NE" : { "name" : "nebraska" , "abbr" : "NE", "search_terms" : ["nebraska", "ne"], "tweets" : [], "count" : 0},
			"NV" : { "name" : "nevada" , "abbr" : "NV", "search_terms" : ["nevada", "nv"], "tweets" : [], "count" : 0},
			"NH" : { "name" : "new hampshire" , "abbr" : "NH", "search_terms" : ["new hampshire", "nh"], "tweets" : [], "count" : 0},
			"NJ" : { "name" : "new jersey" , "abbr" : "NJ", "search_terms" : ["new jersey", "nj"], "tweets" : [], "count" : 0},
			"NM" : { "name" : "new mexico" , "abbr" : "NM", "search_terms" : ["new mexico", "nm"], "tweets" : [], "count" : 0},
			"NY" : { "name" : "new york" , "abbr" : "NY", "search_terms" : ["new york", "ny"], "tweets" : [], "count" : 0},
			"NC" : { "name" : "north carolina" , "abbr" : "NC", "search_terms" : ["north carolina", "nc"], "tweets" : [], "count" : 0},
			"ND" : { "name" : "north dakota" , "abbr" : "ND", "search_terms" : ["north dakota", "nd"], "tweets" : [], "count" : 0},
			"OH" : { "name" : "ohio" , "abbr" : "OH", "search_terms" : ["ohio", "oh"], "tweets" : [], "count" : 0},
			"OK" : { "name" : "oklahoma" , "abbr" : "OK", "search_terms" : ["oklahoma", "ok"], "tweets" : [], "count" : 0},
			"OR" : { "name" : "oregon" , "abbr" : "OR", "search_terms" : ["oregon", "or"], "tweets" : [], "count" : 0},
			"PA" : { "name" : "pennsylvania" , "abbr" : "PA", "search_terms" : ["pennsylvania", "pa"], "tweets" : [], "count" : 0},
			"RI" : { "name" : "rhode island" , "abbr" : "RI", "search_terms" : ["rhode island", "ri"], "tweets" : [], "count" : 0},
			"SC" : { "name" : "south carolina" , "abbr" : "SC", "search_terms" : ["south carolina", "sc"], "tweets" : [], "count" : 0},
			"SD" : { "name" : "south dakota" , "abbr" : "SD", "search_terms" : ["south dakota", "sd"], "tweets" : [], "count" : 0},
			"TN" : { "name" : "tennessee" , "abbr" : "TN", "search_terms" : ["tennessee", "tn"], "tweets" : [], "count" : 0},
			"TX" : { "name" : "texas" , "abbr" : "TX", "search_terms" : ["texas", "tx"], "tweets" : [], "count" : 0},
			"UT" : { "name" : "utah" , "abbr" : "UT", "search_terms" : ["utah", "ut"], "tweets" : [], "count" : 0},
			"VT" : { "name" : "vermont" , "abbr" : "VT", "search_terms" : ["vermont", "vt"], "tweets" : [], "count" : 0},
			"VA" : { "name" : "virginia" , "abbr" : "VA", "search_terms" : ["virginia", "va"], "tweets" : [], "count" : 0},
			"WA" : { "name" : "washington" , "abbr" : "WA", "search_terms" : ["washington", "wa"], "tweets" : [], "count" : 0},
			"WV" : { "name" : "west virginia" , "abbr" : "WV", "search_terms" : ["west virginia", "wv"], "tweets" : [], "count" : 0},
			"WI" : { "name" : "wisconsin" , "abbr" : "WI", "search_terms" : ["wisconsin", "wi"], "tweets" : [], "count" : 0},
			"WY" : { "name" : "wyoming" , "abbr" : "WY", "search_terms" : ["wyoming", "wy"], "tweets" : [], "count" : 0},
			"other" : { "name" : "other" , "abbr" : "OT", "search_terms" : ["no state found"], "tweets": [], "count" : 0}
                    }

def initialize_states():
	for state in states:
		try:
			temp = State(abbreviation=states[state]["abbr"], name=states[state]["name"])
			temp.save()
		except IntegrityError as e:
			print "Pass"
		#create SearchTerms
		"""
		for term in states[state]["search_terms"]:
		"""
"""
def delete_states():
	for state in State.objects.all():
		state.delete()
"""

if __name__ == "__main__":
	os.environ.setdefault("DJANGO_SETTINGS_MODULE", "election_site.settings")
	import django
	django.setup()
	
	from engine.models import State, SearchTerm, Candidate, Tweet

	"""
	from django.core.wsgi import get_wsgi_application
	from whitenoise.django import DjangoWhiteNoise

	application = get_wsgi_application()
	application = DjangoWhiteNoise(application)
	"""

	initialize_states()
