#!/usr/bin/env python
# -*-coding:utf-8-*-


from contextlib import contextmanager
from exitstatus import ExitStatus
from multiprocessing.dummy import Pool as ThreadPool
from pybreaker import CircuitBreaker
import requests
from signal import getsignal, SIGINT, SIGABRT,SIGTERM, signal
import sys
import time
import urllib3

from webbreaker.common.webbreakerlogger import Logger
from webbreaker.webinspect.webinspect_config import WebInspectConfig
from webbreaker.webinspect.authentication import WebInspectAuth
from webbreaker.webinspect.common.helper import WebInspectAPIHelper


import random
import string
import argparse
import xml.etree.ElementTree as ElementTree

from webbreaker.webinspect.common.loghelper import WebInspectLogHelper
from webbreaker.common.webbreakerhelper import WebBreakerHelper
from webbreaker.common.confighelper import Config
import os
import re
from subprocess import CalledProcessError, check_output


runenv = WebBreakerHelper.check_run_env()
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

try:  # python 3
    import queue
except ImportError:  # python 2
    import Queue as queue


try:  # python 2
    requests.packages.urllib3.disable_warnings()
except (ImportError, AttributeError):  # Python3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class WebInspectScan:
    def __init__(self, cli_overrides):
        # used for multi threading the _is_available API call
        self._results_queue = queue.Queue()

        self.scan_overrides = ScanOverrides(cli_overrides)

        # used in some of the parse_option functions
        self.webinspect_dir = Config().git

        # run the scan
        self.scan()

    @CircuitBreaker(fail_max=5, reset_timeout=60)
    def _set_config(self):
        self.config = WebInspectConfig()
        Logger.app.debug("Webinspect Config: {}".format(self.config))

    @CircuitBreaker(fail_max=5, reset_timeout=60)
    def scan(self):
        """
        Start a scan for webinspect.
        TODO flesh out this better
        :return:
        """
        self._set_config()
        self.scan_overrides.parse_overrides()

        username = scan_overrides['username']
        password = scan_overrides['password']

        auth_config = WebInspectAuth()
        username, password = auth_config.authenticate(username, password)

        # Convert multiple args from tuples to lists
        overrides['allowed_hosts'] = list(overrides['allowed_hosts'])
        overrides['start_urls'] = list(overrides['start_urls'])
        overrides['workflow_macros'] = list(overrides['workflow_macros'])

        self._webinspect_git_clone()
        # ...as well as pulling down webinspect server config files from github...
        try:
            self._fetch_webinspect_configs(overrides)
        except (CalledProcessError, TypeError):
            Logger.app.error("Retrieving WebInspect configurations from GIT repo...")
            # ...and settings...
        webinspect_settings = self._parse_webinspect_options(overrides)

        # The webinspect client is our point of interaction with the webinspect server farm
        self.webinspect_api = WebInspectAPIHelper(username=username, password=password, webinspect_setting_overrides=webinspect_settings)

        # if a scan policy has been specified, we need to make sure we can find/use it
        self.webinspect_api.verify_scan_policy(self.config)

        # Upload whatever overrides have been provided, skipped unless explicitly declared
        if self.webinspect_api.setting_overrides.webinspect_upload_settings:
            self.webinspect_api.upload_settings()

        if self.webinspect_api.setting_overrides.webinspect_upload_webmacros:
            self.webinspect_api.upload_webmacros()

        # if there was a provided scan policy, we've already uploaded so don't bother doing it again.
        if self.webinspect_api.setting_overrides.webinspect_upload_policy and not self.webinspect_api.setting_overrides.scan_policy:
            self.webinspect_api.upload_policy()

        try:
            Logger.app.info("Running WebInspect Scan")
            self.scan_id = self.webinspect_api.create_scan()  # it is self.scan to properly handle an exit event - find a better way

            # Start a single thread so we can have a timeout functionality added.
            pool = ThreadPool(1)
            pool.imap_unordered(self._scan, [self.scan_id])

            # context manager to handle interrupts properly
            with self._termination_event_handler():
                # block until scan completion.
                self._results_queue.get(block=True)

            # kill thread
            pool.terminate()

        # TODO go through and make sure that all these exceptions happen - way too many
        except (requests.exceptions.ConnectionError, requests.exceptions.HTTPError, TypeError, NameError, KeyError,
                IndexError) as e:
            Logger.app.error(
                "WebInspect scan was not properly configured, unable to launch!! see also: {}".format(e))
            raise
        except queue.Empty as e:  # if queue is still empty after timeout period this is raised.
            Logger.app.error("The WebInspect server is unreachable after several retries: {}!".format(e))
            self._stop_scan(self.scan_id)
            exit(ExitStatus.failure)

        Logger.app.info("WebInspect Scan Complete.")

        # If we've made it this far, our new credentials are valid and should be saved
        if username is not None and password is not None and not auth_config.has_auth_creds():
            auth_config.write_credentials(username, password)

    @CircuitBreaker(fail_max=5, reset_timeout=60)
    def _scan(self, scan_id):
        # for multithreading we want to use the same server each request
        self.webinspect_server = self.webinspect_api.setting_overrides.endpoint
        self.webinspect_api.host = self.webinspect_server

        scan_complete = False
        while not scan_complete:
            current_status = self.webinspect_api.get_scan_status(scan_id)

            if current_status.lower() == 'complete':
                scan_complete = True
                # Now let's download or export the scan artifact in two formats
                self.webinspect_api.export_scan_results(scan_id, 'fpr')
                self.webinspect_api.export_scan_results(scan_id, 'xml')
                self._results_queue.put('complete', block=False)
                # TODO add json export

            elif current_status.lower() == 'notrunning':
                webinspectloghelper.log_error_not_running_scan()
                self._stop_scan(scan_id)
                sys.exit(ExitStatus.failure)
            time.sleep(2)

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
        # ...as well as pulling down webinspect server config files from github...
        try:
            self._fetch_webinspect_configs()
        except (CalledProcessError, TypeError):
            Logger.app.error("Retrieving WebInspect configurations from GIT repo...")
            # ...and settings...

    # TODO - move this to scan along with the other functions that only are used there.
    def _fetch_webinspect_configs(self):
        config_helper = Config()
        etc_dir = config_helper.etc
        git_dir = os.path.join(config_helper.git, '.git')
        try:
            if self.scan_overrides.settings == 'Default':
                Logger.app.debug("Default settings were used")

                if os.path.isfile(self.scan_overrides.webinspect_upload_settings + '.xml'):
                    self.scan_overrides.webinspect_upload_settings = self.scan_overrides.webinspect_upload_settings + '.xml'
                if os.path.isfile(self.scan_overrides.webinspect_upload_settings):
                    options['upload_scan_settings'] = self.scan_overrides.webinspect_upload_settings
                else:
                    try:
                        options['upload_scan_settings'] = os.path.join(etc_dir,
                                                                       'settings',
                                                                       self.scan_overrides.webinspect_upload_settings + '.xml')
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
                check_output(['git', 'clone', self.config.webinspect_git, config_helper.git])

            else:
                Logger.app.error(
                    "No GIT Repo was declared in your config.ini, therefore nothing will be cloned!")
        except (CalledProcessError, AttributeError) as e:
            webinspectloghelper.log_webinspect_config_issue(e)
            raise
        except GitCommandError as e:
            webinspectloghelper.log_git_access_error(self.config.webinspect_git, e)
            raise Exception(webinspectloghelper.log_error_fetch_webinspect_configs())
        except IndexError as e:
            webinspectloghelper.log_config_file_unavailable(e)
            raise Exception(webinspectloghelper.log_error_fetch_webinspect_configs())

        Logger.app.debug("Completed webinspect config fetch")



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
            exit(1)
        except ElementTree.ParseError:
            Logger.app.error("Settings file is not configured properly")
            exit(1)
        return targets

    # TODO find a permanent home for this function




