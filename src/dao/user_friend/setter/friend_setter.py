from typing import List, Dict
from src.model.user import User

class FriendSetter:
    """
    An abstract class representing an object that stores all of a users
    friends in a datastore
    """

    def store_friends(self, user_id: str, friends_ids: List[str]):
        raise NotImplementedError("Subclasses should implement this")
