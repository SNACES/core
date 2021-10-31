class UserFollowersMongoGetDAO:
    def __init__(self):
        self.user_followers_by_name_collection = None
        self.user_followers_by_id_collection = None

    def get_followers_by_name(self, user):
        user_followers_doc = self.user_followers_by_name_collection.find_one({'user': user})
   
        return user_followers_doc['user_followers'] if user_followers_doc else None
    
    def get_followers_by_id(self, user):
        user_followers_doc = self.user_followers_by_id_collection.find_one({'user': user})
   
        return user_followers_doc['user_followers'] if user_followers_doc else None
