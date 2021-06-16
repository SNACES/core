from src.process.community_ranking.community_ranker import CommunityRanker
from typing import List


class LinearCommunityRanker(CommunityRanker):
    def __init__(self, raw_tweet_getter):
        self.raw_tweet_getter = raw_tweet_getter
        self.ranking_function_name = "retweets"

    def score_users(self, users: List, current_community: List, gamma=3):
        """
        @param users: list of users' ids
        @param current_community: list of current community users' ids
        @param gamma: the coefficient of # of tweets
        """
        # calculate retweet score
        retweet_scores = {}
        tweet_scores = {}
        for id in users:
            retweet_scores[id] = 0
            tweet_scores[id] = 0

        for id in users:
            retweets = self.raw_tweet_getter.get_retweets_of_user_by_user_id(id)
            for retweet in retweets:
                if (str(retweet.user_id) in current_community) or (int(retweet.user_id) in current_community):
                    if int(retweet.user_id) != int(id):
                        retweet_scores[id] += 1

        # calculate tweet score
        for id in users:
            tweets = self.raw_tweet_getter.get_tweets_by_user_id(id)
            for tweet in tweets:
                if tweet.retweet_user_id is not None:
                    if (str(tweet.retweet_user_id) in current_community or int(
                            tweet.retweet_user_id) in current_community) and (str(tweet.retweet_user_id) != str(id)):
                        if 190 < len(tweets) < 201:
                            tweet_scores[id] += 5
                        else:
                            tweet_scores[id] += 1
        # return step
        scores = {}
        for id in users:
            scores[id] = retweet_scores[id] + tweet_scores[id] * gamma
        return scores
