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

# debugging
from pprint import pprint
from sys import exit

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
            author = tweet.user.name.encode('ascii',errors='ignore')
            text = tweet.text.encode('ascii', errors='ignore')
            created_at = tweet.created_at
            state = get_state(tweet.user.location)
            sentiment = get_sentiment(text)
            candidate = get_candidates(text)

            #candidate must exist to create tweet
            if candidate:
                try:
                    t = Tweet(candidate=candidate, state=state, created_at=created_at, 
                        author=author, text=text, sentiment=sentiment)
                    t.save()
                    print "Tweet Processed"
                except IntegrityError as e:
                    pass
            else:
                print "\n\nno candidate found in text: \n{}".format(text)

    return

def get_state(location):
    if (location):
        location.encode('ascii', errors='ignore')
        for state in seed.states.values():
            for term in state['search_terms']:
                if term in location:
                    return State(name=state['name'], abbreviation=state['abbr'])
    else:
        return State(name='other', abbreviation='OT')






# finds candidate(s) mentioned in the current tweet
# returns candidate object if exactly 1 candidate found
# otherwise returns None
def get_candidates(text):
    candidates = re.findall(r'trump|cruz|kasich|sanders|clinton', text.lower())
    #return None if > 1 or < 1 candidate found (unless only repeated candidate)
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
            return Candidate(first_name=c['first'], last_name=c['last'], party=c['party'])



def get_sentiment(text):
    response = alchemyapi.sentiment("text", text)
    if response.get('status') == 'ERROR':
        return response['statusInfo']
    else:
        return response['docSentiment']


def initialize():
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = API(auth)

    tweets = api.search(q = 'trump | ', count = 10)

    process_tweets(tweets)
