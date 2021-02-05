import logging
import math


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

        logger.log_progress = lambda self, i, total: _log_progress(self, i, total)

        return logger

def _log_progress(log, i, total):
    percent_done = i/total * 100
    if _passes_interval(i, total, 2):
        log.info("Done " + str(math.floor(percent_done)) + "% of process")

def _passes_interval(i, total, interval):
    current_percent = i/total * 100
    previous_percent = (i - 1)/total * 100

    return int(current_percent/interval) > int(previous_percent/interval)
