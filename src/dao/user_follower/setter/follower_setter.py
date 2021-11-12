from typing import List

class FollowerSetter:
    """
    An abstract class representing an object that stores all of a users
    followers in a datastore
    """

    def store_followers(self, user_id:str, followers_ids: List[str]):
        raise NotImplementedError("Subclasses should implement this")
