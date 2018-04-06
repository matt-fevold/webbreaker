#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys

from exitstatus import ExitStatus
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
            self.verify_ssl = self._convert_verify_ssl_config(config.get("fortify", "verify_ssl"))

            # Bulk API Application Values
            self.business_risk_ranking = config.get("fortify", "business_risk_ranking")
            self.development_phase = config.get("fortify", "development_phase")
            self.development_strategy = config.get("fortify", "development_strategy")
            self.accessibility = config.get("fortify", "accessibility")
            self.custom_attribute_name = config.get("fortify", "custom_attribute_name")
            self.custom_attribute_value = config.get("fortify", "custom_attribute_value")

        except (configparser.NoOptionError, CalledProcessError) as noe:
            Logger.app.error("{} has incorrect or missing values {}".format(config_file, noe))
        except configparser.Error as e:
            logexceptionhelper.LogErrorReading(config_file, e)

    @staticmethod
    def _convert_verify_ssl_config(verify_ssl):
        path = os.path.abspath(os.path.realpath(verify_ssl))
        if os.path.exists(path):
            return path
        elif verify_ssl.upper() == 'FALSE':
            return False
        else:
            logexceptionhelper.LogErrorFortifyInvalidSSLCredentials()
            sys.exit(ExitStatus.failure)