# TODO clean up
import os
from pybreaker import CircuitBreaker
from webbreaker.common.webbreakerhelper import WebBreakerHelper
from webbreaker.common.webbreakerlogger import Logger

from webbreaker.webinspect.jit_scheduler import WebInspectJitScheduler, NoServersAvailableError
from webbreaker.webinspect.webinspect_config import WebInspectConfig


class ScanOverrides:
    """
    This class is meant to handle all the ugliness that is webinspect scan optional arguements overrides.
    """
    def __init__(self, override_dict, username=None, password=None):
        try:
            self.username = username
            self.password = password

            self.settings = override_dict['webinspect_settings']
            self.scan_name = override_dict['webinspect_scan_name']
            self.webinspect_upload_settings = override_dict['webinspect_upload_settings']
            self.webinspect_upload_policy = override_dict['webinspect_upload_policy']
            self.webinspect_upload_webmacros = override_dict['webinspect_upload_webmacros']
            self.scan_mode = override_dict['webinspect_overrides_scan_mode']
            self.scan_scope = override_dict['webinspect_overrides_scan_scope']
            self.login_macro = override_dict['webinspect_overrides_login_macro']
            self.scan_policy = override_dict['webinspect_overrides_scan_policy']
            self.scan_start = override_dict['webinspect_overrides_scan_start']
            self.start_urls = override_dict['webinspect_overrides_start_urls']
            self.workflow_macros = override_dict['webinspect_workflow_macros']
            self.allowed_hosts = override_dict['webinspect_allowed_hosts']
            self.scan_size = override_dict['webinspect_scan_size']
            self.fortify_user = override_dict['fortify_user']

            self.endpoint = self.get_endpoint()
            self.runenv = WebBreakerHelper.check_run_env()

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
            # Breakour exception handling into better messages
        except (EnvironmentError, UnboundLocalError, NameError, TypeError, AttributeError) as e:
            # TODO clean up
            # webinspect_logexceptionhelper.log_error_settings(self.settings, e)
            raise

    def _parse_webinspect_options(self):
        """
        The purpose is to go through and handle all the different optional arguments. The flow is that there is a
        self.options and we manipulate it in each of the functions. The return value ends up being used in the api
        call to start a scan.
        :param options: The dictionary of click arguments that are all optional.
        :return: a dictionary to be used in the scan api call.
        """
        try:
            # value to return.
            settings_dict = {}

            # TODO move to init and fix conflict with overrides.


            # trim extensions off the options.
            self._trim_options()

            # name the scan
            self._parse_scan_name_option()

            # ? TODO
            self._parse_upload_settings_option()

            # if login macro has been specified, ensure it's uploaded.
            self._parse_login_macro_option()

            # if workflow macros have been provided, ensure they are uploaded
            self._parse_workflow_macros_option()

            # ? TODO
            self._parse_upload_webmacros_option()

            # if upload_policy provided explicitly, follow that. otherwise, default to scan_policy if provided
            self._parse_upload_policy_option()

            # Determine the targets specified in a settings file
            targets = self._parse_upload_settings_option_for_scan_target()

            # Unless explicitly stated --allowed_hosts by default will use all values from --start_urls
            self._parse_assigned_hosts_option()

            try:
                # prepares the return value for use in api call.
                settings_dict['webinspect_settings'] = self.settings  # options['settings']
                settings_dict['webinspect_scan_name'] = self.scan_name  # options['scan_name']
                settings_dict['webinspect_upload_settings'] = self.webinspect_upload_settings  # options['upload_settings']
                settings_dict['webinspect_upload_policy'] = self.webinspect_upload_policy  # options['upload_policy']
                settings_dict['webinspect_upload_webmacros'] = self.webinspect_upload_webmacros  # options['upload_webmacros']
                settings_dict['webinspect_overrides_scan_mode'] = self.scan_mode  # options['scan_mode']
                settings_dict['webinspect_overrides_scan_scope'] = self.scan_scope  # options['scan_scope']
                settings_dict['webinspect_overrides_login_macro'] = self.login_macro  # options['login_macro']
                settings_dict['webinspect_overrides_scan_policy'] = self.scan_policy  # options['scan_policy']
                settings_dict['webinspect_overrides_scan_start'] = self.scan_start  # options['scan_start']
                settings_dict['webinspect_overrides_start_urls'] = self.start_urls  # options['start_urls']
                settings_dict['webinspect_scan_targets'] = targets
                settings_dict['webinspect_workflow_macros'] = self.workflow_macros  # options['workflow_macros']
                settings_dict['webinspect_allowed_hosts'] = self.allowed_hosts  # options['allowed_hosts']
                settings_dict['webinspect_scan_size'] = self.scan_size  # options['size']

                settings_dict['fortify_user'] = self.fortify_user  # options['fortify_user']

            except argparse.ArgumentError as e:
                webinspectloghelper.log_error_in_options(e)
        except (AttributeError, UnboundLocalError, KeyError):
            # TODO WTF
            self.incorrect = webinspectloghelper.log_configuration_incorrect(Logger.app_logfile)
            raise

        Logger.app.debug("Completed webinspect settings parse")
        return settings_dict

    def _parse_scan_name_option(self):
        """
        Use self.options and depending on the run environment name the scan.
        Jenkins - either BUILD_TAG or JOB_NAME
        Others - webinspect-[5 random ascii characters]
        """
        if not self.scan_name:
            try:
                if runenv == "jenkins":
                    if "/" in os.getenv("JOB_NAME"):
                        self.scan_name = os.getenv("BUILD_TAG")
                    else:
                        self.scan_name = os.getenv("JOB_NAME")
                else:
                    self.scan_name = "webinspect" + "-" + "".join(
                        random.choice(string.ascii_uppercase + string.digits) for _ in range(5))
            except AttributeError as e:
                webinspectloghelper.log_scan_error(self.scan_name, e)

    def _parse_upload_settings_option(self):
        """
        ? TODO
        :return:
        """
        if self.webinspect_upload_settings:
            if os.path.isfile(self.webinspect_upload_settings + '.xml'):
                self.webinspect_upload_settings = self.webinspect_upload_settings + '.xml'
            if os.path.isfile(self.webinspect_upload_settings):
                self.options.upload_scan_settings = self.webinspect_upload_settings
            else:
                try:
                    self.options.upload_scan_settings = os.path.join(self.webinspect_dir,
                                                                   'settings',
                                                                        self.webinspect_upload_settings + '.xml')
                except (AttributeError, TypeError) as e:
                    webinspectloghelper.log_error_settings(self.webinspect_upload_settings, e)

        else:
            if os.path.isfile(self.options.settings + '.xml'):
                self.options.settings = self.options.settings + '.xml'

            if not os.path.isfile(self.options.settings) and self.options.settings != 'Default':
                self.webinspect_upload_settings = os.path.join(self.webinspect_dir,
                                                          'settings',
                                                               self.options.settings + '.xml')

            elif self.options.settings == 'Default':
                # All WebInspect servers come with a Default.xml settings file, no need to upload it
                self.webinspect_upload_settings = None
            else:
                self.webinspect_upload_settings = self.options.settings
                try:

                    self.options.settings = re.search('(.*)\.xml', self.options.settings).group(1)
                except AttributeError as e:
                    Logger.app.error("There was an issue finding you settings file {}, verify it exists and make "
                                     "sure you pass in the path to the file (relative path okay): {}".format(
                        self.options.settings, e))

    def _parse_login_macro_option(self):
        """
        # if login macro has been specified, ensure it's uploaded.
        :return:
        """
        if self.options.login_macro:
            if self.options.upload_webmacros:
                # add macro to existing list.
                self.options.upload_webmacros.append(self.options.login_macro)
            else:
                # add macro to new list
                self.options.upload_webmacros = []
                self.options.upload_webmacros.append(self.options.login_macro)

    def _parse_workflow_macros_option(self):
        """
        # if workflow macros have been provided, ensure they are uploaded
        :return:
        """
        if self.options.workflow_macros:
            if self.options.upload_webmacros:
                # add macros to existing list
                self.options.upload_webmacros.extend(self.options.workflow_macros)
            else:
                # add macro to new list
                self.options.upload_webmacros = list(self.options.workflow_macros)

    def _parse_upload_webmacros_option(self):
        """
        ? TODO
        :return:
        """
        if self.options.upload_webmacros:
            try:
                # trying to be clever, remove any duplicates from our upload list
                self.options.upload_webmacros = list(set(self.options.upload_webmacros))
                corrected_paths = []
                for webmacro in self.options.upload_webmacros:
                    if os.path.isfile(webmacro + '.webmacro'):
                        webmacro = webmacro + '.webmacro'
                    if not os.path.isfile(webmacro):
                        corrected_paths.append(os.path.join(self.webinspect_dir,
                                                            'webmacros',
                                                            webmacro + '.webmacro'))
                    else:
                        corrected_paths.append(webmacro)
                self.options.upload_webmacros = corrected_paths

            except (AttributeError, TypeError) as e:
                webinspectloghelper.log_error_settings(self.options.upload_webmacros, e)

    def _parse_upload_policy_option(self):
        """
        # if upload_policy provided explicitly, follow that. otherwise, default to scan_policy if provided
        :return:
        """
        try:
            if self.options.upload_policy:
                if os.path.isfile(self.options.upload_policy + '.policy'):
                    self.options.upload_policy = self.options.upload_policy + '.policy'
                if not os.path.isfile(self.options.upload_policy):
                    self.options.upload_policy = os.path.join(self.webinspect_dir, 'policies',
                                                                 self.options.upload_policy + '.policy')

            elif self.options.scan_policy:
                if os.path.isfile(self.options.scan_policy + '.policy'):
                    self.options.scan_policy = self.options.scan_policy + '.policy'
                if not os.path.isfile(self.options.scan_policy):
                    self.options.upload_policy = os.path.join(self.webinspect_dir, 'policies',
                                                                 self.options.scan_policy + '.policy')
            else:
                self.options.upload_policy = self.options.scan_policy

        except TypeError as e:
            webinspectloghelper.log_error_scan_policy(e)

    def _parse_upload_settings_option_for_scan_target(self):
        """
        # Determine the targets specified in a settings file
        :return:
        """
        try:
            if self.webinspect_upload_settings:
                targets = self._get_scan_targets(self.webinspect_upload_settings)
            else:
                targets = None
        except NameError as e:
            # TODO should I break here? Or should I assign targets=None?
            webinspectloghelper.log_no_settings_file(e)

        return targets

    def _parse_assigned_hosts_option(self):
        """
        # Unless explicitly stated --allowed_hosts by default will use all values from --start_urls
        :return:
        """
        if not self.options.allowed_hosts:
            self.options.allowed_hosts = self.options.start_urls

    @CircuitBreaker(fail_max=5, reset_timeout=60)
    def get_endpoint(self):
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

    def _trim_ext(self, file):
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

    def _trim_options(self):
        """
        strips off the extension from the options in self.options
        """
        # Trim .xml
        self.options.settings = self._trim_ext(self.options.settings)
        self.webinspect_upload_settings = self._trim_ext(self.webinspect_upload_settings)

        # Trim .webmacro
        self.options.upload_webmacros = self._trim_ext(self.options.upload_webmacros)
        self.options.workflow_macros = self._trim_ext(self.options.workflow_macros)
        self.options.login_macro = self._trim_ext(self.options.login_macro)

        # Trim .policy
        self.options.upload_policy = self._trim_ext(self.options.upload_policy)
        self.options.scan_policy = self._trim_ext(self.options.scan_policy)
