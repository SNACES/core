from src.shared.lib import get_unique_list

class UserFollowersMongoSetDAO:
    def __init__(self):
        self.user_followers_by_name_collection = None
        self.user_followers_by_id_collection = None

    def store_followers_by_screen_name(self, screen_name, followers_users_screen_name):
        self._store_followers(screen_name, followers_users_screen_name, self.user_followers_by_name_collection)

    def store_followers_by_id(self, id, followers_users_ID):
        self._store_followers(id, followers_users_ID, self.user_followers_by_id_collection)

    def _store_followers(self, user, followers, collection):
        user_doc = collection.find_one({
            'user': user
        })

        if user_doc:
            # Update
            user_doc['user_followers'] += followers
            user_doc['user_followers'] = get_unique_list(user_doc['user_followers'])
            collection.replace_one({
                'user': user
            }, user_doc)
        else:
            # Add new entry
            collection.insert_one({
                'user': user,
                'user_followers': followers
            })         