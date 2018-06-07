#!/usr/bin/env python
# -*- coding: utf-8 -*-


from webbreaker.common.webbreakerlogger import Logger
from webbreaker.common.confighelper import Config

import os
import sys
from exitstatus import ExitStatus
from webbreaker.common.logexceptionhelper import LogExceptionHelper
from webbreaker.fortify.common.loghelper import FortifyLogHelper

logexceptionhelper = LogExceptionHelper()
fortifyloghelper = FortifyLogHelper()

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
    """
    if config ssl value is False return False, otherwise it should be a valid path to the cert to be used for ssl
    :param verify_ssl:
    :return: either False or the path to the CA cert
    """
    path = os.path.abspath(os.path.realpath(verify_ssl))
    if os.path.exists(path):
        return path
    elif verify_ssl.upper() == 'FALSE':
        return False
    else:
        logexceptionhelper.log_error_invalid_ssl_credentials()
        sys.exit(ExitStatus.failure)


def trim_ext(file):
    """
    This function removes the extension from a settings file. If file is a valid file, will preserve any /path/
    otherwise will just trim the extension and return that.  If it is a list it will repeat this process N times
    if it is None return None.
    :param file:
    :return:
    """
    if type(file) is list:
        result = []
        for f in file:
            if os.path.isfile(f):
                result.append(os.path.splitext(f)[0])

            else:
                result.append(os.path.splitext(os.path.basename(f))[0])
        return result
    elif file is None:
        return file
    else:
        if os.path.isfile(file):
            return os.path.splitext(file)[0]
        return os.path.splitext(os.path.basename(file))[0]