#!/usr/bin/env python
# -*-coding:utf-8-*-

import click
from contextlib import contextmanager
from exitstatus import ExitStatus
from multiprocessing.dummy import Pool as ThreadPool
from pybreaker import CircuitBreaker
import requests
from signal import getsignal, SIGINT, SIGABRT,SIGTERM, signal
from sys import exit
from subprocess import CalledProcessError
import urllib3

from webbreaker.common.webbreakerlogger import Logger
from webbreaker.webinspect.webinspect_config import WebInspectConfig
from webbreaker.webinspect.authentication import WebInspectAuth
from webbreaker.webinspect.common.helper import WebInspectAPIHelper

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
    def __init__(self, overrides):
        # used for multi threading the _is_available API call
        # self._results_queue = queue.Queue()

        # run the scan
        self.scan(overrides)

    @CircuitBreaker(fail_max=5, reset_timeout=60)
    def _set_config_(self):
        self.config = WebInspectConfig()
        Logger.app.debug("Webinspect Config: {}".format(self.config))

    @CircuitBreaker(fail_max=5, reset_timeout=60)
    def scan(self, overrides):
        self._set_config_()

        username = overrides['username']
        password = overrides['password']

        # Convert multiple args from tuples to lists
        overrides['allowed_hosts'] = list(overrides['allowed_hosts'])
        overrides['start_urls'] = list(overrides['start_urls'])
        overrides['workflow_macros'] = list(overrides['workflow_macros'])

        auth_config = WebInspectAuth()
        username, password = auth_config.authenticate(username, password)

        # ...as well as pulling down webinspect server config files from github...
        try:
            self.config.fetch_webinspect_configs(overrides)
        except (CalledProcessError, TypeError):
            Logger.app.error("Retrieving WebInspect configurations from GIT repo...")
            # ...and settings...
        webinspect_settings = self.config.parse_webinspect_options(overrides)

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

        # TODO revert back to the old way
        try:
            Logger.app.info("Running WebInspect Scan")
            self.scan_id = self.webinspect_api.create_scan()

            scan_complete = False
            while not scan_complete:

                current_scan_status = self.webinspect_api.get_scan_status(self.scan_id)
                print("scan id: ", self.scan_id)

                if self.scan_id:
                    Logger.app.info("Scan status: {}".format(current_scan_status))
                    if current_scan_status.lower() != 'complete':
                        scan_complete = True
                        Logger.app.info("status change: ".format(current_scan_status))

            # # Start a single thread so we can have a timeout functionality added.
            # pool = ThreadPool(1)
            # pool.imap_unordered(self._scan, [self.scan_id])
            #
            # # context manager to handle interrupts properly
            # with self._termination_event_handler():
            #     # block until scan completion.
            #     self._results_queue.get(block=True)
            #
            # # kill thread
            # pool.terminate()

                self.webinspect_api.export_scan_results(self.scan_id, 'fpr')
                self.webinspect_api.export_scan_results(self.scan_id, 'xml')
                # self._stop_scan(self.scan_id)

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

    # @CircuitBreaker(fail_max=5, reset_timeout=60)
    # def _scan(self, scan_id):
    #     # for multithreading we want to use the same server each request
    #     self.webinspect_server = self.webinspect_api.setting_overrides.endpoint
    #     self.webinspect_api.host = self.webinspect_server
    #
    #     scan_complete = False
    #     while not scan_complete:
    #         current_status = self.webinspect_api.get_scan_status(scan_id)
    #
    #         if current_status.lower() == 'complete':
    #             scan_complete = True
    #             # Now let's download or export the scan artifact in two formats
    #             self.webinspect_api.export_scan_results(scan_id, 'fpr')
    #             self.webinspect_api.export_scan_results(scan_id, 'xml')
    #             self._results_queue.put('complete', block=False)
    #             # TODO add json export

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




