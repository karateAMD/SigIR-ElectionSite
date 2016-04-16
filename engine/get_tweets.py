# import the necessary methods from tweepy library
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy import API
import json
import re

#import django methods
from django.core.management.base import BaseCommand, CommandError
from engine.models import *
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

# tweet class
class Tweet:
    def __init__(self, author, text, location, sentiment):
        self.author = author
        self.text = text
        self.location = location
        self.sentiment = sentiment


def process_tweets(tweets):
    for tweet in tweets:
        if tweet.user:
            # get tweets author, text, location, date, and sentiment
            author = tweet.user.name.encode('ascii',errors='ignore')
            text = tweet.text.encode('ascii', errors='ignore')
            created_at = tweet.created_at.encode('ascii',errors='ignore')
            if (tweet.user.location):   
                location = tweet.user.location.encode('ascii', errors='ignore')
            else:
                location = "other"
            sentiment = get_sentiment(text)

            # make and store if only one candidate found  
            candidate = get_candidates(tweet)
            if candidate:
                try:
                    t = Tweet(candidate=candidate, state=location, created_at=created_at, 
                        author=author, text=text, sentiment=sentiment)
                    t.save()
                    print "Tweet Processed"
                except IntegrityError as e:
                    pass
            else:
                print "ERROR: no candidate found in text"

    return


# finds candidate(s) mentioned in the current tweet
# returns None if 0 found or > 1 found
def get_candidates(tweet):
    text = tweet.text.lower()
    candidates = re.findall(r'(trump)|(cruz)|(kasich)|(bernie|sanders)|(hillary|clinton)', text)
    #if len(candidates) < 1 or len(candidates) > 1:
    #    return None
    return candidates[0]

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

    tweets = api.search(q = 'trump', count = 10)

    process_tweets(tweets)