import sys
sys.path.append('../Concrete-DAO')

import yaml
from mongoDAO import *
from tweepyDAO import *


class DAOConfig():
    def __init__(self, DAO_config_yaml):
        self.ds_type = DAO_config_yaml['type']
        self.ds_name = DAO_config_yaml['datastore-name']
        self.project_name = DAO_config_yaml['project-name']
        self.ds_location = DAO_config_yaml['location']
        self.collection_name = DAO_config_yaml['collection-name']

"""
Create input and output DAO objects.
"""
class DAOFactory():
    def __init__(self):
        self._initialize_DAO_constructors()

    def _initialize_DAO_constructors(self):
        self.input_DAO_constructors = {
            "Tweepy": TweepyDAO,
            "MongoDB": MongoInputDAO
        }

        self.output_DAO_constructors = {
            "MongoDB": MongoOutputDAO
        }

    def create_DAOs(self, init_path: str) -> (dict, dict):
        """
        Return input and output datastore dictionaries, generated based 
        on syntactically valid initial configurations located at init_path.
        """
        with open(init_path, 'r') as stream:
            try:
                parsed_DS_init = yaml.safe_load(stream)
                # print(parsed_DS_init)
                input_datastore_interfaces = self._get_DAOs(parsed_DS_init['input-datastores'], self.input_DAO_constructors)
                output_datastore_interfaces = self._get_DAOs(parsed_DS_init['output-datastores'], self.output_DAO_constructors)

                return input_datastore_interfaces, output_datastore_interfaces
            except yaml.YAMLError as exc:
                print(exc)

    def _get_DAOs(self, datastores_config, DAO_constructors):
        result = {}
        for datastore_config_id in datastores_config:
            datastore_config_yaml = datastores_config[datastore_config_id]
            DAO_config = DAOConfig(datastore_config_yaml)    
            datastore_interface = self._get_DAO(DAO_config, DAO_constructors)
            result[DAO_config.collection_name] = datastore_interface

        return result

    def _get_DAO(self, DAO_config, DAO_constructors):
        ds_type = DAO_config.ds_type
        
        try:
            DAO_constructor = DAO_constructors[ds_type]
        except:
            raise Exception('Invalid Data Store type')

        if (ds_type == 'MongoDB'):
            mongo_database_name = "{0}-{1}".format(DAO_config.project_name, DAO_config.ds_name)
            return DAO_constructor(DAO_config.ds_location, mongo_database_name, DAO_config.collection_name)
        elif (ds_type == 'Tweepy'):
            return DAO_constructor()

