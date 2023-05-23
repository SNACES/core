from src.dao.user_friend.setter.friend_setter import FriendSetter
from src.dao.user_friend.setter.mongo_friend_from_tweets_setter import MongoFriendSetter
from src.dao.user_friend.getter.friend_getter import FriendGetter
from src.dao.user_friend.getter.mongo_friend_from_tweets_getter import MongoFriendGetter
from src.shared.mongo import get_collection_from_config
from typing import Dict

class UserFriendFromTweetsDAOFactory():
    def create_setter(friends: Dict) -> FriendSetter:
        friend_setter = None
        if friends["type"] == "Mongo":
            friend_setter = MongoFriendSetter()
            collection = get_collection_from_config(friends["config"])
            friend_setter.set_friend_collection(collection)
        else:
            raise Exception("Datastore type not supported")

        return friend_setter

    def create_getter(friends: Dict) -> FriendGetter:
        friend_getter = None
        if friends["type"] == "Mongo":
            friend_getter = MongoFriendGetter()
            collection = get_collection_from_config(friends["config"])
            friend_getter.set_friend_collection(collection)
        else:
            raise Exception("Datastore type not supported")

        return friend_getter
