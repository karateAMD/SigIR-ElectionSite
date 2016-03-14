# fixes SNIMissingWarning
import urllib3.contrib.pyopenssl
urllib3.contrib.pyopenssl.inject_into_urllib3()

# Import the necessary methods from tweepy library
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import json

import re, string

# AlchemyAPI
from alchemyapi import AlchemyAPI
alchemyapi = AlchemyAPI()
alchemyapi.apikey = "6ef2cc0d08007ca6c2710c697466a5ed206ff487"

#TwitterAPI keys
consumer_key = 	"dV62jowOdyOGFHXTz2n8S0m7k"
consumer_secret = "wpar83p7x8jFVm3ZGc5QSD1ThlbKG8gN3s0aBEqdqrxMpyALuQ"
access_token = "632282263-UxE1BZfYhs1socKlm2gKJXUxont6PZWhpRFWRIfM"
access_token_secret = "fkQBXFFpg9L5wGqDmON4hJadcz9HkkhWFo31eBFkihYOu"


# Tweet object
class Tweet:
    def __init__(self, author, text, location):
        self.author = author
        self.text = text
        self.location = location

# SortedTweets object
class SortedTweets:
    def __init__(self, maximum):
        #states dictionary
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
        self.max = maximum;
        self.size = 0;

    # sort the tweet by location
    def add(self, tweet):
        self.size += 1
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
            # get response
            response = alchemyapi.sentiment("text", tweet.text)
            if response.get('status') == 'ERROR':
                response = response['statusInfo']
            else:
                response = response['docSentiment']
            
            formatted += "{}.\tAuthor: {}\n\tTweet: {}\n\tSentiment: {}\n\tLocation: {}\n".format(count, tweet.author, tweet.text, response, tweet.location)
            count += 1

        header = "{}:".format((self.states[state]["names"][0]).upper())
        if formatted == "":
            return "{}\nNO TWEETS FOUND\n".format(header)
        else:
            return "{}\n{}\n".format(header, formatted)




# This is a basic listener that just prints received tweets to stdout.
class StdOutListener(StreamListener):
    def __init__(self, sorter):
        super(StreamListener, self).__init__();
        self.sorter = sorter

    def on_data(self, data):
        tweet = json.loads(data)
        # Avoid ASCII errors - really important!
        # get author, text, location, and sentiment response from tweet
        author = tweet["user"]["name"].encode('ascii',errors='ignore')
        text = tweet["text"].encode('ascii', errors='ignore')
        if (tweet["user"]["location"]):
            location = tweet["user"]["location"].encode('ascii', errors='ignore')
        else:
            location = "No location listed"
        new_tweet = Tweet(author, text, location) #new Tweet created
        self.sorter.add(new_tweet)
        print "Tweet processed"

        if self.sorter.size < self.sorter.max:
            return True
        else:
            return False

    def on_error(self, status):
        print status # Will print a status number - look up status codes and what they mean

tweet_sorter = SortedTweets(50)
streamer = StdOutListener(tweet_sorter)
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
stream = Stream(auth, streamer)

# stream.filter(track=['donald trump', 'hillary clinton', 'jeb bush', 'marco rubio'])
stream.filter(track=['trump2016'])

for state in tweet_sorter.states:
    if tweet_sorter.states[state]["count"] != 0:
        print tweet_sorter.print_state_tweets(state)
