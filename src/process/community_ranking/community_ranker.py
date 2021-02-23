from typing import List


class CommunityRanker():
    def rank(self, user_ids:List, params):
        scores = self.score_users(user_ids)

        ranked_ids = list(sorted(scores, key=scores.get, reverse=True))
        return ranked_ids

    def score_users(self, user_ids: List[str]):
        raise NotImplementedError("This method should be implemented by subclasses")