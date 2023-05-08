from src.process.ranking.ranker import Ranker
from typing import List
from tqdm import tqdm

class ConsumptionUtilityRanker(Ranker):
    def __init__(self, raw_tweet_getter, friends_getter, ranking_setter):
        self.raw_tweet_getter = raw_tweet_getter
        self.friends_getter = friends_getter
        self.ranking_setter = ranking_setter
        self.ranking_function_name = "consumption utility"

    def score_users(self, user_ids: List[str], respection: List[str]):
        scores = {}

        for user_id in user_ids:
            scores[user_id] = self.score_user(user_id, respection)

        return scores

    def score_user(self, user_id: str, user_ids: List[str]):
        if user_id not in user_ids:
            user_ids = user_ids + [user_id]

        score = 0

        retweets = self.raw_tweet_getter.get_retweets_by_user_id(user_id)

        for retweet in retweets:
            if str(retweet.retweet_user_id) in user_ids and \
                    str(retweet.retweet_user_id) != str(user_id):
                # retweeting your own tweet does not count
                score += 1

        return score / len(user_ids)
