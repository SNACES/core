from typing import List, Dict
import bson
from src.model.user import User
from src.dao.user.setter.user_setter import UserSetter


class MongoUserSetter(UserSetter):
    def __init__(self):
        self.user_collection = None

    def set_user_collection(self, user_collection: str) -> None:
        self.user_collection = user_collection

    def store_user(self, user: User) -> None:
        doc = user.__dict__

        if self._contains_user(user):
            self.user_collection.find_one_and_replace({"id": bson.int64.Int64(user.id)}, doc)
        else:
            self.user_collection.insert_one(doc)

    def _contains_user(self, user: User) -> bool:
        return self.user_collection.find_one({"id": bson.int64.Int64(user.id)}) is not None
