#!/usr/bin/env python
# -*- coding: utf-8 -*-

from webbreaker.common.webbreakerlogger import Logger
from webbreaker.common.confighelper import Config
from subprocess import CalledProcessError
from webbreaker.common.logexceptionhelper import LogExceptionHelper
from webbreaker.common.webbreakerconfig import convert_verify_ssl_config

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
            self.api_key = self._get_config("api_key")
            self.host = self._get_config("host")
            if len(self.host) and self.host[-1] != '/':
                self.host = self.host + '/'
            self.verify_ssl = convert_verify_ssl_config(self._get_config("verify_ssl"))

        except (configparser.NoOptionError, CalledProcessError) as noe:
            Logger.app.error("{} has incorrect or missing values {}".format(config_file, noe))
        except (configparser.Error) as e:
            logexceptionhelper.log_error_reading(config_file, e)
            # Logger.app.error("Error reading {} {}".format(config_file, e))

    def _get_config(self, key):
        """
        So that "threadfix" doesn't have to be typed everytime a new config value is needed

        :param key: some threadfix config key
        :return: the value for the given key
        """
        return config.get("threadfix", key)
