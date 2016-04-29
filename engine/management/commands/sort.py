from django.core.management import BaseCommand
from retriever import get_tweets

class Command(BaseCommand):
    help = "Resorts all tweets in the database"

    def handle(self, *args, **options):
        get_tweets.resort()
