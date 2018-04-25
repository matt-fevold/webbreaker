#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import os
import sys
import random
import string
import re
import xml.etree.ElementTree as ElementTree
from exitstatus import ExitStatus
from subprocess import CalledProcessError, check_output
from webbreaker.common.webbreakerlogger import Logger
from webbreaker.common.webbreakerhelper import WebBreakerHelper
from webbreaker.common.confighelper import Config
from webbreaker.webinspect.common.loghelper import WebInspectLogHelper
from webbreaker.fortify.common.loghelper import FortifyLogHelper



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
fortifyloghelper = FortifyLogHelper()


class WebInspectEndpoint(object):
    def __init__(self, uri, size):
        self.uri = uri
        self.size = size


class WebInspectSize(object):
    def __init__(self, size, max_scans):
        self.size = size
        self.max_scans = max_scans


class WebInspectConfig(object):
    def __init__(self):
        Logger.app.debug("Starting webinspect config initialization")
        try:
            webinspect_dict = self.__get_webinspect_settings__()
            self.endpoints = webinspect_dict['endpoints']
            self.webinspect_git = webinspect_dict['git']
            self.mapped_policies = webinspect_dict['mapped_policies']
            self.verify_ssl = self._convert_verify_ssl_config(webinspect_dict['verify_ssl'])
        except KeyError as e:
            Logger.app.error("Your configurations file or scan setting is incorrect : {}!!!".format(e))
        Logger.app.debug("Completed webinspect config initialization")

    def __get_webinspect_settings__(self):
        Logger.app.debug("Getting webinspect settings from config file")
        webinspect_dict = {}
        wb_config = Config()
        webinspect_setting = wb_config.config

        try:
            config.read(webinspect_setting)
            endpoints = []
            sizes = []
            endpoint = re.compile('endpoint_\d*')
            size = re.compile('size_')

            for option in config.items('webinspect'):
                if endpoint.match(option[0]):
                    endpoints.append([option[0], option[1]])
                elif size.match(option[0]):
                    sizes.append([option[0], option[1]])

            webinspect_dict['git'] = wb_config.conf_get('webinspect', 'git_repo')

            webinspect_dict['endpoints'] = [[endpoint[1].split('|')[0], endpoint[1].split('|')[1]] for endpoint in
                                            endpoints]

            webinspect_dict['size_list'] = sizes

            webinspect_dict['mapped_policies'] = [[option, config.get('webinspect_policy', option)] for option in
                                                  config.options('webinspect_policy')]

            webinspect_dict['verify_ssl'] = wb_config.conf_get('webinspect', 'verify_ssl')

        except (configparser.NoOptionError, CalledProcessError) as e:
            Logger.app.error("{} has incorrect or missing values {}".format(webinspect_setting, e))
        except configparser.Error as e:
            Logger.app.error("Error reading webinspect settings {} {}".format(webinspect_setting, e))
        Logger.app.debug("Initializing webinspect settings from config.ini")
        return webinspect_dict

    def __getScanTargets__(self, settings_file_path):
        """
        Given a settings file at the provided path, return a set containing
        the targets for the scan.
        :param settings_file_path: Path to WebInspect settings file
        :return: unordered set of targets
        """
        # TODO: Validate settings_file_path
        targets = set()
        try:
            tree = ElementTree.parse(settings_file_path)
            root = tree.getroot()
            for target in root.findall("xmlns:HostFolderRules/"
                                       "xmlns:List/"
                                       "xmlns:HostFolderRuleData/"
                                       "xmlns:HostMatch/"
                                       "xmlns:List/"
                                       "xmlns:LookupList/"
                                       "xmlns:string",
                                       namespaces={'xmlns': 'http://spidynamics.com/schemas/scanner/1.0'}):
                targets.add(target.text)
        except FileNotFoundError:
            Logger.app.error("Unable to read the settings file {0}".format(settings_file_path))
            sys.exit(1)
        except ElementTree.ParseError:
            Logger.app.error("Settings file is not configured properly")
            sys.exit(1)
        return targets

    def parse_webinspect_options(self, options):
        try:
            webinspect_dir = Config().git
            webinspect_dict = {}

            # Trim .xml
            options['settings'] = self.trim_ext(options['settings'])
            # Trim .webmacro
            options['upload_webmacros'] = self.trim_ext(options['upload_webmacros'])
            options['workflow_macros'] = self.trim_ext(options['workflow_macros'])
            options['login_macro'] = self.trim_ext(options['login_macro'])
            # Trim .policy
            options['upload_policy'] = self.trim_ext(options['upload_policy'])
            # Trim .policy
            options['scan_policy'] = self.trim_ext(options['scan_policy'])

            # Trim .xml
            options['upload_settings'] = self.trim_ext(options['upload_settings'])

            if not options['scan_name']:
                try:
                    if runenv == "jenkins":
                        if "/" in os.getenv("JOB_NAME"):
                            options['scan_name'] = os.getenv("BUILD_TAG")
                        else:
                            options['scan_name'] = os.getenv("JOB_NAME")
                    else:
                        options['scan_name'] = "webinspect" + "-" + "".join(
                            random.choice(string.ascii_uppercase + string.digits) for _ in range(5))
                except AttributeError as e:
                    webinspectloghelper.log_scan_error(options['scan_name'], e)

            if options['upload_settings']:
                if os.path.isfile(options['upload_settings'] + '.xml'):
                    options['upload_settings'] = options['upload_settings'] + '.xml'
                if os.path.isfile(options['upload_settings']):
                    options['upload_scan_settings'] = options['upload_settings']
                else:
                    try:
                        options['upload_scan_settings'] = os.path.join(webinspect_dir,
                                                                       'settings',
                                                                       options['upload_settings'] + '.xml')
                    except (AttributeError, TypeError) as e:
                        webinspectloghelper.log_error_settings(options['upload_settings'], e)

            else:
                if os.path.isfile(options['settings'] + '.xml'):
                    options['settings'] = options['settings'] + '.xml'

                if not os.path.isfile(options['settings']) and options['settings'] != 'Default':
                    options['upload_settings'] = os.path.join(webinspect_dir,
                                                              'settings',
                                                              options['settings'] + '.xml')

                elif options['settings'] == 'Default':
                    # All WebInspect servers come with a Default.xml settings file, no need to upload it
                    options['upload_settings'] = None
                else:
                    options['upload_settings'] = options['settings']
                    try:

                        options['settings'] = re.search('(.*)\.xml', options['settings']).group(1)
                    except AttributeError as e:
                        Logger.app.error("There was an issue finding you settings file {}, verify it exists and make "
                                         "sure you pass in the path to the file (relative path okay): {}".format(options['settings'], e))

            # if login macro has been specified, ensure it's uploaded.
            if options['login_macro']:
                if options['upload_webmacros']:
                    # add macro to existing list.
                    options['upload_webmacros'].append(options['login_macro'])
                else:
                    # add macro to new list
                    options['upload_webmacros'] = []
                    options['upload_webmacros'].append(options['login_macro'])

            # if workflow macros have been provided, ensure they are uploaded
            if options['workflow_macros']:
                if options['upload_webmacros']:
                    # add macros to existing list
                    options['upload_webmacros'].extend(options['workflow_macros'])
                else:
                    # add macro to new list
                    options['upload_webmacros'] = list(options['workflow_macros'])

            if options['upload_webmacros']:
                try:
                    # trying to be clever, remove any duplicates from our upload list
                    options['upload_webmacros'] = list(set(options['upload_webmacros']))
                    corrected_paths = []
                    for webmacro in options['upload_webmacros']:
                        if os.path.isfile(webmacro + '.webmacro'):
                            webmacro = webmacro + '.webmacro'
                        if not os.path.isfile(webmacro):
                            corrected_paths.append(os.path.join(webinspect_dir,
                                                                'webmacros',
                                                                webmacro + '.webmacro'))
                        else:
                            corrected_paths.append(webmacro)
                    options['upload_webmacros'] = corrected_paths

                except (AttributeError, TypeError) as e:
                    webinspectloghelper.log_error_settings(options['upload_webmacros'], e)

            # if upload_policy provided explicitly, follow that. otherwise, default to scan_policy if provided
            try:
                if options['upload_policy']:
                    if os.path.isfile(options['upload_policy'] + '.policy'):
                        options['upload_policy'] = options['upload_policy'] + '.policy'
                    if not os.path.isfile(options['upload_policy']):
                        options['upload_policy'] = os.path.join(webinspect_dir,
                                                                'policies',
                                                                options['upload_policy'] + '.policy')

                elif options['scan_policy']:
                    if os.path.isfile(options['scan_policy'] + '.policy'):
                        options['scan_policy'] = options['scan_policy'] + '.policy'
                    if not os.path.isfile(options['scan_policy']):
                        options['upload_policy'] = os.path.join(webinspect_dir,
                                                                'policies',
                                                                options['scan_policy'] + '.policy')
                else:
                    options['upload_policy'] = options['scan_policy']

            except TypeError as e:
                webinspectloghelper.log_error_scan_policy(e)

            # Determine the targets specified in a settings file
            try:
                if options['upload_settings']:
                    targets = self.__getScanTargets__(options['upload_settings'])
                else:
                    targets = None
            except NameError as e:
                webinspectloghelper.log_no_settings_file(e)

            # Unless explicitly stated --allowed_hosts by default will use all values from --start_urls
            if not options['allowed_hosts']:
                options['allowed_hosts'] = options['start_urls']

            try:
                webinspect_dict['webinspect_settings'] = options['settings']
                webinspect_dict['webinspect_scan_name'] = options['scan_name']
                webinspect_dict['webinspect_upload_settings'] = options['upload_settings']
                webinspect_dict['webinspect_upload_policy'] = options['upload_policy']
                webinspect_dict['webinspect_upload_webmacros'] = options['upload_webmacros']
                webinspect_dict['webinspect_overrides_scan_mode'] = options['scan_mode']
                webinspect_dict['webinspect_overrides_scan_scope'] = options['scan_scope']
                webinspect_dict['webinspect_overrides_login_macro'] = options['login_macro']
                webinspect_dict['webinspect_overrides_scan_policy'] = options['scan_policy']
                webinspect_dict['webinspect_overrides_scan_start'] = options['scan_start']
                webinspect_dict['webinspect_overrides_start_urls'] = options['start_urls']
                webinspect_dict['webinspect_scan_targets'] = targets
                webinspect_dict['webinspect_workflow_macros'] = options['workflow_macros']
                webinspect_dict['webinspect_allowed_hosts'] = options['allowed_hosts']
                webinspect_dict['webinspect_scan_size'] = options['size']
                webinspect_dict['fortify_user'] = options['fortify_user']

            except argparse.ArgumentError as e:
                webinspectloghelper.log_error_in_options(e)
        except (AttributeError, UnboundLocalError, KeyError):
            self.incorrect = webinspectloghelper.log_configuration_incorrect(Logger.app_logfile)
            raise

        Logger.app.debug("Completed webinspect settings parse")
        return webinspect_dict

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
            fortifyloghelper.log_error_invalid_ssl()
            sys.exit(ExitStatus.failure)

    def trim_ext(self, file):
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


