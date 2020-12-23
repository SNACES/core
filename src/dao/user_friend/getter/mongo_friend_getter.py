from typing import List, Dict
import bson
from src.model.user import User
from src.dao.user_friend.getter.friend_getter import FriendGetter

class MongoFriendGetter(FriendGetter):
    def __init__(self):
        self.friend_collection = None

    def set_friend_collection(self, friend_collection: str) -> None:
        self.friend_collection = friend_collection

    def get_user_friends_ids(self, user_id: str) -> List[str]:
        doc = self.friend_collection.find_one({"user_id": bson.int64.Int64(user_id)})
        if doc is not None:
            return doc["friends_ids"]
        else:
            return None
