import logging
import sys

def set_logger_mode(logger, mode):
    """
    This will set the logging mode
    for the logger
    :param logger:
    :param mode:
    :return:
    """
    if mode == "DEBUG":
        logger.setLevel(logging.DEBUG)
    elif mode == "INFO":
        logger.setLevel(logging.INFO)
    elif mode == "WARNING":
        logger.setLevel(logging.WARNING)
    elif mode == "ERROR":
        logger.setLevel(logging.ERROR)
    else:
        logger.setLevel(logging.INFO)

def get_logger():
    """
    This will get a new logger
    :return logger:
    """
    logger = logging.getLogger()

    handler = logging.StreamHandler(stream=sys.stdout)
    formatter = logging.Formatter("%(asctime)s %(name)-5s"
                               " %(levelname)-5s %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger
