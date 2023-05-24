from typing import List, Dict
from src.model.user import User

class RetweetUsersSetter:
    """
    An abstract class representing an object that stores all of a users
    friends in a datastore
    """

    def store_retweet_users(self, user_id: str, friends_ids: List[str]):
        raise NotImplementedError("Subclasses should implement this")
