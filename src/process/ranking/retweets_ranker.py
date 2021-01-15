from src.model.ranking import Ranking
from src.process.ranking.ranker import Ranker
from typing import List


class RetweetsRanker(Ranker):
    def __init__(self, cluster_getter, raw_tweet_getter, ranking_setter):
        self.cluster_getter = cluster_getter
        self.raw_tweet_getter = raw_tweet_getter
        self.ranking_setter = ranking_setter
        self.ranking_function_name = "retweets"

    def rank(self, user_ids: List[str]):
        scores = {}
        for id in user_ids:
            retweets = self.raw_tweet_getter.get_retweets_of_user_by_user_id(id)

            count = 0
            for retweet in retweets:
                if str(retweet.user_id) in user_ids:
                    count += 1

            scores[id] = count
        result = {k: v for k, v in sorted(scores.items(), key=lambda item: item[1], reverse= True)}
        self.ranking_setter.store_ranking(user_ids, result)

        return result
