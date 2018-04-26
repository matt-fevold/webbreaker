#!/usr/bin/env python
# -*-coding:utf-8-*-

from contextlib import contextmanager
from exitstatus import ExitStatus
import os, datetime
import requests
import urllib3
from webbreaker.common.webbreakerlogger import Logger
from webbreaker.webinspect.webinspect_config import WebInspectConfig
from webbreaker.webinspect.authentication import WebInspectAuth
from webbreaker.webinspect.common.helper import WebInspectAPIHelper
from signal import *
from subprocess import CalledProcessError
import sys


try:
    import urlparse as urlparse
except ImportError:
    from urllib.parse import urlparse


try:
    requests.packages.urllib3.disable_warnings()
except (ImportError, AttributeError):  # Python3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class WebInspectScan:
    def __init__(self, overrides):
        print(overrides)
        self.scan(overrides)

    def _set_config_(self):
        self.config = WebInspectConfig()
        Logger.app.debug("Webinspect Config: {}".format(self.config))

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

        # OK, we're ready to actually do something now

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

        Logger.app.info("Launching a scan")
        # Launch the scan.

        try:
            scan_id = self.webinspect_api.create_scan()
            Logger.app.debug("Scan ID: {}".format(scan_id))



            from multiprocessing.dummy import Pool as ThreadPool

            pool = ThreadPool(1)

            # start some threads - first to finish adds to a queue and that is what we return.
            pool.imap_unordered(self._scan, scan_id)
            pool.close()
            pool.join()

            
        except (
                requests.exceptions.ConnectionError, requests.exceptions.HTTPError, TypeError, NameError, KeyError,
                IndexError) as e:
            Logger.app.error(
                # "Unable to connect to WebInspect {0}, see also: {1}".format(webinspect_settings['webinspect_url'], e))
                "WebInspect scan was not properly configured, unable to launch!! see also: {}".format(e))
            raise

        # If we've made it this far, our new credentials are valid and should be saved
        if username is not None and password is not None and not auth_config.has_auth_creds():
            auth_config.write_credentials(username, password)

        try:
            # handle_scan_event('scan_end')
            Logger.app.info("Webbreaker WebInspect has completed.")

        except (requests.exceptions.ConnectionError, requests.exceptions.HTTPError, TypeError, NameError, KeyError,
                IndexError) as e:
            Logger.app.error(
                # "Unable to connect to WebInspect {0}, see also: {1}".format(webinspect_settings['webinspect_url'], e))
                "Webbreaker WebInspect scan was unable to complete! See also: {}".format(e))
            raise

    def _scan(self, scan_id):
        scan_complete = False
        while not scan_complete:
            # Logger.app.info("inside thread :) ")
            current_status = self.webinspect_api.get_scan_status(scan_id)
            Logger.app.info("current status: ", current_status)


            if current_status.lower() == 'complete':
                scan_complete = True
                return True


        self.webinspect_api.export_scan_results(scan_id, 'fpr')
        self.webinspect_api.export_scan_results(scan_id, 'xml')
        # TODO add json export



        # if scan_id:
        #     # Initialize handle_scan_event first then go to webinspectscanhelpers
        #
        #     global handle_scan_event
        #     Logger.app.debug("handle_scan_event: {}".format(handle_scan_event))
        #     handle_scan_event = create_scan_event_handler(self.webinspect_api, scan_id, webinspect_settings)
        #     handle_scan_event('scan_start')
        #     Logger.app.debug("Starting scan handling")
        #     Logger.app.info("Execution is waiting on scan status change")
        #     with scan_running():
        #         self.webinspect_api.wait_for_scan_status_change(scan_id)  # execution waits here, blocking call
        #     status = self.webinspect_api.get_scan_status(scan_id)
        #     Logger.app.info("Scan status has changed to {0}.".format(status))
        #
        #     if status.lower() != 'complete':  # case insensitive comparison is tricky. this should be good enough for now
        #         Logger.app.error(
        #             "See the WebInspect server scan log --> {}, typically the application to be scanned is "
        #             "unavailable.".format(WebInspectConfig().endpoints))
        #         Logger.app.error('Scan is incomplete and is unrecoverable. WebBreaker will exit!!')
        #         handle_scan_event('scan_end')
        #         sys.exit(ExitStatus.failure)

# handle_scan_event = None

#
# # Use a closure for events related to scan status changes
# def create_scan_event_handler(self.webinspect_api, scan_id, webinspect_settings):
#     def scan_event_handler(event_type, external_termination=False):
#         try:
#             event = {}
#             event['scanid'] = scan_id
#             event['server'] = self.webinspect_api.setting_overrides.endpoint
#             event['scanname'] = webinspect_settings['webinspect_scan_name']
#             event['event'] = event_type
#             event['timestamp'] = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
#             event['subject'] = 'WebBreaker ' + event['event']
#
#             if webinspect_settings['webinspect_allowed_hosts']:
#                 event['targets'] = webinspect_settings['webinspect_allowed_hosts']
#             else:
#                 event['targets'] = webinspect_settings['webinspect_scan_targets']
#
#             if external_termination:
#                 self.webinspect_api.stop_scan(scan_id)
#         except Exception as e:
#             Logger.console.error("Oh no: {}".format(e))
#
#     return scan_event_handler
#
#
# # Special function here - called only when we're in a context (defined below) of intercepting process-termination
# # signals. If, while a scan is executing, WebBreaker receives a termination signal from the OS, we want to
# # handle that as a scan-end event prior to terminating. So, this function will be called by the python signal
# # handler within the scan-running context.
# def write_end_event(*args):
#     handle_scan_event('scan_end', external_termination=True)
#     os._exit(0)
#
#
# @contextmanager
# def scan_running():
#     # Intercept the "please terminate" signals
#     original_sigint_handler = getsignal(SIGINT)
#     original_sigabrt_handler = getsignal(SIGABRT)
#     original_sigterm_handler = getsignal(SIGTERM)
#     for sig in (SIGABRT, SIGINT, SIGTERM):
#         signal(sig, write_end_event)
#     try:
#         yield
#     except:
#         raise
#     finally:
#         # Go back to normal signal handling
#         signal(SIGABRT, original_sigabrt_handler)
#         signal(SIGINT, original_sigint_handler)
#         signal(SIGTERM, original_sigterm_handler)
#
#
# if __name__ == '__main__':
#     pass
#
