class UserFriendsMongoGetDAO:
    def __init__(self):
        self.user_friends_by_name_collection = None
        self.user_friends_by_id_collection = None
    
    def get_friends_by_name(self, user):
        user_friends_doc = self.user_friends_by_name_collection.find_one({'user': user})
   
        return user_friends_doc['friends'] if user_friends_doc else None
    
    def get_friends_by_id(self, user):
        user_friends_doc = self.user_friends_by_id_collection.find_one({'user': user})
   
        return user_friends_doc['friends'] if user_friends_doc else None