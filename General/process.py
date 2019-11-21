import sys
sys.path.append('../')

from datastore import *
import credentials
from DAOFactory import *

"""
Process data from Input DAOs and output results in Output DAO.
"""
class Process:
    def __init__(self, init_path, input_DAOs={}, output_DAOs={}):
        self.DAO_factory = DAOFactory()
        self._instantiate_DAOs(init_path, input_DAOs, output_DAOs)

    def _instantiate_DAOs(self, init_path, input_DAOs, output_DAOs):
        self.input_DAOs, self.output_DAOs = self.DAO_factory.create_DAOs(init_path)
        self.input_DAOs.update(input_DAOs)
        self.output_DAOs.update(output_DAOs)
