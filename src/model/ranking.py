from typing import List, Dict, Optional
from copy import deepcopy


class Ranking():
    """
    A class which represents a ranking
    """

    def __init__(self, seed_id: str, ids: List[str], ranking_function: str, params: Optional[Dict] = None):
        self.seed_id = seed_id
        self.ids = ids
        # if params is None:
        #     self.params = {}
        # else:
        #     self.params = deepcopy(params)
        self.params = ranking_function

        # self.params["ranking_function"] = ranking_function

    def fromDict(dict: Dict):
        seed_id = dict["seed_id"]
        ids = dict["ids"]
        params = dict["params"]

        ranking = Ranking(seed_id, ids, params)

        return ranking

    def get_top_user_id(self):
        return self.ids[0]

    def get_top_10_user_ids(self):
        return self.ids[:10]

    def get_top_20_user_ids(self):
        return self.ids[:20]

    def get_top_30_user_ids(self):
        return self.ids[:30]

    def get_top_50_user_ids(self):
        return self.ids[:50]

    def get_all_ranked_user_ids(self):
        return self.ids
