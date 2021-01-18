from typing import Union, List, Dict
from src.model.word_frequency_vector import WordFrequencyVector
from src.model.user_word_frequency_vector import UserWordFrequencyVector
from src.model.cluster_word_frequency_vector import ClusterWordFrequencyVector
from copy import deepcopy


class ClusterWordFrequencyProcessor():
    """
    Process and store a clusters word frequency
    """

    def __init__(self, user_word_frequency_vector_getter, cluster_word_frequency_vector_getter, 
                 cluster_word_frequency_vector_setter, global_word_frequency_vector_getter):
        self.user_word_frequency_vector_getter = user_word_frequency_vector_getter
        self.cluster_word_frequency_vector_getter = cluster_word_frequency_vector_getter
        self.cluster_word_frequency_vector_setter = cluster_word_frequency_vector_setter
        self.global_word_frequency_vector_getter = global_word_frequency_vector_getter

    def process_cluster_word_frequency_vector(self, ids: List[str]):
        cluster_word_frerquency_dict = {}
        for id in ids:
            user_word_frequency_vector = self.user_word_frequency_vector_getter.get_user_word_frequency_by_id(id)
            cluster_word_frequency_dict = self._merge_word_count(user_word_frequency_vector, cluster_word_frequency_dict)
        # cluster_words = self.cluster_word_frequency_vector_getter.get_cluster_word_frequency_vector(ids)
        self.cluster_word_frequency_vector_setter.store_cluster_word_frequency_vector(ids, cluster_word_frequency_dict)     

    def process_relative_cluster_word_frequency(self, ids: List[str]):
        cluster_word_frequency_vc = self.cluster_word_frequency_vector_getter.get_cluster_word_frequency_by_ids(ids).get_words()
        global_word_count_vc = self.global_word_frequency_vector_getter.get_global_word_frequency()

        relative_cluster_word_frequency = self._gen_relative_cluster_word_frequency(cluster_word_frequency_vc, global_word_count_vc)
        self.cluster_word_frequency_vector_setter.store_relative_user_word_frequency_vector(ids, relative_cluster_word_frequency)

    def _gen_relative_cluster_word_frequency(self, user_relative_word_count, global_word_count):
        merge_count = self._merge_word_count(user_relative_word_count, global_word_count)
        user_word_frequency = self._gen_word_frequency(user_relative_word_count)
        global_word_frequency =self._gen_word_frequency(merge_count)

        for words in user_word_frequency:
            user_word_frequency[words] = user_word_frequency[words] / global_word_frequency[words]
        return user_word_frequency

    def _gen_word_frequency(self, word_counts: Dict):
        word_count = deepcopy(word_counts)
        total_count = sum(word_count.values())
        for words in word_count:
            word_count[words] = word_count[words] / total_count
        return word_count
    
    def _merge_word_count(self, user_word_count, global_word_counts):
        global_word_count = deepcopy(global_word_counts)
        for words in user_word_count:
            if words in global_word_count:
                global_word_count[words] += user_word_count[words]
            else:
                global_word_count[words] = user_word_count[words]
        return global_word_count
