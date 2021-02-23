from src.process.community_ranking.community_ranker import CommunityRanker
from typing import List


class CommunityTweetsRanker(CommunityRanker):
    def __init__(self, raw_tweet_getter):
        self.raw_tweet_getter = raw_tweet_getter
        self.ranking_function_name = "tweets"

    def score_users(self, user_ids: List[str]):
        scores = {}
        for id in user_ids:
            tweets = self.raw_tweet_getter.get_tweets_by_user_id(id)

            count = 0
            for tweet in tweets:
                if str(tweet.user_id) in user_ids:
                    count += 1

            scores[id] = count

        return scores