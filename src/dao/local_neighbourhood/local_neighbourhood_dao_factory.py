from src.dao.local_neighbourhood.setter.local_neighbourhood_setter import LocalNeighbourhoodSetter
from src.dao.local_neighbourhood.setter.mongo_local_neighbourhood_setter import MongoLocalNeighbourhoodSetter
from src.dao.local_neighbourhood.getter.local_neighbourhood_getter import LocalNeighbourhoodGetter
from src.dao.local_neighbourhood.getter.mongo_local_neighbourhood_getter import MongoLocalNeighbourhoodGetter
from src.shared.mongo import get_collection_from_config
from typing import Dict


class LocalNeighbourhoodDAOFactory():
    def create_getter(config: Dict) -> LocalNeighbourhoodGetter:
        local_neighbourhood_getter = None
        if config["type"] == "Mongo":
            local_neighbourhood_getter = MongoLocalNeighbourhoodGetter()
            collection = get_collection_from_config(config["config"])
            local_neighbourhood_getter.set_collection(collection)
        else:
            raise Exception("Datastore type not supported")

        return local_neighbourhood_getter

    def create_setter(config: Dict) -> LocalNeighbourhoodSetter:
        local_neighbourhood_setter = None
        if config["type"] == "Mongo":
            local_neighbourhood_setter = MongoLocalNeighbourhoodSetter()
            collection = get_collection_from_config(config["config"])
            local_neighbourhood_setter.set_collection(collection)
        else:
            raise Exception("Datastore type not supported")

        return local_neighbourhood_setter
