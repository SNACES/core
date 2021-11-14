from typing import List

import bson
from typing import List

from src.dao.user_follower.getter.follower_getter import FollowerGetter


class MongoFollowerGetter(FollowerGetter):
    def __init__(self):
        self.follower_collection = None

    def set_follower_collection(self, follower_collection: str) -> None:
        self.follower_collection = follower_collection

    def get_follower_by_id(self, user_id: str) -> List[str]:
        follower_list = self.follower_collection.find({"user_id": bson.int64.Int64(user_id)})

        followers = []
        for doc in follower_list:
            followers.append(doc["follower_id"])
        return followers
    def get_friendship_by_id(self, a: str, b:str) :
        friendship = self.follower_collection.find({"user_a": bson.int64.Int64(a), "user_a": bson.int64.Int64(b)})
        return friendship["a_follow_b"], friendship["b_follow_a"]
