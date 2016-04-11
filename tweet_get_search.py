# import the necessary methods from tweepy library
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy import API
import json
import re

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

# candidate class, one for each of the 5 candidates is created
class Candidate: 
    def __init__(self, name):
        self.name = name
        self.tweets = []
        self.states = { "AL" : { "names" : ["alabama, al"], "tweets" : [], "count" : 0},
                        "AK" : { "names" : ["alaska", "ak"], "tweets" : [], "count" : 0},
                        "AZ" : { "names" : ["arizona", "az"], "tweets" : [], "count" : 0},
                        "AR" : { "names" : ["arkansas", "ar"], "tweets" : [], "count" : 0},
                        "CA" : { "names" : ["california", "ca"], "tweets" : [], "count" : 0},
                        "CO" : { "names" : ["colorado"], "tweets" : [], "count" : 0},
                        "CT" : { "names" : ["connecticut", "ct"], "tweets" : [], "count" : 0},
                        "DE" : { "names" : ["delaware", "de"], "tweets" : [], "count" : 0},
                        "FL" : { "names" : ["florida", "fl"], "tweets" : [], "count" : 0},
                        "GA" : { "names" : ["georgia", "ga"], "tweets" : [], "count" : 0},
                        "HI" : { "names" : ["hawaii", "hi"], "tweets" : [], "count" : 0},
                        "ID" : { "names" : ["idaho", "id"], "tweets" : [], "count" : 0},
                        "IL" : { "names" : ["illinois", "il"], "tweets" : [], "count" : 0},
                        "IN" : { "names" : ["indiana", "in"], "tweets" : [], "count" : 0},
                        "IA" : { "names" : ["iowa", "ia"], "tweets" : [], "count" : 0},
                        "KS" : { "names" : ["kansas", "ks"], "tweets" : [], "count" : 0},
                        "KY" : { "names" : ["kentucky", "ky"], "tweets" : [], "count" : 0},
                        "LA" : { "names" : ["louisiana", "la"], "tweets" : [], "count" : 0},
                        "ME" : { "names" : ["maine", "me"], "tweets" : [], "count" : 0},
                        "MD" : { "names" : ["maryland", "md"], "tweets" : [], "count" : 0},
                        "MA" : { "names" : ["massachusetts", "ma"], "tweets" : [], "count" : 0},
                        "MI" : { "names" : ["michigan", "mi"], "tweets" : [], "count" : 0},
                        "MN" : { "names" : ["minnesota", "mn"], "tweets" : [], "count" : 0},
                        "MS" : { "names" : ["mississippi", "ms"], "tweets" : [], "count" : 0},
                        "MO" : { "names" : ["missouri", "mo"], "tweets" : [], "count" : 0},
                        "MT" : { "names" : ["montana", "mt"], "tweets" : [], "count" : 0},
                        "NE" : { "names" : ["nebraska", "ne"], "tweets" : [], "count" : 0},
                        "NV" : { "names" : ["nevada", "nv"], "tweets" : [], "count" : 0},
                        "NH" : { "names" : ["new hampshire", "nh"], "tweets" : [], "count" : 0},
                        "NJ" : { "names" : ["new jersey", "nj"], "tweets" : [], "count" : 0},
                        "NM" : { "names" : ["new mexico", "nm"], "tweets" : [], "count" : 0},
                        "NY" : { "names" : ["new york", "ny"], "tweets" : [], "count" : 0},
                        "NC" : { "names" : ["north carolina", "nc"], "tweets" : [], "count" : 0},
                        "ND" : { "names" : ["north dakota", "nd"], "tweets" : [], "count" : 0},
                        "OH" : { "names" : ["ohio", "oh"], "tweets" : [], "count" : 0},
                        "OK" : { "names" : ["oklahoma", "ok"], "tweets" : [], "count" : 0},
                        "OR" : { "names" : ["oregon", "or"], "tweets" : [], "count" : 0},
                        "PA" : { "names" : ["pennsylvania", "pa"], "tweets" : [], "count" : 0},
                        "RI" : { "names" : ["rhode island", "ri"], "tweets" : [], "count" : 0},
                        "SC" : { "names" : ["south carolina", "sc"], "tweets" : [], "count" : 0},
                        "SD" : { "names" : ["south dakota", "sd"], "tweets" : [], "count" : 0},
                        "TN" : { "names" : ["tennessee", "tn"], "tweets" : [], "count" : 0},
                        "TX" : { "names" : ["texas", "tx"], "tweets" : [], "count" : 0},
                        "UT" : { "names" : ["utah", "ut"], "tweets" : [], "count" : 0},
                        "VT" : { "names" : ["vermont", "vt"], "tweets" : [], "count" : 0},
                        "VA" : { "names" : ["virginia", "va"], "tweets" : [], "count" : 0},
                        "WA" : { "names" : ["washington", "wa"], "tweets" : [], "count" : 0},
                        "WV" : { "names" : ["west virginia", "wv"], "tweets" : [], "count" : 0},
                        "WI" : { "names" : ["wisconsin", "wi"], "tweets" : [], "count" : 0},
                        "WY" : { "names" : ["wyoming", "wy"], "tweets" : [], "count" : 0},
                        "other" : { "names" : ["no state found"], "tweets": [], "count" : 0}
                    }
    # sort the tweet by location
    def add(self, tweet):
        restraints = [tweet.location, tweet.text, tweet.author]
        for state in self.states:
            if(self.searchWords(self.states[state]["names"], restraints)):
                self.states[state]["tweets"].append(tweet)
                self.states[state]["count"] += 1
                return

        self.states["other"]["tweets"].append(tweet)
        self.states["other"]["count"] += 1   

    def searchWords(self, words, texts):
        for word in words:
            for text in texts:
                if self.findWholeWord(word) (text):
                    return True
        return False

    def findWholeWord(self, w):
        return re.compile(r'\b({0})\b'.format(w), flags=re.IGNORECASE).search

    def print_state_tweets(self, state):
        count = 1
        formatted = ""
        for tweet in self.states[state]["tweets"]:
            
            formatted += "{}.\tAuthor: {}\n\tTweet: {}\n\tSentiment: {}\n\tLocation: {}\n".format(count, tweet.author, tweet.text, tweet.sentiment, tweet.location)
            count += 1

        header = "{}:".format((self.states[state]["names"][0]).upper())
        if formatted == "":
            return "{}\nNO TWEETS FOUND\n".format(header)
        else:
            return "{}\n{}\n".format(header, formatted)


