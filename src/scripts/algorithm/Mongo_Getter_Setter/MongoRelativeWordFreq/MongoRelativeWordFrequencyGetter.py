class MongoRelativeWordFrequencyGetter():
    def __init__(self):
        self.collection = None

    def set_collection(self, collection) -> None:
        self.collection = collection

    def get_relative_word_frequency(self, cluster_num: int, base_user:str, clustering_type: str, params=None):
        all_word_frequency = None
        if params is None:
            all_word_frequency = self.collection.find({}, {"user": 1,"relative_word_frequency_vector":1})
        else:
            all_word_frequency = self.collection.find({}, {"user": 1,"relative_word_frequency_vector":1, params: 1})

        user_to_rwf = {}
        for item in all_word_frequency:
            user_to_rwf[item["user"]] = item["relative_word_frequency_vector"]

        return user_to_rwf

