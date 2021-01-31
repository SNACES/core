import logging


FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
STYLE = "%"
FILENAME = './log/snaces.log'
LEVEL = logging.INFO

class LoggerFactory():
    def init_root_logger(filename=FILENAME, level=LEVEL):
        logging.basicConfig(format=FORMAT, style=STYLE, datefmt=DATE_FORMAT,
            level=level)

    def logger(name, level=LEVEL):
        logger = logging.getLogger(name)
        logger.setLevel(LEVEL)

        formatter = logging.Formatter(fmt=FORMAT, datefmt=DATE_FORMAT)

        file_handler = logging.FileHandler(FILENAME)
        file_handler.setFormatter(formatter)
        file_handler.setLevel(LEVEL)

        logger.addHandler(file_handler)

        return logger
