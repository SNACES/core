import yaml

class ConfigParser():    
    def __init__(self, config_path: str):
        self.config_path = config_path

    def create_getter_DAOs(self):
        """
        Return appropriate getter DAO objects, generated based 
        on syntactically valid initial configurations located at init_path.
        """
        with open(self.config_path, 'r') as stream:
            try:
                parsed_DS_config = yaml.safe_load(stream)
                return self.get_getters(parsed_DS_config['input-datastore'])
            except yaml.YAMLError as exc:
                print(exc)

    def create_setter_DAOs(self):
        """
        Return appropriate setter DAO objects, generated based 
        on syntactically valid initial configurations located at init_path.
        """
        with open(self.config_path, 'r') as stream:
            try:
                parsed_DS_config = yaml.safe_load(stream)
                return self.get_setters(parsed_DS_config['output-datastore'])
            except yaml.YAMLError as exc:
                print(exc)
        
    def get_getters(self, parsed_getter_config):
        raise NotImplementedError
    
    def get_setters(self, parsed_setter_config):
        raise NotImplementedError
