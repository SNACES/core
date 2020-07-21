from src.general.datastore import *
import conf.credentials as credentials

"""
Process data from Input DAOs and output results in Output DAO.
"""
class Process:
    def __init__(self, dao_factory, init_path="", input_DAOs={}, output_DAOs={}):
        self.dao_factory = dao_factory
        if (init_path):
            self._instantiate_DAOs(init_path, input_DAOs, output_DAOs)

    def _instantiate_DAOs(self, init_path, input_DAOs, output_DAOs):
        self.input_daos, self.output_DAOs = self.dao_factory.create_DAOs_from_config_file(init_path)
        self.input_daos.update(input_DAOs)
        self.output_daos.update(output_DAOs)
