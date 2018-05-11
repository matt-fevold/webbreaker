#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os
import sys

import re
from exitstatus import ExitStatus
from subprocess import CalledProcessError, check_output
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


# class WebInspectEndpoint(object):
#     def __init__(self, uri, size):
#         self.uri = uri
#         self.size = size
#
#
# class WebInspectSize(object):
#     def __init__(self, size, max_scans):
#         self.size = size
#         self.max_scans = max_scans
#

class WebInspectConfig(object):
    def __init__(self):
        Logger.app.debug("Starting webinspect config initialization")
        try:
            webinspect_dict = self._get_webinspect_settings()
            
            self.endpoints = webinspect_dict['endpoints']
            self.webinspect_git = webinspect_dict['git']
            self.mapped_policies = webinspect_dict['mapped_policies']
            self.verify_ssl = self._convert_verify_ssl_config(webinspect_dict['verify_ssl'])
        except KeyError as e:
            Logger.app.error("Your configurations file or scan setting is incorrect : {}!!!".format(e))
        Logger.app.debug("Completed webinspect config initialization")

    def _get_webinspect_settings(self):
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

    @staticmethod
    def _convert_verify_ssl_config(verify_ssl):
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
            webinspectloghelper.log_error_invalid_ssl()
            sys.exit(ExitStatus.failure)

    # TODO - move this to scan along with the other functions that only are used there.
    def fetch_webinspect_configs(self, options):
        config_helper = Config()
        etc_dir = config_helper.etc
        git_dir = os.path.join(config_helper.git, '.git')

        try:
            if options['settings'] == 'Default':
                Logger.app.debug("Default settings were used")

                if os.path.isfile(options['upload_settings'] + '.xml'):
                    options['upload_settings'] = options['upload_settings'] + '.xml'
                if os.path.isfile(options['upload_settings']):
                    options['upload_scan_settings'] = options['upload_settings']
                else:
                    try:
                        options['upload_scan_settings'] = os.path.join(etc_dir,
                                                                       'settings',
                                                                       options['upload_settings'] + '.xml')
                    except (AttributeError, TypeError) as e:
                        webinspectloghelper.log_error_settings(options['upload_settings'], e)

            elif os.path.exists(git_dir):
                Logger.app.info("Updating your WebInspect configurations from {}".format(etc_dir))
                check_output(['git', 'init', etc_dir])
                check_output(
                    ['git', '--git-dir=' + git_dir, '--work-tree=' + str(config_helper.git), 'reset', '--hard'])
                check_output(
                    ['git', '--git-dir=' + git_dir, '--work-tree=' + str(config_helper.git), 'pull', '--rebase'])
                sys.stdout.flush()
            elif not os.path.exists(git_dir):
                Logger.app.info("Cloning your specified WebInspect configurations to {}".format(config_helper.git))
                check_output(['git', 'clone', self.webinspect_git, config_helper.git])
            else:
                Logger.app.error(
                    "No GIT Repo was declared in your config.ini, therefore nothing will be cloned!")
        except (CalledProcessError, AttributeError) as e:
            webinspectloghelper.log_webinspect_config_issue(e)
            raise
        except GitCommandError as e:
            webinspectloghelper.log_git_access_error(self.webinspect_git, e)
            raise Exception(webinspectloghelper.log_error_fetch_webinspect_configs())
        except IndexError as e:
            webinspectloghelper.log_config_file_unavailable(e)
            raise Exception(webinspectloghelper.log_error_fetch_webinspect_configs())

        Logger.app.debug("Completed webinspect config fetch")
