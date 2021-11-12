from typing import List


class FollowerGetter:
    def get_follower_by_id(self, user_id: str):
        raise NotImplementedError("Subclasses should implement this")

    def get_follower_by_id_list(self, id_list: List[str]):
        return [self.get_follower_by_id(id) for id in id_list]
