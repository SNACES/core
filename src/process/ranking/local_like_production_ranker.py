from src.process.ranking.ranker import Ranker
from tqdm import tqdm
from typing import List

class LocalLikeProductionRanker(Ranker):
    """
        Number of times a tweet by a user has been liked by others
        in the cluster.
    """
    def __init__(self, cluster_getter, liked_tweet_getter, ranking_setter):
        self.cluster_getter = cluster_getter
        self.ranking_setter = ranking_setter
        self.liked_tweet_getter = liked_tweet_getter
        self.ranking_function_name = "local like production"

    def score_users(self, user_ids: List[str]):
        scores = {}
        for user_id in user_ids:
            scores[str(user_id)] = 0

        for user_id in tqdm(user_ids):
            # tweets that being tweeted by user_id
            liked_tweet = self.liked_tweet_getter.get_tweets_by_user_id_time_restricted(user_id)

            for liked_tweet in liked_tweet:
                # user that liked the tweet
                liked_user = liked_tweet.liked_id
                # liking your own tweet doesn't count
                if str(liked_user) in user_ids and str(liked_user) != str(user_id):
                    scores[str(user_id)] += 1
            # TODO: REMOVE THE FOLLOWING PRINT CALL
            #print(scores)
        return scores
