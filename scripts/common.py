"""
Common functions, classes, constants
"""

import logging
from pathlib import Path

ROOT_DIR = Path(__file__).parent.parent
DATA_DIR = ROOT_DIR.joinpath("data")


def get_logger() -> logging.Logger:
    """
    Returns logger
    """
    logger = logging.getLogger(__name__)

    # logger already exists
    if len(logger.handlers) > 0:
        return logger

    # set logger level
    logger.setLevel(logging.INFO)

    # create a console handler
    handler = logging.StreamHandler()
    handler.setLevel(logging.DEBUG)

    # create a formatter and add it to handler
    formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
    )
    handler.setFormatter(formatter)

    # add handler to logger
    logger.addHandler(handler)

    return logger
