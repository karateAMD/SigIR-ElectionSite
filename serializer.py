import json
import keys

print json.dumps(keys.ALCHEMY_CODES)
print "\n\n"
print json.dumps(keys.TWITTER_CODES)
print "\n\nCopy above into an environment variable with the below syntax: \n"
print "export ALCHEMY_API_KEYS='{pasted text}'"
print "export TWITTER_API_KEYS='{pasted text}'"
