import json
import random
import os

def get_twitter_keys():
    twitter_keys = json.loads(os.environ['TWITTER_API_KEYS'])
    random.shuffle(twitter_keys)
    return twitter_keys

def get_alchemy_keys():
    alchemy_api_keys = json.loads(os.environ['ALCHEMY_API_KEYS'])
    random.shuffle(alchemy_api_keys)
    return alchemy_api_keys