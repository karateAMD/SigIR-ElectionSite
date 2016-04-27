from django.core.management import BaseCommand
from retriever import get_tweets

class Command(BaseCommand):
    help = "Fetches tweets, matches them with State and Candidate, and stores them in the database1"

    def handle(self, *args, **options):
        get_tweets.initialize()
