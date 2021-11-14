from typing import List

class FollowerSetter:
    """
    An abstract class representing an object that stores all of a users
    followers in a datastore
    """

    def store_followers(self, user_id:str, followers_ids: str, a_follow_b, b_follow_a):
        raise NotImplementedError("Subclasses should implement this")
