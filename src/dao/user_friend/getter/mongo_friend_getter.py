from typing import List, Dict
import bson
from src.model.user import User
from src.dao.user_friend.getter.friend_getter import FriendGetter
import MACROS


class MongoFriendGetter(FriendGetter):
    def __init__(self):
        self.friend_collection = None

    def set_friend_collection(self, friend_collection: str) -> None:
        self.friend_collection = friend_collection

    def get_user_friends_ids(self, user_id: str) -> List[str]:
        if user_id not in MACROS.FRIENDS:
            doc = self.friend_collection.find_one({"user_id": bson.int64.Int64(user_id)})
            if doc is not None:
                MACROS.FRIENDS[user_id] = doc["friends_ids"]
            else:
                MACROS.FRIENDS[user_id] = None
        return MACROS.FRIENDS[user_id]

    def contains_user(self, user_id: str) -> bool:
        return self.friend_collection.find_one({"user_id": bson.int64.Int64(user_id)}) is not None
