from src.data_cleaning.DAOFactory.MongoUserNeighborhoodGetter import MongoUserNeighborhoodGetter
from src.data_cleaning.DAOFactory.MongoUserNeighborhoodSetter import MongoUserNeighborhoodSetter
from typing import Dict, List
from src.shared.mongo import get_collection_from_config


class FriendsCleaningDAOFactory():
    def create_getter(config: Dict):
        user_neighbourhood_getter = None
        if config["type"] == "Mongo":
            user_neighbourhood_getter = MongoUserNeighborhoodGetter()
            collection = get_collection_from_config(config["config"])
            user_neighbourhood_getter.set_collection(collection)
        else:
            raise Exception("Datastore type not supported")

        return user_neighbourhood_getter

    def create_wordcount_getter(config: Dict):
        user_wordcount_getter = None
        if config["type"] == "Mongo":
            user_wordcount_getter = MongoUserNeighborhoodGetter()
            collection = get_collection_from_config(config["config"])
            user_wordcount_getter.set_collection(collection)
        else:
            raise Exception("Datastore type not supported")

        return user_wordcount_getter    

    def create_setter(config: Dict):
        user_neighbourhood_setter = None
        if config["type"] == "Mongo":
            user_neighbourhood_setter = MongoUserNeighborhoodSetter()
            collection = get_collection_from_config(config["config"])
            user_neighbourhood_setter.set_collection(collection)
        else:
            raise Exception("Datastore type not supported")

        return user_neighbourhood_setter


