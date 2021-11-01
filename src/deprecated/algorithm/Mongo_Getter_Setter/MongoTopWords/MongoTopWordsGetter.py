class MongoTopWordsGetter():
    def __init__(self):
        self.collection = None

    def set_collection(self, collection) -> None:
        self.collection = collection

    def get_top_words(self, cluster_num: int, base_user:str, cluster_type: str, params=None):
        target_top_words = None
        if params is None:
            target_top_words = self.collection.find_one({"base_user":base_user, "cluster_type":cluster_type, "cluster_num": cluster_num})
        else:
            target_top_words = self.collection.find_one({"base_user":base_user, "cluster_type":cluster_type, "cluster_num": cluster_num, "params": params})

        top_words_list = target_top_words["top_words"]

        return top_words_list

        