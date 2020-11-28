from src.dao.user.setter.user_setter import UserSetter
from src.dao.user.setter.mongo_user_setter import MongoUserSetter
from src.dao.user.getter.user_getter import UserGetter
from src.dao.user.getter.mongo_user_getter import MongoUserGetter
from src.shared.mongo import get_collection_from_config
from typing import Dict

class UserDAOFactory():
    def create_setter(users: Dict) -> UserSetter:
        user_setter = None
        if users["type"] == "Mongo":
            user_setter = MongoUserSetter()
            collection = get_collection_from_config(users["config"])
            user_setter.set_user_collection(collection)
        else:
            raise Exception("Datastore type not supported")

        return user_setter

    def create_getter(users: Dict) -> UserGetter:
        user_getter = None
        if users["type"] == "Mongo":
            user_getter = MongoUserGetter()
            collection = get_collection_from_config(users["config"])
            user_getter.set_user_collection(collection)
        else:
            raise Exception("Datastore type not supported")

        return user_getter
