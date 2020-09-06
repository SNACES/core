from src.shared.utils import get_unique_list

class UserFriendsMongoSetDAO:
    def __init__(self):
        self.user_friends_by_name_collection = None
        self.user_friends_by_id_collection = None

    def store_friends_by_screen_name(self, screen_name, friends):
        self._store_friends(screen_name, friends, self.user_friends_by_name_collection)

    def store_friends_by_id(self, id, friends):
        self._store_friends(id, friends, self.user_friends_by_id_collection)

    def _store_friends(self, user, friends, collection):
        user_doc = collection.find_one({
            'user': user
        })

        if user_doc:
            # Update
            user_doc['friends'] += friends
            user_doc['friends'] = get_unique_list(user_doc['friends'])
            collection.replace_one({
                'user': user
            }, user_doc)
        else:
            # Add new entry
            collection.insert_one({
                'user': user,
                'friends': friends
            }) 