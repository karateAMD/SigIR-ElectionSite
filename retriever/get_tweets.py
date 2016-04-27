import json
from re import search
from sys import exit

# import the necessary methods from tweepy library
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler, Stream, API
from tweepy import TweepError

#import django methods
from django.core.management.base import BaseCommand, CommandError
from engine.models import *
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist

#retrieving keys for os environment
import utils



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
    for a_key in utils.get_alchemy_keys():
        alchemyapi.apikey = a_key
        response = alchemyapi.sentiment("text", text)

        #check if current key is overused
        if response.get('status') == 'ERROR':
            continue
        if response['docSentiment']['type'] == 'neutral':
            return 0
        return float(response['docSentiment']['score'])


def initialize():
    for t_keys in utils.get_twitter_keys():
        auth = OAuthHandler(t_keys['CONSUMER_KEY'], t_keys['CONSUMER_SECRET'])
        auth.set_access_token(t_keys['ACCESS_TOKEN'], t_keys['ACCESS_SECRET'])
        api = API(auth)

        tweets = api.search(q = 'donald OR trump OR cruz OR kasich OR bernie OR sanders OR hillary OR clinton', count = 50)
       

        # Rate limit exceeded
        #if TweepError.message[0]['code'] == 88:
        #    continue


        process_tweets(tweets)
