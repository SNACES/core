from typing import List
from src.dao.user_follower.setter.follower_setter import FollowerSetter

class MongoFollowerSetter(FollowerSetter):
    def __init__(self):
        self.follower_collection = None

    def set_follower_collection(self, follower_collection: str) -> None:
        self.follower_collection = follower_collection

    def store_followers(self, a: str, b: str, a_follow_b, b_follow_a):
        doc = {"user_a": a, "user_b": b, "a_follow_b": a_follow_b, "b_follow_a": b_follow_a}
        #TODO: replace if contains
        if not self._contains_user(a, b):
            self.follower_collection.insert_one(doc)

    def _contains_user(self, user_id: str, follower_id: str) -> bool:
        a = self.follower_collection.find_one({"user_a": user_id, "user_b": follower_id})
        b = self.follower_collection.find_one({"user_a": follower_id, "user_b": user_id})
        return (a is not None) or (b is not None)
