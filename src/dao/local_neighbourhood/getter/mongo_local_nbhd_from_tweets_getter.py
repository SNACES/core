from src.dao.local_neighbourhood.getter.local_neighbourhood_getter import LocalNeighbourhoodGetter
from src.model.local_neighbourhood import LocalNeighbourhood
from typing import Dict
import bson


class MongoLocalNbhdFromTweetsGetter():
    def __init__(self):
        self.collection = None

    def set_collection(self, collection) -> None:
        self.collection = collection

    def get_local_neighbourhood(self, seed_id: str, params=None):
        doc = None
        if params is None:
            doc = self.collection.find_one({"seed_id": bson.int64.Int64(seed_id)})
        else:
            doc = self.collection.find_one({
                "seed_id": bson.int64.Int64(seed_id),
                "params": params})
        return LocalNeighbourhood.fromDict(doc)
