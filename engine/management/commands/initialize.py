from django.core.management.base import BaseCommand, CommandError
from engine.models import *
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
from engine import seed

class Command(BaseCommand):
	help = 'Initializes instances of State and/or Candidate'

	def add_arguments(self, parser):
		parser.add_argument('model', nargs=1, type=str)
	
	def handle(self, *args, **options):
		if options['model'][0] == 'all':
			self.initialize_all()
		elif options['model'][0] == 'states':
			self.initialize_states()
		elif options['model'][0] == 'candidates':
			self.initialize_candidates()
		else:
			raise CommandError('Invalid argument. Valid arguments are "all", "states", and "candidates".')

	def initialize_all(self):
		self.initialize_states()
		self.initialize_candidates()
	
	def initialize_states(self):
		for state in seed.states:
			try:
				s, created_s = State.objects.get_or_create(abbreviation=seed.states[state]["abbr"], name=seed.states[state]["name"])
				s.save()
			except IntegrityError as e:
				pass
			try:
				# create search terms
				for term in seed.states[state]["search_terms"]:
					t, created_t = SearchTerm.objects.get_or_create(text=term, state=s)
					t.save()
			except IntegrityError as e:
				pass
`
				
		self.stdout.write(self.style.SUCCESS('Successfully initialized states'))

	def initialize_candidates(self):
		for candidate in seed.candidates:
			try:
				c, created_c = Candidate.objects.get_or_create( first_name=seed.candidates[candidate]["first"], last_name=seed.candidates[candidate]["last"], party=seed.candidates[candidate]["party"])
				c.save()

				# match States with candidate
				for state in seed.states:
					try:
						s = State.objects.get(name=seed.states[state]["name"])
						c.states.add(s)
					except ObjectDoesNotExist as o:
						raise CommandError('State not found. States need to be initialized first.')
			except IntegrityError as e:
				pass
	
		self.stdout.write(self.style.SUCCESS('Successfully initialized candidates'))

