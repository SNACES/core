from typing import List, Dict


class Cluster():
    """
    A class which represents a cluster
    """

    def __init__(self, base_user: str, users: List[str], params: Dict):
        self.base_user = base_user
        self.users = users
        self.params = params

    def fromDict():
        pass
