import json
import random
import os

def get_random_twitter_credentials():
    twitter_codes = json.loads(os.environ['TWITTER_API_KEYS'])
    random.shuffle(twitter_codes)
    return twitter_codes

def get_random_alchemy_credentials():
    alchemy_api_keys = json.loads(os.environ['ALCHEMY_API_KEYS'])
    random.shuffle(alchemy_api_keys)
    return alchemy_api_keys