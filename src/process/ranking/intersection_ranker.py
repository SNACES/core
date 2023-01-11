from typing import List


class IntersectionRanker:
    def __init__(self, ranker_list):
        self.ranker_list = ranker_list
        self.ranking_function_name = "intersection"

    def rank(self, user_list: List[str]):
        ranks = []
        for ranker in self.ranker_list:
            scores = ranker.score_users(user_list)
            ranks.append(sorted(scores.keys(), key=scores.get, reverse=True))
        ranking = {}
        # i means top i users
        for i in range(len(ranks[0])):
            # find users that are in the intersection of top i of each rank
            intersection_users = set(ranks[0][:i+1])
            for j in range(1, len(ranks)):
                intersection_users = intersection_users.intersection(
                    set(ranks[j][:i+1]))
            for user in intersection_users:
                if user not in ranking:
                    ranking[user] = i
        intersection_ranking = \
            sorted(ranking.keys(), key=ranking.get, reverse=False)
        return intersection_ranking
