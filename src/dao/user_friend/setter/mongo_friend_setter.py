from typing import List, Dict
import bson
from src.model.user import User
from src.dao.user_friend.setter.friend_setter import FriendSetter


class MongoFriendSetter(FriendSetter):
    def __init__(self):
        self.friend_collection = None

    def set_friend_collection(self, friend_collection: str) -> None:
        self.friend_collection = friend_collection

    def store_friends(self, user_id: str, friends_ids: List[str]):
        doc = {"user_id": bson.int64.Int64(user_id), "friends_ids": friends_ids}

        if self._contains_user(user_id):
            self.friend_collection.find_one_and_replace({"user_id": bson.int64.Int64(user_id)}, doc)
        else:
            self.friend_collection.insert_one(doc)

    def _contains_user(self, user_id: str) -> bool:
        return self.friend_collection.find_one({"user_id": bson.int64.Int64(user_id)}) is not None
