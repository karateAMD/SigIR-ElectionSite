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
from django.db.models import Q

#retrieving keys for os environment
import utils



# AlchemyAPI
from alchemyapi import AlchemyAPI
alchemyapi = AlchemyAPI()


def process_tweets(tweets):
    newTweetsAdded = 0
    for tweet in tweets:
        if tweet.user:
            author = tweet.user.name.encode('ascii', errors='ignore')
            text = tweet.text.encode('ascii', errors='ignore')
            created_at = tweet.created_at
            location = tweet.user.location.encode('ascii', errors='ignore')
            state = get_state(location)
            candidate = get_candidates(text.lower())
            if candidate and state:
                sentiment = get_sentiment(text)
                if sentiment == -2:
                    print "Error getting sentiment"
                    continue
                try:
                    t, created = Tweet.objects.get_or_create(candidate=candidate, state=state, author=author, location=location, text=text, sentiment=sentiment, created_at = created_at)
                    if created:
                    	print "Tweet Processed"
                    	newTweetsAdded += 1
                    else:
                    	print "Duplicate Tweet"
                except IntegrityError as e:
                   print "IntegrityError" 
    print "\nNew tweets Added : {}".format(newTweetsAdded)
    print "Total tweets in database : {}".format(Tweet.objects.all().count())

#state returned if specified, otherwise return other
def get_state(location):
    if location != "":
    	qset = Q()
    	for term in location.split():
    		if term.lower() == "new":
    			continue
    		qset |= Q(name__contains=term)
    		if (len(term) == 2):
    			qset |= Q(abbreviation__exact=term)
    	location = State.objects.filter(qset).first()
    	return location 
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

# resorts tweets in database if needed
def resort():
	tweetsModified = 0
	for tweet in Tweet.objects.all():
		s = get_state(tweet.location)
		if s == None:
			continue
		if tweet.state != s:
			tweet.state = s
			tweet.save()
			tweetsModified += 1
	
	print "Tweets modified : {}".format(tweetsModified)
	print "Total tweets in database : {}".format(Tweet.objects.all().count())
		


def initialize():
    for t_keys in utils.get_twitter_keys():
        auth = OAuthHandler(t_keys['CONSUMER_KEY'], t_keys['CONSUMER_SECRET'])
        auth.set_access_token(t_keys['ACCESS_TOKEN'], t_keys['ACCESS_SECRET'])
        api = API(auth)

        tweets = api.search(q = 'donald OR trump OR cruz OR kasich OR bernie OR sanders OR hillary OR clinton', lang='en', count = 100)
       

        # Rate limit exceeded
        #if TweepError.message[0]['code'] == 88:
        #    continue


        process_tweets(tweets)
