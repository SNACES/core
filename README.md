# SNACES

SNACES (Social Network Algorithm Contained Experiment System)
is a Python library for downloading and analyze Twitter data, by making
use of the Tweepy library and the Twitter API.

## Setup

### Twitter Developer Account

In order to make use of the Twitter API, and the tweepy package, you will need
credential for the twitter API.

To retrieve these credentials sign up for a developer twitter account [here](https://developer.twitter.com/en/apply-for-access).

Getting access may be immediate or may take several days.
Once your application is approved, you will get four values: 
`API Key`, `API Key Secret`, `Access Token`, and `Access Token Secret`.
Create a file with this path `./conf/credentials.py` and enter the four values into the file in this format:
```python
ACCESS_TOKEN = "<Your Access Token>"
ACCESS_TOKEN_SECRET = "<Your Access Token Secret>"
CONSUMER_KEY = "<Your API Key>"
CONSUMER_SECRET = "<Your API Key Secret>"
```
Note that the API Key is also known as the Consumer Key.

### Installing
Python 3.9 is required for the following installation steps.

Follow the instructions in the main README.md file to setup the environment.

### Notes
The algorithm, as run below, takes tweets from July 16, 2022 to July 16, 2023. This date is a bit arbitrary, but it is important to fix the date range since no new tweets are being added to the dataset. This can be viewed at `src/dao/raw_tweet/getter/mongo_raw_tweet_getter.py` in the function `get_tweets_by_user_ids`.

## Running

1. The main program can be started by running `python detect_core_jaccard.py -n {seed_user} -act {user_activity}`. For example 
`python detect_core_jaccard.py -n "hardmaru" -act "user retweets"` for seed user "hardmaru" and user activity "user retweets".
