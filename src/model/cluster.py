from typing import List, Dict


class Cluster():
    """
    A class which represents a cluster
    """

    def __init__(self, base_user: str, users: List[str]):
        self.base_user = base_user

        if base_user not in users:
            users = [base_user] + users
        self.users = users

    def fromDict(dict: Dict):
        base_user = dict["base_user"]
        users = dict["users"]

        cluster = Cluster(base_user, users)

        return cluster
