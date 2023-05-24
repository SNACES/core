from src.dao.retweeted_users.setter.retweet_users_setter import RetweetUsersSetter
from src.dao.retweeted_users.setter.mongo_retweeted_users_setter import MongoRetweetUsersSetter
from src.dao.retweeted_users.getter.retweet_users_getter import RetweetUsersGetter
from src.dao.retweeted_users.getter.mongo_retweeted_users_getter import MongoRetweetUsersGetter
from src.shared.mongo import get_collection_from_config
from typing import Dict

class RetweetedUsersDAOFactory():
    def create_setter(friends: Dict) -> RetweetUsersSetter:
        friend_setter = None
        if friends["type"] == "Mongo":
            friend_setter = MongoRetweetUsersSetter()
            collection = get_collection_from_config(friends["config"])
            friend_setter.set_retweet_user_collection(collection)
        else:
            raise Exception("Datastore type not supported")

        return friend_setter

    def create_getter(friends: Dict) -> RetweetUsersGetter:
        friend_getter = None
        if friends["type"] == "Mongo":
            friend_getter = MongoRetweetUsersGetter()
            collection = get_collection_from_config(friends["config"])
            friend_getter.set_retweet_user_collection(collection)
        else:
            raise Exception("Datastore type not supported")

        return friend_getter
