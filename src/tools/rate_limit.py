import tweepy
from credentials import *

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

api = tweepy.API(auth)
public_tweets = api.home_timeline()
# user = api.get_user('@MyUserName')

data = api.rate_limit_status()
print(data['resources']['statuses']['/statuses/home_timeline'])
print(data['resources']['users']['/users/lookup'])