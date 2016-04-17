# import the necessary methods from tweepy library
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy import API
import json, re
import seed

#import django methods
from django.core.management.base import BaseCommand, CommandError
from models import *
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist

# twitter keys
import keys
consumer_key = keys.twitter_consumer_key
consumer_secret = keys.twitter_consumer_secret
access_token = keys.twitter_access_token
access_token_secret = keys.twitter_access_token_secret

# AlchemyAPI
from alchemyapi import AlchemyAPI
alchemyapi = AlchemyAPI()
alchemyapi.apikey = keys.alchemy_apikey

def process_tweets(tweets):
    for tweet in tweets:
        if tweet.user:
            author = tweet.user.name.encode('ascii', errors='ignore')
            text = tweet.text.encode('ascii', errors='ignore')
            created_at = tweet.created_at
            location = tweet.user.location.encode('ascii', errors='ignore')
            state = get_state(location.lower())
            sentiment = get_sentiment(text)
            candidate = get_candidates(text)

            if candidate:
                try:
                    t = Tweet(candidate=candidate, state=state, author=author, 
                        location=location, text=text, sentiment=sentiment, 
                        created_at = created_at)
                    t.save()
                    print "Tweet Processed"
                except IntegrityError as e:
                    pass
            else:
                print "\n\nno candidate found in text: \n{}".format(text)
    return


def get_state(location):
    if (location):
        for state in seed.states.values():
            if state['name'] in location:
                return State.objects.get(name=state['name'])
            if location.endswith(state['abbr']) or state['abbr'].upper() in location:
                return State.objects.get(name=state['name'])
    return State.objects.get(name='other')


# returns candidate object if exactly 1 candidate found (None otherwise)
def get_candidates(text):
    candidates = re.findall(r'trump|cruz|kasich|sanders|clinton', text.lower())
    if len(candidates) < 1:
        return None
    if len(candidates) > 1:
        firstcand = candidates[0]
        for candidate in candidates[1:]:
            if candidate != firstcand:
                return None
    candidate = candidates[0]
    for c in seed.candidates.values():
        if c['last'].lower() == candidate:
            return Candidate.objects.get(last_name=c['last'])


#returns sentiment value of type decimal (0 if not found)
def get_sentiment(text):
    response = alchemyapi.sentiment("text", text)
    if response.get('status') == 'ERROR':
        return 0
    else:
        if response['docSentiment']['type'] == 'neutral':
            return 0
        return float(response['docSentiment']['score'])


def initialize():
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = API(auth)

    tweets = api.search(q = 'trump OR cruz OR kasich OR sandrs OR clinton', count = 25)

    process_tweets(tweets)
