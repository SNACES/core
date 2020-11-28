from typing import List, Dict
import bson
from src.model.user import User
from src.dao.user.getter.user_getter import UserGetter

class MongoUserGetter(UserGetter):
    def __init__(self):
        self.user_collection = None

    def set_user_collection(self, user_collection: str) -> None:
        self.user_collection = user_collection

    def get_user_by_id(self, user_id: str) -> User:
        return User.fromDict(self.user_collection.find_one({"id": bson.int64.Int64(user_id)}))

    def get_user_by_screen_name(self, screen_name: str) -> User:
        return User.fromDict(self.user_collection.find_one({"screen_name": screen_name}))
