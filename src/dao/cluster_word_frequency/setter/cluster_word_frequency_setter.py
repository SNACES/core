from typing import List, Dict
from src.model.cluster_word_frequency_vector import ClusterWordFrequencyVector

class ClusterWordFrequencySetter:
    """
    An abstract class representing an object that stores a clusters word frequency vector in a datastore
    """

    def store_cluster_word_frequency_vector(self, user_ids:List[str], cluster_word_freq_vc: Dict):
        raise NotImplementedError("Subclasses should implement this")