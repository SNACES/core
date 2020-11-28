from typing import List, Dict
from src.model.user import User

class UserSetter:
    """
    An abstract class representing an object that stores users in a datastore
    """

    def store_user(self, user: User):
        raise NotImplementedError("Subclasses should implement this")

    def store_users(self, users: List[User]):
        for user in users:
            self.store_user(user)
