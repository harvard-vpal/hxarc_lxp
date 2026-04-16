# -*- coding: utf-8 -*-

import logging

# Prep the logger
VERBOSE_LOGFORMAT = "%(asctime)s\t%(levelname)s\t%(name)s:%(lineno)d\t%(message)s"
DATETIME_LOGFORMAT = "%Y-%m-%dT%H:%M:%S"
LOGLEVEL = logging.DEBUG


def config_log(logfile=None):
    """NOT always log to file."""
    handlers = [logging.StreamHandler()]
    if logfile:
        handlers += logging.FileHandler(logfile)

    logging.basicConfig(
        level=LOGLEVEL,
        format=VERBOSE_LOGFORMAT,
        datefmt=DATETIME_LOGFORMAT,
        handlers=handlers,
    )