def process_tweets(tweets, candidates):
    for tweet in tweets:
        if tweet.user:
            # get tweets author, text, location, and sentiment
            author = tweet.user.name.encode('ascii',errors='ignore')
            text = tweet.text.encode('ascii', errors='ignore')
            if (tweet.user.location):
                location = tweet.user.location.encode('ascii', errors='ignore')
            else:
                location = "No location listed"
            sentiment = get_sentiment(text)

            # make and store a tweet per candidate mentioned    
            candids = get_candidates(tweet)
            if candids: # in case no candidate is found
                for candid in candids:
                    new_tweet = Tweet(author, text, location, sentiment)
                    candidates[candid].add(new_tweet)
            else:
                print text

            print "Tweet Processed"
    return candidates


# finds and logs candidate(s) mentioned in the current tweet
def get_candidates(tweet):
    text = tweet.text.lower()
    url = tweet.w
    candids = re.findall(r'trump|clinton|sanders|cruz|kasich', text)
    return candids

def get_sentiment(text):
    response = alchemyapi.sentiment("text", text)
    if response.get('status') == 'ERROR':
        return response['statusInfo']
    else:
        return response['docSentiment']


if __name__ == "__main__":
    # initialize candidates
    trump = Candidate("trump")
    cruz = Candidate("cruz")
    kasich = Candidate("kasich")
    sanders = Candidate("sanders")
    clinton = Candidate("clinton")
    candidates = {trump.name:trump, cruz.name:cruz, kasich.name:kasich, sanders.name:sanders, clinton.name:clinton}

    # initialize stream
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = API(auth)

    tweets = api.search(q = 'trump', count = 50)

    candidates = process_tweets(tweets, candidates)

    # print out recorded tweets
    for candidate in candidates.values():
        for state in candidate.states:
            if candidate.states[state]["count"] != 0:
                print candidate.print_state_tweets(state)















































