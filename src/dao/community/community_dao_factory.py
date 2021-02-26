from src.dao.community.setter.community_setter import CommunitySetter
from src.dao.community.setter.mongo_community_setter import MongoCommunitySetter
from src.shared.mongo import get_collection_from_config
from typing import Dict


class CommunityDAOFactory():
    def create_setter(config: Dict) -> CommunitySetter:
        community_setter = None
        if config["type"] == "Mongo":
            community_setter = MongoCommunitySetter()
            collection = get_collection_from_config(config["config"])
            community_setter.set_collection(collection)
        else:
            raise Exception("Datastore type not supported")

        return community_setter
