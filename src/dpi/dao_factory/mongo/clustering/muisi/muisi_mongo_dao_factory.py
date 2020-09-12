from src.shared.mongo import get_collection_from_config
from src.dpi.datastore.mongo.word_frequency.wf_mongo_get import WordFrequencyMongoGetDAO
from src.dpi.datastore.mongo.cluster.MUISI.standard.muisi_mongo_set import MUISIMongoSetDAO
from src.dpi.datastore.mongo.cluster.MUISI.standard.muisi_mongo_get import MUISIMongoGetDAO
from src.dpi.datastore.mongo.cluster.MUISI.retweets.muisi_retweets_mongo_set import MUISIRetweetsMongoSetDAO
from src.dpi.datastore.mongo.cluster.MUISI.retweets.muisi_retweets_mongo_get import MUISIRetweetsMongoGetDAO

class MUISIMongoDAOFactory:
    def create_setter(self, muisi_config):
        return self._create_muisi_dao(muisi_config, True)

    def create_getter(self, muisi_config):
        return self._create_muisi_dao(muisi_config, False)

    def _create_muisi_dao(self, muisi_config, is_setter):
        # Check whether retweets mode is set in config
        is_retweets_mode = muisi_config['is-retweets-mode']
        if is_retweets_mode:
            muisi_mongo_dao = MUISIRetweetsMongoSetDAO() if is_setter else MUISIRetweetsMongoGetDAO()
        else:
            muisi_mongo_dao = MUISIMongoSetDAO() if is_setter else MUISIMongoGetDAO()

        muisi_cluster_config = muisi_config['Cluster']
        if muisi_cluster_config:
            if is_retweets_mode:
                muisi_mongo_dao.muisi_retweets_cluster_collection = get_collection_from_config(muisi_cluster_config)
            else:
                muisi_mongo_dao.muisi_cluster_collection = get_collection_from_config(muisi_cluster_config)
        else:
            muisi_mongo_dao = None

        return muisi_mongo_dao