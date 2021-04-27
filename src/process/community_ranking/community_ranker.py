from typing import List


class CommunityRanker():
    def rank(self, user_ids:List, current_community: List):
        scores = self.score_users(user_ids, current_community)

        ranked_ids = list(sorted(scores, key=scores.get, reverse=True))
        return ranked_ids

    def score_users(self, user_ids: List[str], current_community: List):
        raise NotImplementedError("This method should be implemented by subclasses")