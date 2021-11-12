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
        doc = self.follower_collection.find_one({"user_id": bson.int64.Int64(user_id)})
        return doc["follower_ids"]

