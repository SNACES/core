from src.shared.mongo import get_collection_from_config
from src.data_infrastructure.datastore.mongo.word_frequency.wf_mongo_set import WordFrequencyMongoSetDAO
from src.data_infrastructure.datastore.mongo.word_frequency.wf_mongo_get import WordFrequencyMongoGetDAO

class WordFrequencyMongoDAOFactory:
    """
    A class that generates WordFrequency getter and setter.
    """
    def create_setter(self, wf_config):
        """
        Create a WordFrequencySetDAO with the config file.

        @param wf_config: the path of config file
        @return: a required WordFrequencySetDAO
        """
        return self._create_wf_dao(wf_config, True)

    def create_getter(self, wf_config):
        """
        Create a WordFrequencyGetDAO with the config file.

        @param wf_config: the path of config file
        @return: a required WordFrequencyGetDAO
        """
        return self._create_wf_dao(wf_config, False)

    def _create_wf_dao(self, wf_config, is_setter):
        """
        Create a WordFrequency getter or setter as required. 
        For a getter dao, get the required data collection from MongoDB.
        For a setter dao, set the data collection into MongoDB.

        @param wf_config: path of the config file
        @param is_setter: True if WordFrequenceDao setter is required
        @return: a WordFrequencyDAO getter or a WordFrequenctDAO setter
        """
        wf_mongo_dao = WordFrequencyMongoSetDAO() if is_setter else WordFrequencyMongoGetDAO()

        global_wcv_config = wf_config['Global-Word-Count'] if 'Global-Word-Count' in wf_config else None
        user_wcv_config = wf_config['User-Word-Count'] if 'User-Word-Count' in wf_config else None
        global_wfv_config = wf_config['Global-Word-Frequency'] if 'Global-Word-Frequency' in wf_config else None
        user_wfv_config = wf_config['User-Word-Frequency'] if 'User-Word-Frequency' in wf_config else None
        user_rwfv_config = wf_config['Relative-User-Word-Frequency'] if 'Relative-User-Word-Frequency' in wf_config else None
        gen_new_collection = True

        if global_wcv_config:
            wf_mongo_dao.global_word_count_vector_collection = get_collection_from_config(global_wcv_config)
            # # uncomment if create a new collection 
            # wf_mongo_dao.global_word_count_vector_collection = get_collection_from_config(global_wcv_config ,gen_new_collection)

        if user_wcv_config:
            wf_mongo_dao.user_word_count_vector_collection = get_collection_from_config(user_wcv_config)
        
        if global_wfv_config:
            wf_mongo_dao.global_word_frequency_vector_collection = get_collection_from_config(global_wfv_config)
        
        if user_wfv_config:
            wf_mongo_dao.user_word_frequency_vector_collection = get_collection_from_config(user_wfv_config)

        if user_rwfv_config:
            wf_mongo_dao.relative_user_word_frequency_vector_collection = get_collection_from_config(user_rwfv_config)

        if not global_wcv_config and not user_wcv_config and not global_wfv_config and not user_wfv_config and not user_rwfv_config:
            wf_mongo_dao = None

        return wf_mongo_dao

        

        

