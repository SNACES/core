

class RetweetsRanker():
    def __init__(self, cluster_getter, raw_tweet_getter):
        self.cluster_getter = cluster_getter
        self.raw_tweet_getter = raw_tweet_getter

    def rank(self, seed_id, params):
        clusters = self.cluster_getter.get_clusters(seed_id, params)

        cluster = clusters[0]
        user_ids = cluster.users

        scores = {}
        for id in user_ids:
            retweets = self.raw_tweet_getter.get_retweets_of_user_by_user_id(id)

            count = 0
            for retweet in retweets:
                if str(retweet.user_id) in user_ids:
                    count += 1

            scores[id] = count

        ranking = list(sorted(scores, key=scores.get))
        print(ranking)
        print(scores)
        return ranking
