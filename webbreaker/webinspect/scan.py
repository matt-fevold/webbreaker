#!/usr/bin/env python
# -*-coding:utf-8-*-


from contextlib import contextmanager
from exitstatus import ExitStatus
import requests
from signal import getsignal, SIGINT, SIGABRT,SIGTERM, signal
from subprocess import CalledProcessError, check_output
import sys
import time
import urllib3
import os
import random
import string
import xml.etree.ElementTree as ElementTree
import re

from webbreaker.common.confighelper import Config
from webbreaker.common.webbreakerhelper import WebBreakerHelper
from webbreaker.common.webbreakerlogger import Logger
from webbreaker.common.webbreakerconfig import trim_ext
from webbreaker.webinspect.authentication import WebInspectAuth
# deviating from standard style to remove circular dependency problem.
#import webbreaker.webinspect.common.helper
from webbreaker.webinspect.common.helper import WebInspectAPIHelper
from webbreaker.webinspect.common.loghelper import WebInspectLogHelper
from webbreaker.webinspect.jit_scheduler import WebInspectJitScheduler, NoServersAvailableError
from webbreaker.webinspect.webinspect_config import WebInspectConfig


webinspectloghelper = WebInspectLogHelper()

try:
    from git.exc import GitCommandError
except (ImportError, AttributeError) as e:  # module will fail if git is not installed
    Logger.app.error("Please install the git client or add it to your PATH variable ->"
                     " https://git-scm.com/download.  See log {}!!!".format
                     (Logger.app_logfile, e.message))

try:
    import urlparse as urlparse
except ImportError:
    from urllib.parse import urlparse



try:  # python 2
    requests.packages.urllib3.disable_warnings()
