#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os
import sys
from subprocess import CalledProcessError
import re
from exitstatus import ExitStatus

from webbreaker.common.webbreakerconfig import convert_verify_ssl_config
from webbreaker.common.webbreakerlogger import Logger
from webbreaker.common.webbreakerhelper import WebBreakerHelper
from webbreaker.common.confighelper import Config
from webbreaker.webinspect.common.loghelper import WebInspectLogHelper

try:
    from git.exc import GitCommandError
except (ImportError, AttributeError) as e:  # module will fail if git is not installed
    Logger.app.error("Please install the git client or add it to your PATH variable ->"
                     " https://git-scm.com/download.  See log {}!!!".format
                     (Logger.app_logfile, e.message))

# Python2/3 compatibility statements
try:
    import ConfigParser as configparser

    config = configparser.SafeConfigParser()
except ImportError:  # Python3
    import configparser

    config = configparser.ConfigParser()

try:
   FileNotFoundError  # Python 3
except NameError:  # Python 2
   FileNotFoundError = IOError

runenv = WebBreakerHelper.check_run_env()
webinspectloghelper = WebInspectLogHelper()

class WebInspectConfig(object):
    def __init__(self):
        Logger.app.debug("Starting webinspect config initialization")
        try:
            webinspect_dict = self._get_webinspect_settings()
            
            self.endpoints = webinspect_dict['endpoints']
            self.webinspect_git = webinspect_dict['git']
            self.mapped_policies = webinspect_dict['mapped_policies']
            self.verify_ssl = convert_verify_ssl_config(webinspect_dict['verify_ssl'])
        except KeyError as e:
            Logger.app.error("Your configurations file or scan setting is incorrect : {}!!!".format(e))
        Logger.app.debug("Completed webinspect config initialization")

    @staticmethod
    def _get_webinspect_settings():
        """
        Read in webinspect config.ini settings and return it as a dictionary.
        :return:
        """
        Logger.app.debug("Getting webinspect settings from config file")
        settings_dict = {}
        webinspect_config = Config()
        config_file = webinspect_config.config

        try:
            config.read(config_file)
            endpoints = []
            sizes = []
            endpoint = re.compile('endpoint_\d*')
            size = re.compile('size_')

            for option in config.items('webinspect'):
                if endpoint.match(option[0]):
                    endpoints.append([option[0], option[1]])
                elif size.match(option[0]):
                    sizes.append([option[0], option[1]])

            settings_dict['git'] = webinspect_config.conf_get('webinspect', 'git_repo')

            settings_dict['endpoints'] = [[endpoint[1].split('|')[0], endpoint[1].split('|')[1]] for endpoint in
                                            endpoints]

            settings_dict['size_list'] = sizes

            settings_dict['mapped_policies'] = [[option, config.get('webinspect_policy', option)] for option in
                                                  config.options('webinspect_policy')]

            settings_dict['verify_ssl'] = webinspect_config.conf_get('webinspect', 'verify_ssl')

        except (configparser.NoOptionError, CalledProcessError) as e:
            Logger.app.error("{} has incorrect or missing values {}".format(config_file, e))
        except configparser.Error as e:
            Logger.app.error("Error reading webinspect settings {} {}".format(config_file, e))
        Logger.app.debug("Initializing webinspect settings from config.ini")
        return settings_dict




