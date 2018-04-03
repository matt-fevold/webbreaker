#!/usr/bin/env python
# -*- coding: utf-8 -*-

from webbreaker.common.webbreakerlogger import Logger
from subprocess import CalledProcessError
from webbreaker.common.confighelper import Config
from webbreaker.common.logexceptionhelper import LogExceptionHelper

logexceptionhelper = LogExceptionHelper()

try:
    import ConfigParser as configparser

    config = configparser.SafeConfigParser()

except ImportError:  # Python3
    import configparser

    config = configparser.ConfigParser()


class FortifyConfig(object):
    def __init__(self):
        config_file = Config().config
        try:
            config.read(config_file)
            self.ssc_url = config.get("fortify", "ssc_url")
            self.project_template = config.get("fortify", "project_template")
            self.application_name = config.get("fortify", "application_name")
            self.verify_ssl = config.get("fortify", "verify_ssl")

            self.search_expression = config.get("fortify", "search_expression")
            self.version_attribute_value = config.get("fortify", "version_attribute_value")
            self.version_attribute_values = config.get("fortify", "version_attribute_values")
            self.attribute_definition_id = config.get("fortify", "attribute_definition_id")

        except (configparser.NoOptionError, CalledProcessError) as noe:
            Logger.app.error("{} has incorrect or missing values {}".format(config_file, noe))
        except configparser.Error as e:
            logexceptionhelper.LogErrorReading(config_file, e)
