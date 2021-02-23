from src.process.community_ranking.community_ranker import CommunityRanker
from typing import List


class CommunityRetweetsRanker(CommunityRanker):
    def __init__(self, raw_tweet_getter):
        self.raw_tweet_getter = raw_tweet_getter
        self.ranking_function_name = "retweets"

    def score_users(self, user_ids: List[str]):
        scores = {}
        for id in user_ids:
            scores[id] = 0

        for id in user_ids:
            retweets = self.raw_tweet_getter.get_retweets_of_user_by_user_id(id)

            for retweet in retweets:
                if str(retweet.user_id) in user_ids:
                    scores[id] += 1

        return scores