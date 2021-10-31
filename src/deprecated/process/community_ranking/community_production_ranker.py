from src.process.community_ranking.community_ranker import CommunityRanker
from typing import List
from tqdm import tqdm


class CommunityProductionRanker(CommunityRanker):
    def __init__(self, raw_tweet_getter):
        self.raw_tweet_getter = raw_tweet_getter
        self.ranking_function_name = "retweets"

    def score_users(self, user_ids: List[str], current_community: List):
        scores = {}
        for id in user_ids:
            scores[id] = 0

        for id in tqdm(user_ids):
            retweets = self.raw_tweet_getter.get_retweets_of_user_by_user_id(id)
            if len(retweets) < 1:
                scores[id] = 0
                continue
            # coeffcient = self.raw_tweet_getter.get_tweet_scale_coefficient(id)
            for retweet in retweets:
                if (str(retweet.user_id) in current_community) or (int(retweet.user_id) in current_community):
                    if int(retweet.user_id) != int(id):
                        scores[id] += 1
            # scores[id] *= coeffcient
        return scores