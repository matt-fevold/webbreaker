#!/usr/bin/env python
# -*- coding: utf-8 -*-


from webbreaker.common.webbreakerlogger import Logger
from webbreaker.common.confighelper import Config

import os
import sys
from exitstatus import ExitStatus
from webbreaker.common.logexceptionhelper import LogExceptionHelper

logexceptionhelper = LogExceptionHelper()

try:
    import ConfigParser as configparser

    config = configparser.SafeConfigParser()
except ImportError:  # Python3
    import configparser

    config = configparser.ConfigParser()


class WebBreakerConfig(object):
    def parse_emailer_settings(self):
        emailer_dict = {}
        config.read(Config().config)

        try:
            emailer_dict['smtp_host'] = config.get('emailer', 'smtp_host')
            emailer_dict['smtp_port'] = config.get('emailer', 'smtp_port')
            emailer_dict['from_address'] = config.get('emailer', 'from_address')
            emailer_dict['to_address'] = config.get('emailer', 'to_address')
            emailer_dict['email_template'] = config.get('emailer', 'email_template')
        except configparser.NoOptionError:
            Logger.console.error("{} has incorrect or missing values!".format(self.config))
            Logger.console.info("Your scan email notifier is not configured: {}".format(self.config))

        return emailer_dict


def convert_verify_ssl_config(verify_ssl):
    path = os.path.abspath(os.path.realpath(verify_ssl))
    if os.path.exists(path):
        return path
    elif verify_ssl.upper() == 'FALSE':
        return False
    else:
        logexceptionhelper.LogErrorFortifyInvalidSSLCredentials()
        sys.exit(ExitStatus.failure)
