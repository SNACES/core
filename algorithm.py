from datastore import DataStore
import credentials
import DSGenerator

class Algorithm:
    def __init__(self, init_path, input_datastores={}, output_datastores={}):
        self._instantiate_datastores(init_path, input_datastores, output_datastores)

    def _instantiate_datastores(self, init_path, input_datastores, output_datastores):
        self.input_datastores, self.output_datastores = DSGenerator.DSGenerator(init_path)
        self.input_datastores.update(input_datastores)
        self.output_datastores.update(output_datastores)