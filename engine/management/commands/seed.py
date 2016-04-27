from django.core.management.base import BaseCommand, CommandError
from engine import seeder

class Command(BaseCommand):
	help = 'Initializes instances of State and Candidate'

	def handle(self, *args, **options):
		seeder.initialize()
