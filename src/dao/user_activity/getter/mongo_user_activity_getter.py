from typing import List
from src.dao.user_activity.getter.user_activity_getter import ActivityGetter

class MongoActivityGetter():
    def __init__(self, activity_getter, user_activity) -> None:
        self.activity_getter = activity_getter
        self.user_activity = user_activity

    def get_user_activities(self, user_id: str) -> List[str]:
        if self.user_activity == 'friends':
            # self.activity_getter = MongoFriendGetter()
            return self.activity_getter.get_user_friends_ids(user_id)
        elif self.user_activity == 'user retweets':
            # self.activity_getter = MongoRetweetedUsersGetter()
            return self.activity_getter.get_retweet_users_ids(user_id)
        elif self.user_activity == 'user retweets ids':
            # self.activity_getter = MongoRawTweetGetter()
            return self.activity_getter.get_retweets_ids_by_user_id(user_id)