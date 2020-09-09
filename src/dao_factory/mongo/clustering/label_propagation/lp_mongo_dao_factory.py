from src.shared.mongo import get_collection_from_config
from src.datastore.mongo.cluster.label_propagation.label_prop_mongo_set import LabelPropagationMongoSetDAO
from src.datastore.mongo.cluster.label_propagation.label_prop_mongo_get import LabelPropagationMongoGetDAO

class LabelPropagationMongoDAOFactory():
    def create_setter(self, lp_config):
        return self._create_lp_dao(lp_config, True)

    def create_getter(self, ap_config):
        return self._create_lp_dao(ap_config, False)

    def _create_lp_dao(self, lp_config, is_setter):
        lp_mongo_dao = LabelPropagationMongoSetDAO() if is_setter else LabelPropagationMongoGetDAO()
        ap_cluster_config = lp_config['Cluster']
        
        if ap_cluster_config:
            lp_mongo_dao.clusters_collection = get_collection_from_config(ap_cluster_config)
        else:
            lp_mongo_dao = None
        
        return lp_mongo_dao
        