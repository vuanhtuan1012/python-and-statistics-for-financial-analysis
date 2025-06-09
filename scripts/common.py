"""
Common functions, classes, constants
"""

import logging
from pathlib import Path

import pandas as pd

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


def read_csv(filename: str, logger: logging.Logger) -> pd.DataFrame:
    """
    Returns DataFrame read from CSV file in the data directory
    """
    df = pd.read_csv(
        DATA_DIR.joinpath(filename), index_col="Date", parse_dates=["Date"]
    )
    logger.info("read successfully CSV file %s.", filename)
    return df
