#!/usr/bin/env python
# -*-coding:utf-8-*-

import logging.config
import logging
import datetime
import sys
import os
from webbreaker.confighelper import Config

LOG_PATH = Config().log
FORMATTER = logging.Formatter('%(message)s')
DATETIME_SUFFIX = datetime.datetime.now().strftime("%m-%d-%Y")
APP_LOG = os.path.abspath(os.path.join(LOG_PATH, 'webbreaker-' + DATETIME_SUFFIX + '.log'))
DEBUG_LOG = os.path.abspath(os.path.join(LOG_PATH, 'webbreaker-debug-' + DATETIME_SUFFIX + '.log'))
STOUT_LOG = os.path.abspath(os.path.join(LOG_PATH, 'webbreaker-out' + DATETIME_SUFFIX + '.log'))


def singleton(cls):
    instances = {}

    def get_instance():
        if cls not in instances:
            instances[cls] = cls()
        return instances[cls]

    return get_instance()


def get_console_logger():
    try:
        console_logger = logging.getLogger()
        console_logger.setLevel(logging.NOTSET)
        # console_logger.propagate = False
        # if there are two console_logger use only one.
        if console_logger.handlers:
            console_logger.handlers.pop()

        # Set-up the logging configs
        ch = logging.StreamHandler()
        # Use the standard formatter constant
        ch.setFormatter(FORMATTER)
        # Only send stout INFO level messages
        ch.setLevel(logging.INFO)
        # TODO: Delete LessThanFilter if not needed in future
        # ch.addFilter(LessThanFilter(logging.WARNING))
        # add the handler
        console_logger.addHandler(ch)
    except TypeError as e:
        sys.stdout.write(str("Console logger is having issues: {}\n".format(e)))

    return console_logger


def get_app_logger(name=None):
    try:
        logger_map = {"__webbreaker__": APP_LOG}
        app_logger = logging.getLogger("__webbreaker__")
        app_logger.setLevel(logging.NOTSET)
        # if there are two app_loggers use only one.
        if app_logger.handlers:
            app_logger.handlers.pop()

        formatter = logging.Formatter('%(asctime)s: %(name)s %(levelname)s(%(message)s')
        fh = logging.FileHandler(logger_map[name], mode='a')
        fh.setFormatter(formatter)
        fh.setLevel(logging.DEBUG)
        fh.setLevel(logging.INFO)
        app_logger.addHandler(fh)
    except TypeError as e:
        sys.stdout.write(str("App logger error: {}!\n".format(e)))

    return app_logger


def get_debug_logger(name=None):
    try:
        debug_logger = logging.getLogger(name)
        debug_logger.setLevel(logging.NOTSET)
        # if there are two debug_logger use only one.
        if debug_logger.handlers:
            debug_logger.handlers.pop()

        debug_formatter = logging.Formatter('%(asctime)s: %(name)s %(levelname)s(%(message)s')
        fh = logging.FileHandler(DEBUG_LOG, mode='a')
        fh.setFormatter(debug_formatter)
        fh.setLevel(logging.DEBUG)
        debug_logger.addHandler(fh)
    except TypeError as e:
        sys.stdout.write(str("Debug logger error: {}!\n".format(e)))

    return debug_logger


# Override existing hierarchical filter logic in logger
class LessThanFilter(logging.Filter):
    def __init__(self, level):
        self._level = level
        logging.Filter.__init__(self)

    def filter(self, rec):
        return rec.levelno < self._level


@singleton
class Logger():
    def __init__(self):
        self.app = get_app_logger("__webbreaker__")
        self.debug = get_debug_logger("__webbreaker_debug__")
        self.console = get_console_logger()
        self.app_logfile = APP_LOG
        self.app_debug = DEBUG_LOG
