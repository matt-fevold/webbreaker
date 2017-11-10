#!/usr/bin/env python
# -*- coding: utf-8 -*-

try:
    import ConfigParser as configparser
except ImportError:  # Python3
    import configparser
import os
from webbreaker.webbreakerlogger import Logger
from subprocess import CalledProcessError

try:  # Python 2
    config = configparser.SafeConfigParser()
except NameError:  # Python 3
    config = configparser.ConfigParser()


class ThreadFixConfig(object):
    def __init__(self):
        config_file = os.path.abspath(os.path.join('webbreaker', 'etc', 'threadfix.ini'))
        try:
            config.read(config_file)
            self.api_key = config.get("threadfix", "api_key")
            self.host = config.get("threadfix", "host")
            if len(self.host) and self.host[-1] != '/':
                self.host = self.host + '/'

        except (configparser.NoOptionError, CalledProcessError) as noe:
            Logger.app.error("{} has incorrect or missing values {}".format(config_file, noe))
        except configparser.Error as e:
            Logger.app.error("Error reading {} {}".format(config_file, e))
        except Exception as e:
            Logger.app.error("Unknown Error: {}".format(e))
