class MongoUserNeighborhoodGetter():
    def __init__(self):
        self.collection = None

    def set_collection(self, collection) -> None:
        self.collection = collection

    def get_user_neighbourhood(self, base_user: str, params=None):
        all_users = None
        if params is None:
            all_users = self.collection.find({}, {'user': 1, "friends":1})
        else:
            all_users = self.collection.find({}, {'user': 1, "friends":1, params: 1})
        
        user_friends = None
        all_dict = {}
        for item in all_users:
            all_dict[item["user"]] = item["friends"]
            if item["user"] == base_user:
                user_friends = item["friends"]

        return user_friends, all_dict

    def get_user_wordcount(self, params=None):
        user_word_count_vc = None
        if params is None:
            user_word_count_vc = self.collection.find({}, {'User': 1, "UserWordFreqVector":1})
        else:
            user_word_count_vc = self.collection.find({}, {'User': 1, "UserWordFreqVector":1, params: 1})
        all_user_wc = {}
        for item in user_word_count_vc:
            all_user_wc[item["user"]] = item["friends"]
        return all_user_wc