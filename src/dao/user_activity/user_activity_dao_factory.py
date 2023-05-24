from src.dao.user_activity.getter.mongo_user_activity_getter import MongoActivityGetter
from src.dao.user_activity.getter.user_activity_getter import ActivityGetter
from src.shared.mongo import get_collection_from_config
from typing import Dict

class UserActivityDAOFactory():
    def create_getter(selected_activity_getter, user_activity) -> ActivityGetter:
        activity_getter = MongoActivityGetter(selected_activity_getter, user_activity)

        return activity_getter
