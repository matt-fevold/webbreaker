#!/usr/bin/env python
# -*- coding: utf-8 -*-

from webbreaker.common.webbreakerlogger import Logger
from webbreaker.common.confighelper import Config
from subprocess import CalledProcessError
from webbreaker.common.logexceptionhelper import LogExceptionHelper

try:
    import ConfigParser as configparser

    config = configparser.SafeConfigParser()
except ImportError:  # Python3
    import configparser

    config = configparser.ConfigParser()

logexceptionhelper = LogExceptionHelper()

class ThreadFixConfig(object):
    def __init__(self):
        config_file = Config().config
        try:
            config.read(config_file)
            self.api_key = config.get("threadfix", "api_key")
            self.host = config.get("threadfix", "host")
            if len(self.host) and self.host[-1] != '/':
                self.host = self.host + '/'

        except (configparser.NoOptionError, CalledProcessError) as noe:
            Logger.app.error("{} has incorrect or missing values {}".format(config_file, noe))
        except (configparser.Error) as e:
            logexceptionhelper.log_error_reading(config_file, e)
            # Logger.app.error("Error reading {} {}".format(config_file, e))
