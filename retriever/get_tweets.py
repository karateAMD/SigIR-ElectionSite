import json
from re import search
from sys import exit

# import the necessary methods from tweepy library
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler, Stream, API

#import django methods
from django.core.management.base import BaseCommand, CommandError
from engine.models import *
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist

# keys
import utils
# import keys
# consumer_key = keys.twitter_consumer_key
# consumer_secret = keys.twitter_consumer_secret
# access_token = keys.twitter_access_token
# access_token_secret = keys.twitter_access_token_secret

# AlchemyAPI
from alchemyapi import AlchemyAPI
alchemyapi = AlchemyAPI()


def process_tweets(tweets):
    for tweet in tweets:
        if tweet.user:
            author = tweet.user.name.encode('ascii', errors='ignore')
            text = tweet.text.encode('ascii', errors='ignore')
            created_at = tweet.created_at
            location = tweet.user.location.encode('ascii', errors='ignore')
            state = get_state(location.lower())
            candidate = get_candidates(text.lower())
            if candidate and state:
                sentiment = get_sentiment(text)
                if sentiment == -2:
                    print "error getting sentiment"
                    continue
                try:
                    t = Tweet(candidate=candidate, state=state, author=author, 
                        location=location, text=text, sentiment=sentiment, 
                        created_at = created_at)
                    t.save()
                    print "Tweet Processed"
                except IntegrityError as e:
                    pass

#state returned if specified, otherwise return other
def get_state(location):
    if (location):
        for state in State.objects.all():
            if state.name in location:
                return State.objects.get(name=state.name)
            if location.endswith(state.abbreviation) or state.abbreviation.upper() in location:
                return State.objects.get(name=state.name)
    return None

# returns candidate object if exactly 1 candidate found (None otherwise)
def get_candidates(text):
    candidates = []
    for Cand in Candidate.objects.all():
        if Cand.first_name.lower() in text or Cand.last_name.lower() in text:
            candidates.append(Cand)
    if len(candidates) < 1 or len(candidates) > 1:
        return None
    return candidates[0]


#returns sentiment value of type decimal (0 if not found)
def get_sentiment(text):
    for key in 
    response = alchemyapi.sentiment("text", text)
    if response.get('status') == 'ERROR':
        return -2
    if response['docSentiment']['type'] == 'neutral':
        return 0
    return float(response['docSentiment']['score'])


def initialize():
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = API(auth)

    tweets = api.search(q = 'donald OR trump OR cruz OR kasich OR bernie OR sanders OR hillary OR clinton', count = 1000)

    process_tweets(tweets)
