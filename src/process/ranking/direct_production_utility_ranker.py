from src.process.ranking.ranker import Ranker
from typing import List
from tqdm import tqdm


class ProductionUtilityRanker(Ranker):
    def __init__(self, raw_tweet_getter, friends_getter, ranking_setter):
        self.raw_tweet_getter = raw_tweet_getter
        self.user_friend_getter = friends_getter
        self.ranking_setter = ranking_setter
        self.ranking_function_name = "retweets"

    def score_users(self, user_ids: List[str]):
        scores = {}
        for user_id in user_ids:
            scores[str(user_id)] = 0

        for user_id in tqdm(user_ids):
            retweets = self.raw_tweet_getter.get_retweets_of_user_by_user_id(
                user_id)

            for retweet in retweets:
                # retweet.user_id is the user that retweeted the tweet
                # retweet.retweet_user_id is the tweet owner
                retweet_user_id = str(retweet.user_id)
                retweet_user_friends = list(
                    map(str, self.user_friend_getter.get_user_friends_ids(
                        retweet_user_id)))
                if retweet_user_id in user_ids and \
                        retweet_user_id != str(user_id) and \
                        user_id in retweet_user_friends:
                    # only count retweets that are from user's followers
                    scores[str(user_id)] += 1

        return scores

    def score_user(self, user_id, user_ids: List[str]):
        score = 0

        retweets = self.raw_tweet_getter.get_retweets_of_user_by_user_id(
            user_id)

        for retweet in retweets:
            # retweet.user_id is the user that retweeted the tweet
            # retweet.retweet_user_id is the tweet owner
            retweet_user_id = str(retweet.user_id)
            retweet_user_friends = list(
                map(str, self.user_friend_getter.get_user_friends_ids(
                    retweet_user_id)))
            if retweet_user_id in user_ids and \
                    retweet_user_id != str(user_id) and \
                    user_id in retweet_user_friends:
                # only count retweets that are from user's followers
                score += 1

        return score