except (ImportError, AttributeError):  # Python3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class WebInspectScan:
    def __init__(self, cli_overrides):
        # used for multi threading the _is_available API call
        self.config = WebInspectConfig()

        # handle all the overrides
        if 'git' not in cli_overrides:  # it shouldn't be in the overrides, but here for potential future support of cli passed git paths
            cli_overrides['git'] = Config().git

        self.scan_overrides = ScanOverrides(cli_overrides)

        # run the scan
        self.scan()

    def scan(self):
        """
        Start a scan for webinspect. It is multithreaded in that it uses a thread to handle checking on the scan status
        and a queue in the main execution to wait for a repsonse from the thread.
        :return:
        """

        # handle the authentication
        auth_config = WebInspectAuth()
        username, password = auth_config.authenticate(self.scan_overrides.username, self.scan_overrides.password)

        # handle github setup
        self._webinspect_git_clone()

        self._set_api(username=username, password=password)
        # self.webinspect_api = WebInspectAPIHelper(username=username, password=password,
        #                                           webinspect_setting_overrides=self.scan_overrides)

        # abstract out a bunch of conditional uploads
        self._upload_settings_and_policies()

        try:
            Logger.app.info("Running WebInspect Scan")

            self.scan_id = self.webinspect_api.create_scan()

            # context manager to handle interrupts properly
            with self._termination_event_handler():

                self._scan()

        except (requests.exceptions.ConnectionError, requests.exceptions.HTTPError) as e:
            webinspectloghelper.log_error_scan_start_failed(e)
            exit(ExitStatus.failure)

        Logger.app.info("WebInspect Scan Complete.")

        # If we've made it this far, our new credentials are valid and should be saved
        if username is not None and password is not None and not auth_config.has_auth_creds():
            auth_config.write_credentials(username, password)

    def _set_api(self, username, password):
        """
        created so I could mock this functionality better. It sets up the webinspect api
        :param username:
        :param password:
        :return:
        """
        self.webinspect_api = WebInspectAPIHelper(username=username, password=password,
                                                  webinspect_setting_overrides=self.scan_overrides)

    def _upload_settings_and_policies(self):
        """
        upload any settings, policies or macros that need to be uploaded
        :return:
        """

        # if a scan policy has been specified, we need to make sure we can find/use it on the server
        self.webinspect_api.verify_scan_policy(self.config)

        # Upload whatever overrides have been provided, skipped unless explicitly declared
        if self.webinspect_api.setting_overrides.webinspect_upload_settings:
            self.webinspect_api.upload_settings()

        if self.webinspect_api.setting_overrides.webinspect_upload_webmacros:
            self.webinspect_api.upload_webmacros()

        # if there was a provided scan policy, we've already uploaded so don't bother doing it again.
        if self.webinspect_api.setting_overrides.webinspect_upload_policy and not self.webinspect_api.setting_overrides.scan_policy:
            self.webinspect_api.upload_policy()

    def _scan(self, delay=2):
        """
        If it returns complete we are
        happy and download the results files. If we enter NotRunning then something has gone wrong and we want to
        exit with a failure.
        :param scan_id: the id on the webinspect server for the running scan
        :param delay: time between calls to Webinspect server
        :return: no return but upon completion sends a "complete" message back to the queue that is waiting for it.
        """
        # self.webinspect_server = self.webinspect_api.setting_overrides.endpoint
        self.webinspect_api.host = self.webinspect_api.setting_overrides.endpoint

        scan_complete = False
        while not scan_complete:
            current_status = self.webinspect_api.get_scan_status(self.scan_id)

            if current_status.lower() == 'complete':
                # Now let's download or export the scan artifact in two formats
                self.webinspect_api.export_scan_results(self.scan_id, 'fpr')
                self.webinspect_api.export_scan_results(self.scan_id, 'xml')
                return
                # TODO add json export

            elif current_status.lower() == 'notrunning':
                webinspectloghelper.log_error_not_running_scan()
                self._stop_scan(self.scan_id)
                sys.exit(ExitStatus.failure)
            time.sleep(delay)

    def _stop_scan(self, scan_id):
        self.webinspect_api.stop_scan(scan_id)

    # below functions are for handling someone forcefully ending webbreaker.
    def _exit_scan_gracefully(self, *args):
        """
        called when someone ctl+c's - sends an api call to end the running scan.
        :param args:
        :return:
        """
        Logger.app.info("Aborting!")
        self.webinspect_api.stop_scan(self.scan_id)
        exit(ExitStatus.failure)

    @contextmanager
    def _termination_event_handler(self):
        """
        meant to handle termination events (ctr+c and more) so that we call scan_end(scan_id) if a user decides to end the
        scan.
        :return:
        """
        # Intercept the "please terminate" signals
        original_sigint_handler = getsignal(SIGINT)
        original_sigabrt_handler = getsignal(SIGABRT)
        original_sigterm_handler = getsignal(SIGTERM)
        for sig in (SIGABRT, SIGINT, SIGTERM):
            signal(sig, self._exit_scan_gracefully)

        yield  # needed for context manager

        # Go back to normal signal handling
        signal(SIGABRT, original_sigabrt_handler)
        signal(SIGINT, original_sigint_handler)
        signal(SIGTERM, original_sigterm_handler)

    def _webinspect_git_clone(self):
        """
        If local file exist, it will use that file. If not, it will go to github and clone the config files
        :return:
        """
        try:
            config_helper = Config()
            etc_dir = config_helper.etc
            git_dir = os.path.join(config_helper.git, '.git')
            try:
                if self.scan_overrides.settings == 'Default':
                    webinspectloghelper.log_info_default_settings()

                    if os.path.isfile(self.scan_overrides.webinspect_upload_settings + '.xml'):
                        self.scan_overrides.webinspect_upload_settings = self.scan_overrides.webinspect_upload_settings + '.xml'

                elif os.path.exists(git_dir):
                    webinspectloghelper.log_info_updating_webinspect_configurations(etc_dir)

                    check_output(['git', 'init', etc_dir])
                    check_output(
                        ['git', '--git-dir=' + git_dir, '--work-tree=' + str(config_helper.git), 'reset', '--hard'])
                    check_output(
                        ['git', '--git-dir=' + git_dir, '--work-tree=' + str(config_helper.git), 'pull', '--rebase'])
                    sys.stdout.flush()
                elif not os.path.exists(git_dir):
                    webinspectloghelper.log_info_webinspect_git_clonning(config_helper.git)
                    check_output(['git', 'clone', self.config.webinspect_git, config_helper.git])

                else:
                    Logger.app.error(
                        "No GIT Repo was declared in your config.ini, therefore nothing will be cloned!")
            except (CalledProcessError, AttributeError) as e:
                webinspectloghelper.log_webinspect_config_issue(e)
                raise
            except GitCommandError as e:
                webinspectloghelper.log_git_access_error(self.config.webinspect_git, e)
                exit(ExitStatus.failure)

            except IndexError as e:
                webinspectloghelper.log_config_file_unavailable(e)
                exit(ExitStatus.failure)

            Logger.app.debug("Completed webinspect config fetch")
            
        except TypeError as e:
            webinspectloghelper.log_error_git_cloning_error(e)


