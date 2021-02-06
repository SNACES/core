from src.dependencies.dao_module import DAOModule
from src.dependencies.process_module import ProcessModule
from src.scripts.parser.parse_config import parse_from_file
from src.shared.logger_factory import LoggerFactory

class Injector():
    """
    The Injector is used to initialize all the modules used to inject
    dependencies
    """

    def __init__(self, config):
        self.config = config

        self.dao_module = None
        self.process_module = None

    def get_dao_module(self) -> DAOModule:
        if self.dao_module is None:
            self.dao_module = DAOModule(self.config)

        return self.dao_module

    def get_process_module(self) -> ProcessModule:
        if self.process_module is None:
            dao_module = self.get_dao_module()
            self.process_module = ProcessModule(dao_module)

        return self.process_module


    def get_injector_from_file(path: str):
        config = parse_from_file(path)
        injector = Injector(config)

        log_config = config.get("Logging", {})
        LoggerFactory.init_root_logger("snaces2.log")

        return injector
