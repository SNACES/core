import yaml
import mongoDS, tweepyDS

# init location is the path to a syntatically valid yaml per specification
# return input datastores dict and output datastores dict
def DSGenerator(init_path):
    with open(init_path, 'r') as stream:
        try:
            parsed_DS_init = yaml.safe_load(stream)
            # print(parsed_DS_init)
            input_datastore_interfaces = _get_datastores_interfaces(parsed_DS_init['input-datastores'])
            output_datastore_interfaces = _get_datastores_interfaces(parsed_DS_init['output-datastores'])

            return input_datastore_interfaces, output_datastore_interfaces
        except yaml.YAMLError as exc:
            print(exc)

def _get_datastores_interfaces(datastores_config):
    # print(datastores_config)
    result = {}
    for datastore_config_id in datastores_config:
        datastore_config = datastores_config[datastore_config_id]
        
        # maybe can objectify this
        ds_type = datastore_config['type']
        ds_name = datastore_config['datastore-name']
        project_name = datastore_config['project-name']
        ds_location = datastore_config['location']
        
        datastore_interface = _get_datastore_interface(ds_type, project_name, ds_name, ds_location)
        result[ds_name] = datastore_interface

    return result

def _get_datastore_interface(ds_type, project_name, ds_name, ds_location):
    if (ds_type == 'MongoDB'):
        mongo_database_name = "{0}-{1}".format(project_name, ds_name)
        return mongoDS.MongoDS(ds_location, mongo_database_name)
    elif (ds_type == 'Tweepy'):
        return tweepyDS.TweepyDS()
    else:
        raise Exception('Invalid DataStore type')

print(DSGenerator("init-algo.yaml"))