class ScanOverrides:
    """
    This class is meant to handle all the ugliness that is webinspect scan optional arguments overrides.
    """
    def __init__(self, override_dict):
        try:

            # used in some of the parse_overrides functions
            self.webinspect_dir = override_dict['git']

            self.username = override_dict['username']
            self.password = override_dict['password']

            self.settings = override_dict['settings']
            self.scan_name = override_dict['scan_name']
            # Deprecate these click options
            self.webinspect_upload_settings = override_dict['upload_settings']
            self.webinspect_upload_policy = override_dict['upload_policy']
            self.webinspect_upload_webmacros = override_dict['upload_webmacros']
            # end deprecation
            self.scan_mode = override_dict['scan_mode']
            self.scan_scope = override_dict['scan_scope']
            self.login_macro = override_dict['login_macro']
            self.scan_policy = override_dict['scan_policy']
            self.scan_start = override_dict['scan_start']
            self.scan_size = override_dict['size']
            self.fortify_user = override_dict['fortify_user']
            self.targets = None  # to be set in a parse function

            # need to convert tuple to list
            self.start_urls = list(override_dict['start_urls'])
            self.workflow_macros = list(override_dict['workflow_macros'])
            self.allowed_hosts = list(override_dict['allowed_hosts'])

            self.endpoint = self.get_endpoint()
            self.runenv = WebBreakerHelper.check_run_env()

            # prepare the options
            self._parse_webinspect_overrides()

            Logger.app.debug("Completed webinspect client initialization")
            Logger.app.debug("url: {}".format(self.endpoint))
            Logger.app.debug("settings: {}".format(self.settings))
            Logger.app.debug("scan_name: {}".format(self.scan_name))
            Logger.app.debug("upload_settings: {}".format(self.webinspect_upload_settings))
            Logger.app.debug("upload_policy: {}".format(self.webinspect_upload_policy))
            Logger.app.debug("upload_webmacros: {}".format(self.webinspect_upload_webmacros))
            Logger.app.debug("workflow_macros: {}".format(self.workflow_macros))
            Logger.app.debug("allowed_hosts: {}".format(self.allowed_hosts))
            Logger.app.debug("scan_mode: {}".format(self.scan_mode))
            Logger.app.debug("scan_scope: {}".format(self.scan_scope))
            Logger.app.debug("login_macro: {}".format(self.login_macro))
            Logger.app.debug("scan_policy: {}".format(self.scan_policy))
            Logger.app.debug("scan_start: {}".format(self.scan_start))
            Logger.app.debug("start_urls: {}".format(self.start_urls))
            Logger.app.debug("fortify_user: {}".format(self.fortify_user))
        except (EnvironmentError, TypeError) as e:
            webinspectloghelper.log_error_scan_overrides_parsing_error(e)
            exit(ExitStatus.failure)

    def get_formatted_overrides(self):
        """
        Prepares the ScanOverrides object to be passed to the webinspect api as a dictionary.
        :return: a dictionary of webinspect scan overrides
        """
        settings_dict = {}

        # prepares the return value for use in api call.
        settings_dict['webinspect_settings'] = self.settings
        settings_dict['webinspect_scan_name'] = self.scan_name
        settings_dict['webinspect_upload_settings'] = self.webinspect_upload_settings
        settings_dict['webinspect_upload_policy'] = self.webinspect_upload_policy
        settings_dict['webinspect_upload_webmacros'] = self.webinspect_upload_webmacros
        settings_dict['webinspect_overrides_scan_mode'] = self.scan_mode
        settings_dict['webinspect_overrides_scan_scope'] = self.scan_scope
        settings_dict['webinspect_overrides_login_macro'] = self.login_macro
        settings_dict['webinspect_overrides_scan_policy'] = self.scan_policy
        settings_dict['webinspect_overrides_scan_start'] = self.scan_start
        settings_dict['webinspect_overrides_start_urls'] = self.start_urls
        settings_dict['webinspect_scan_targets'] = self.targets
        settings_dict['webinspect_workflow_macros'] = self.workflow_macros
        settings_dict['webinspect_allowed_hosts'] = self.allowed_hosts
        settings_dict['webinspect_scan_size'] = self.scan_size
        settings_dict['fortify_user'] = self.fortify_user

        return settings_dict

    def _parse_webinspect_overrides(self):
        """
        The purpose is to go through and handle all the different optional arguments. The flow is that there is a
        self.options and we manipulate it in each of the functions.
        :return:
        """
        try:

            # trim extensions off the options.
            self._trim_overrides()

            # name the scan
            self._parse_scan_name_overrides()

            # parse and trim .xml
            self._parse_upload_settings_overrides()

            # if login macro has been specified, ensure it's uploaded.
            self._parse_login_macro_overrides()

            # if workflow macros have been provided, ensure they are uploaded
            self._parse_workflow_macros_overrides()

            # parse and trim .webmacros
            self._parse_upload_webmacros_overrides()

            # if upload_policy provided explicitly, follow that. otherwise, default to scan_policy if provided
            self._parse_upload_policy_overrides()

            # Determine the targets specified in a settings file
            self._parse_upload_settings_overrides_for_scan_target()

            # Unless explicitly stated --allowed_hosts by default will use all values from --start_urls
            self._parse_assigned_hosts_overrides()

        except (AttributeError, UnboundLocalError, KeyError) as e:
            Logger.app.error("{}".format(e))
            # webinspectloghelper.log_configuration_incorrect(Logger.app_logfile)
            # raise

        Logger.app.debug("Completed webinspect settings parse")

    def _parse_scan_name_overrides(self):
        """
        Use self.options and depending on the run environment name the scan.
        Jenkins - either BUILD_TAG or JOB_NAME
        Others - webinspect-[5 random ascii characters]
        """
        if self.scan_name is None:  # no cli passed scan_name
            if self.runenv == "jenkins":
                if "/" in os.getenv("JOB_NAME"):
                    self.scan_name = os.getenv("BUILD_TAG")
                else:
                    self.scan_name = os.getenv("JOB_NAME")
            else:
                self.scan_name = "webinspect" + "-" + "".join(
                    random.choice(string.ascii_uppercase + string.digits) for _ in range(5))

    def _parse_upload_settings_overrides(self):
        """
        Check for a .xml settings file. Relative path for files are okay
        This function will then trim .xml. If file exist, upload to the server. Else raise an error.
        All webInspect server come with a Default.xml settings file
        :return:
        """
        # if cli supplied upload_settings
        if self.webinspect_upload_settings:
            # if the settings file is provided and is a file - add an xml file extension...
            #    more or less a quality of life thing for the cli.
            if os.path.isfile(self.webinspect_upload_settings + '.xml'):
                self.webinspect_upload_settings = self.webinspect_upload_settings + '.xml'

            if os.path.isfile(self.webinspect_upload_settings):
                self.upload_scan_settings = self.webinspect_upload_settings
            else:
                try:
                    self.upload_scan_settings = os.path.join(self.webinspect_dir,
                                                                   'settings',
                                                                        self.webinspect_upload_settings + '.xml')
                except (AttributeError, TypeError) as e:
                    webinspectloghelper.log_error_settings(self.webinspect_upload_settings, e)

        else:
            # if the settings file is provided and is a file - add an xml file extension...
            #    more or less a quality of life thing for the cli.
            if os.path.isfile(self.settings + '.xml'):
                self.settings = self.settings + '.xml'

            # if it is not a file and it is not Default
            if not os.path.isfile(self.settings) and self.settings != 'Default':

                self.webinspect_upload_settings = os.path.join(self.webinspect_dir,
                                                               'settings',
                                                               self.settings + '.xml')
            # it is using the default settings file
            elif self.settings == 'Default':
                # All WebInspect servers come with a Default.xml settings file, no need to upload it
                self.webinspect_upload_settings = None
            # it is a file and not using the default
            else:
                self.webinspect_upload_settings = self.settings
                # grab everything but .xml
                self.settings = re.search('(.*)\.xml', self.settings).group(1)

    def _parse_login_macro_overrides(self):
        """
        # if login macro has been specified, ensure it's uploaded.
        :return:
        """
        if self.login_macro:
            if self.webinspect_upload_webmacros:
                # add macro to existing list.
                self.webinspect_upload_webmacros.append(self.login_macro)
            else:
                # add macro to new list
                self.webinspect_upload_webmacros = []
                self.webinspect_upload_webmacros.append(self.login_macro)

    def _parse_workflow_macros_overrides(self):
        """
        # if workflow macros have been provided, ensure they are uploaded
        :return:
        """
        if self.workflow_macros:
            if self.webinspect_upload_webmacros:
                # add macros to existing list
                self.webinspect_upload_webmacros.extend(self.workflow_macros)
            else:
                # add macro to new list
                self.webinspect_upload_webmacros = list(self.workflow_macros)

    # TODO does this work?
    def _parse_upload_webmacros_overrides(self):
        """
        Check and vaildate for a .webmacro settings file. Relative paths for files are okay
        This function will then trim .webmacro off, if file exist then upload to server, otherwise raise an error
        :return:
        """
        if self.webinspect_upload_webmacros:
            try:
                # trying to be clever, remove any duplicates from our upload list
                self.webinspect_upload_webmacros = list(set(self.webinspect_upload_webmacros))
                corrected_paths = []
                # add .webmacro and verify it is a file
                for webmacro in self.webinspect_upload_webmacros:
                    if os.path.isfile(webmacro + '.webmacro'):
                        webmacro = webmacro + '.webmacro'
                    if not os.path.isfile(webmacro):
                        corrected_paths.append(os.path.join(self.webinspect_dir,
                                                            'webmacros',
                                                            webmacro + '.webmacro'))
                    else:
                        corrected_paths.append(webmacro)
                self.webinspect_upload_webmacros = corrected_paths

            except (AttributeError, TypeError) as e:
                webinspectloghelper.log_error_settings(self.webinspect_upload_webmacros, e)

    # TODO does this work?
    def _parse_upload_policy_overrides(self):
        """
        # if upload_policy provided explicitly, follow that. otherwise, default to scan_policy if provided
        :return:
        """
        try:
            if self.webinspect_upload_policy:
                if os.path.isfile(self.webinspect_upload_policy + '.policy'):
                    self.webinspect_upload_policy = self.webinspect_upload_policy + '.policy'
                if not os.path.isfile(self.webinspect_upload_policy):
                    self.webinspect_upload_policy = os.path.join(self.webinspect_dir, 'policies',
                                                                 self.webinspect_upload_policy + '.policy')

            elif self.scan_policy:
                if os.path.isfile(self.scan_policy + '.policy'):
                    self.scan_policy = self.scan_policy + '.policy'
                if not os.path.isfile(self.scan_policy):
                    self.webinspect_upload_policy = os.path.join(self.webinspect_dir, 'policies',
                                                                 self.scan_policy + '.policy')
            else:
                self.webinspect_upload_policy = self.scan_policy

        except TypeError as e:
            webinspectloghelper.log_error_scan_policy(e)

    def _parse_upload_settings_overrides_for_scan_target(self):
        """
        # Determine the targets specified in a settings file
        :return:
        """
        try:
            if self.webinspect_upload_settings:

                self.targets = self._get_scan_targets(self.webinspect_upload_settings)
            else:
                self.targets = None
        except NameError as e:
            webinspectloghelper.log_no_settings_file(e)
            exit(ExitStatus.failure)

    def _parse_assigned_hosts_overrides(self):
        """
        # Unless explicitly stated --allowed_hosts by default will use all values from --start_urls
        :return:
        """
        if not self.allowed_hosts:
            self.allowed_hosts = self.start_urls

    def get_endpoint(self):
        # TODO this needs to be abstracted back to the jit scheduler class - left in due to time considerations
        config = WebInspectConfig()
        lb = WebInspectJitScheduler(endpoints=config.endpoints,
                                    server_size_needed=self.scan_size,
                                    username=self.username,
                                    password=self.password)
        Logger.app.info("Querying WebInspect scan engines for availability.")
        try:
            endpoint = lb.get_endpoint()
            return endpoint

        except NoServersAvailableError as e:
            Logger.app.error("No servers are available to handle this request! {}".format(e))
            sys.exit(ExitStatus.failure)

    def _trim_overrides(self):
        """
        strips off the extension from some of the overrides
        """
        # Trim .xml
        self.settings = trim_ext(self.settings)
        self.webinspect_upload_settings = trim_ext(self.webinspect_upload_settings)

        # Trim .webmacro
        self.webinspect_upload_webmacros = trim_ext(self.webinspect_upload_webmacros)
        self.workflow_macros = trim_ext(self.workflow_macros)
        self.login_macro = trim_ext(self.login_macro)

        # Trim .policy
        self.webinspect_upload_policy = trim_ext(self.webinspect_upload_policy)
        self.scan_policy = trim_ext(self.scan_policy)

    @staticmethod
    def _get_scan_targets(settings_file_path):
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
            exit(ExitStatus.failure)
        except ElementTree.ParseError:
            Logger.app.error("Settings file is not configured properly")
            exit(ExitStatus.failure)
        return targets
