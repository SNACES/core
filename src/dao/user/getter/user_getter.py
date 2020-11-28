from typing import List, Dict
from src.model.user import User

class UserGetter:
    def get_user_by_id(self, user_id: str):
        raise NotImplementedError("Subclasses should implement this")

    def get_users_by_id_list(self, id_list: List[str]):
        return [self.get_user_by_id(id) for id in id_list]

    def get_user_by_screen_name(self, screen_name: str):
        raise NotImplementedError("Subclasses should implement this")

    def get_users_by_screen_name_list(self, screen_name_list: List[str]):
        return [self.get_user_by_id(screen_name) for screen_name in screen_name_list]
