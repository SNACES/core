from typing import Dict, List
import json


class LocalNeighbourhood():
    """
    A class which represents a twitter local local neighbourhood
    """

    def __init__(self, seed_id: str, params, users: Dict):
        self.seed_id = seed_id
        self.params = params
        self.users = users

    def get_user_id_list(self) -> List:
        return self.users.keys()

    def get_user_friends(self, id):
        return self.users[id]

    def toJSON(self) -> str:
        """
        Returns a json corresponding to the given localNeighbourhood object

        @return a json representation of the localNeighbourhood
        """
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True,
            indent=4)

    def fromJSON(json_in: str):
        """
        Given a json representation of a local neighbourhood, return the
        local neighbourhood object

        @param json_in the json to convert to a LocalNeighbourhood

        @return the LocalNeighbourhood object
        """
        obj = json.loads(json_in)
        localNeighbourhood = LocalNeighbourhood(
            obj.get("seed_id"),
            obj.get("params"),
            obj.get("users")
        )

        return localNeighbourhood

    def fromDict(dict: Dict):
        localNeighbourhood = LocalNeighbourhood(
            dict["seed_id"], dict["params"], dict["users"]
        )

        return localNeighbourhood

    def __eq__(self, other) -> bool:
        if isinstance(other, self.__class):
            return self.__dict__ == other.__dict__
        else:
            return False

    def __ne__(self, other) -> bool:
        return not self.__eq__(other)
