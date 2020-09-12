import yaml

class DSConfigParser():    
    def __init__(self):
        self.mongo_dao_factory = None

    def _get_dao(self, parsed_dao_config, data_obj_name, is_setter):
        dao = None
        data_obj_config = parsed_dao_config[data_obj_name] if data_obj_name in parsed_dao_config else None

        if data_obj_config:
            if data_obj_config['type'] == "Mongo":
                mongo_dao_factory = self.mongo_dao_factory

                if is_setter:
                    dao = mongo_dao_factory.create_setter(data_obj_config)  
                else:  
                    dao = mongo_dao_factory.create_getter(data_obj_config)  
            else:
                raise Exception("Datastore type not supported")

        return dao