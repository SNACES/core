from src.process.community_ranking.community_ranker import CommunityRanker
from typing import List
from tqdm import tqdm

class CommunityConsumptionRanker(CommunityRanker):
    def __init__(self, raw_tweet_getter):
        self.raw_tweet_getter = raw_tweet_getter
        self.ranking_function_name = "tweets"

    def score_users(self, user_ids: List[str], current_community: List):
        scores = {}
        for id in user_ids:
            scores[str(id)] = 0

        for id in tqdm(user_ids):
            retweets = self.raw_tweet_getter.get_retweets_by_user_id_time_restricted(id)
            # coefficient = self.raw_tweet_getter.get_tweet_scale_coefficient(id)

            for retweet in retweets:
                if str(retweet.retweet_user_id) in current_community or int(retweet.retweet_user_id) in current_community:
                    if str(retweet.retweet_user_id) != str(id):  # retweeting your own tweet does not count
                        scores[str(id)] += 1
            # scores[str(id)] *= coefficient
        return scores