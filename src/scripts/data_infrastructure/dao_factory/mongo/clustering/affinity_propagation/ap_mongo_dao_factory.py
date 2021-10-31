from src.shared.mongo import get_collection_from_config
from src.data_infrastructure.datastore.mongo.cluster.affinity_propagation.aff_prop_mongo_set import AffinityPropagationMongoSetDAO
from src.data_infrastructure.datastore.mongo.cluster.affinity_propagation.aff_prop_mongo_get import AffinityPropagationMongoGetDAO

class AffinityPropagationMongoDAOFactory:
    def create_setter(self, ap_config):
        return self._create_ap_dao(ap_config, True)

    def create_getter(self, ap_config):
        return self._create_ap_dao(ap_config, False)

    def _create_ap_dao(self, ap_config, is_setter):
        ap_mongo_dao = AffinityPropagationMongoSetDAO() if is_setter else AffinityPropagationMongoGetDAO()
        ap_cluster_config = ap_config['Cluster']
        
        if ap_cluster_config:
            ap_mongo_dao.clusters_collection = get_collection_from_config(ap_cluster_config)
        else:
            ap_mongo_dao = None
        
        return ap_mongo_dao
        
