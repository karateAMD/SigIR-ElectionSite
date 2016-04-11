import tweepy
import json
import keys
from alchemyapi import AlchemyAPI
import seed
import re, string

def process_tweet(tweet):
	state = match_state(tweet)
	candidate = match_candidate(tweet)
	return { 'state' : state, 'candidate' : candidate }

def match_state(tweet):
	restraints = [tweet['location']]
	for state in seed.states:
		if(searchWords(seed.states[state]["search_terms"], restraints)):
			return seed.states[state]['name']
	return 'other'

def match_candidate(tweet):
	restraints = [tweet['text']]
	for candidate in seed.candidates:
		query = seed.candidates[candidate]['last']
		if(searchWords(query , restraints)):
			return query
	return 'none'

def searchWords(words, texts):
    for word in words:
        for text in texts:
            if findWholeWord(word) (text):
                return True
    return False

def findWholeWord(w):
	return re.compile(r'\b({0})\b'.format(w), flags=re.IGNORECASE).search 

def get_tweets(num_tweets):
	search_query = 'Donald Trump OR Trump OR Bernie Sanders OR Sanders OR Hillary Clinton OR Ted Cruz OR John Kasich OR Kasich'
	tweet_count = 0
	max_tweets = num_tweets
	since_id =  None
	max_id = -1L
	
	for key_set in keys.oauth_keys:
		# check if max tweets has been reached
		if tweet_count >= max_tweets :
			print "Reached max tweets"
			break

		# authentication of Twitter API
		CONSUMER_KEY = key_set['CONSUMER_KEY']
		CONSUMER_SECRET = key_set['CONSUMER_SECRET']
		ACCESS_TOKEN = key_set['ACCESS_TOKEN']
		ACCESS_TOKEN_SECRET = key_set['ACCESS_SECRET']
	
		# auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
		# auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
		auth = tweepy.AppAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
	
		api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
	
		# AlchemyAPI
		alchemyapi = AlchemyAPI()
		alchemyapi.apikey = keys.alchemy_apikey[0]
	
		if not api:
			print "Can't Authenticate"
			break
	
		while tweet_count < max_tweets:
			if (max_tweets - tweet_count) < 100 :
				tweets_per_qry = max_tweets - tweet_count
			else:
				tweets_per_qry = 100
			try:
				if (max_id <= 0):
					if (not since_id):
						new_tweets = api.search(q=search_query, count=tweets_per_qry)
					else:
						new_tweets = api.search(q=search_query, count=tweets_per_qry, since_id=sinceId)
				else:
					if (not since_id):
						new_tweets = api.search(q=search_query, count=tweets_per_qry, max_id=str(max_id - 1))
					else:
						new_tweets = api.search(q=search_query, count=tweets_per_qry, max_id=str(max_id - 1), since_id=sinceId)
				if not new_tweets:
					print "No more tweets found"
					break
				for tweet in new_tweets:
					# create dictionary of tweet
			
					# skip the tweet if any information is missing
					if tweet.author.name == '' or tweet.text == '' or tweet.created_at == '':
						continue
		
					text = tweet.text
					response = alchemyapi.sentiment("text", text)
					if 'docSentiment' in response and 'score' in response['docSentiment']:
						sentiment = { 'score' : response['docSentiment']['score'], 'type' : response['docSentiment']['type'] }
					# continue onto the next tweet if AlechemyAPI can't perform sentiment analysis
					else:
						continue
					created_at = tweet.created_at
					author = tweet.author.name
					if tweet.author.location != '':
						location = tweet.author.location
					else:
						location = 'No location listed'
				
					new_tweet = { 'created_at' : created_at, 'author' : author, 'text' : text, 'location' : location, 'sentiment' : sentiment }
					print "finding match ..."
					matches = process_tweet(new_tweet)
					print (tweet_count+1)
					print matches
					print "{}\n\n".format(new_tweet)
					tweet_count += 1
			
			
				# tweet_count += len(new_tweets)
				max_id = new_tweets[-1].id
			except tweepy.TweepError as e:
				# Rate limit exceeded
				if e.message[0]['code'] == 88:
					print 'Rate limit exceeded'
					break
				# Just exit if any error
				print("some error : " + str(e))
				break
		print "Moving onto next set of keys ..."

		

def main():
	max_tweets = 50
	get_tweets(max_tweets)


if __name__ == '__main__':
	main()
