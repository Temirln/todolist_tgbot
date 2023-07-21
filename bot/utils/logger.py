import logging
import inspect
import os


def log_action(log_level=logging.DEBUG):
    logger_name = inspect.stack()[1][3]
    logger = logging.getLogger(logger_name)
    logger.setLevel(log_level)
    formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(name)s : %(message)s"
    )
    fh = logging.FileHandler(os.getenv("logger"), mode="a")
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    return logger
