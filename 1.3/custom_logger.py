import os
from pathlib import Path
import logging
import time

PARENT_PATH = os.fspath(Path(__file__).parents[0])
LOGGING_FILE_PATH = os.path.join(PARENT_PATH,
                                 "__logger",
                                 "{}.log")


def set_logger(file_path_extension):
    '''A logging helper.
    Keeps the logged experiments in the __logger path.
    Both prints out on the Terminal and writes on the
    .log file.'''
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)-7s: %(levelname)-1s %(message)s",
        datefmt="%d-%m-%Y | %H:%M:%S'",
        handlers=[
            logging.FileHandler(
                LOGGING_FILE_PATH.format(file_path_extension)
            ),
            logging.StreamHandler()
        ])
    logging.Formatter.converter = time.localtime

    return logging