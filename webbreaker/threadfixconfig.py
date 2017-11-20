#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from webbreaker.webbreakerlogger import Logger
from subprocess import CalledProcessError

try:
    import ConfigParser as configparser

    config = configparser.SafeConfigParser()
except ImportError:  # Python3
    import configparser

    config = configparser.ConfigParser()


class ThreadFixConfig(object):
    def __init__(self):
        config_file = os.path.abspath('.config')
        try:
            config.read(config_file)
            self.api_key = config.get("threadfix", "api_key")
            self.host = config.get("threadfix", "host")
            if len(self.host) and self.host[-1] != '/':
                self.host = self.host + '/'

        except (configparser.NoOptionError, CalledProcessError) as noe:
            Logger.app.error("{} has incorrect or missing values {}".format(config_file, noe))
        except (configparser.Error) as e:
            Logger.app.error("Error reading {} {}".format(config_file, e))
