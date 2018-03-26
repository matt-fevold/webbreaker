#!/usr/bin/env python
# -*-coding:utf-8-*-

import json
import requests
import urllib3
from webinspectapi.webinspect import WebInspectApi
from webbreaker.common.webbreakerlogger import Logger
from webbreaker.common.webbreakerhelper import WebBreakerHelper
from webbreaker.webinspect.webinspect_config import WebInspectConfig
from webbreaker.webinspect.jit_scheduler import WebInspectJitScheduler
import webbreaker.webinspect.webinspect_json as webinspectjson
from webbreaker.common.logexceptionhelper import LogExceptionHelper
from webbreaker.webinspect.authentication import WebInspectAuth
from webbreaker.webinspect.common.webinspect_helper import WebInspectAPIHelper

import sys
from exitstatus import ExitStatus
from contextlib import contextmanager
from signal import *
import os, datetime
try:
    import urlparse as urlparse
except ImportError:
    from urllib.parse import urlparse

logexceptionhelper = LogExceptionHelper()

try:
    requests.packages.urllib3.disable_warnings()
except (ImportError, AttributeError):  # Python3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class WebInspectScan:
    def __init__(self, overrides):
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
        self.config.fetch_webinspect_configs(overrides)

        # ...and settings...
        webinspect_settings = self.config.parse_webinspect_options(overrides)

        # OK, we're ready to actually do something now

        # The webinspect client is our point of interaction with the webinspect server farm
        webinspect_client = WebInspectAPIHelper(username=username, password=password, webinspect_setting_overrides=webinspect_settings)

        # if a scan policy has been specified, we need to make sure we can find/use it
        webinspect_client.verify_scan_policy(self.config)

        # Upload whatever configurations have been provided...
        # All skipped unless explicitly declared in CLI
        if webinspect_client.setting_overrides.webinspect_upload_settings:
            webinspect_client.upload_settings()

        if webinspect_client.setting_overrides.webinspect_upload_webmacros:
            webinspect_client.upload_webmacros()

        # if there was a provided scan policy, we've already uploaded so don't bother doing it again. hack.
        if webinspect_client.setting_overrides.webinspect_upload_policy and not webinspect_client.setting_overrides.scan_policy:
            webinspect_client.upload_policy()

        Logger.app.info("Launching a scan")
        # ... And launch a scan.

        try:
            scan_id = webinspect_client.create_scan()
            Logger.app.debug("Scan ID: {}".format(scan_id))

            if scan_id:
                # Initialize handle_scan_event first then go to webinspectscanhelpers

                global handle_scan_event
                Logger.app.debug("handle_scan_event: {}".format(handle_scan_event))
                handle_scan_event = create_scan_event_handler(webinspect_client, scan_id, webinspect_settings)
                handle_scan_event('scan_start')
                Logger.app.debug("Starting scan handling")
                Logger.app.info("Execution is waiting on scan status change")
                with scan_running():
                    webinspect_client.wait_for_scan_status_change(scan_id)  # execution waits here, blocking call
                status = webinspect_client.get_scan_status(scan_id)
                Logger.app.info("Scan status has changed to {0}.".format(status))

                if status.lower() != 'complete':  # case insensitive comparison is tricky. this should be good enough for now
                    Logger.app.error(
                        "See the WebInspect server scan log --> {}, typically the application to be scanned is "
                        "unavailable.".format(WebInspectConfig().endpoints))
                    Logger.app.error('Scan is incomplete and is unrecoverable. WebBreaker will exit!!')
                    handle_scan_event('scan_end')
                    sys.exit(ExitStatus.failure)

            webinspect_client.export_scan_results(scan_id, 'fpr')
            webinspect_client.export_scan_results(scan_id, 'xml')
            # TODO add json export

        except (
                requests.exceptions.ConnectionError, requests.exceptions.HTTPError, NameError, KeyError,
                IndexError) as e:
            Logger.app.error(
                # "Unable to connect to WebInspect {0}, see also: {1}".format(webinspect_settings['webinspect_url'], e))
                "WebInspect scan was not properly configured, unable to launch!! see also: {}".format(e))
            raise

        # If we've made it this far, our new credentials are valid and should be saved
        if username is not None and password is not None and not auth_config.has_auth_creds():
            auth_config.write_credentials(username, password)

        try:
            handle_scan_event('scan_end')
            Logger.app.info("Webbreaker WebInspect has completed.")

        except (requests.exceptions.ConnectionError, requests.exceptions.HTTPError, TypeError, NameError, KeyError,
                IndexError) as e:
            Logger.app.error(
                # "Unable to connect to WebInspect {0}, see also: {1}".format(webinspect_settings['webinspect_url'], e))
                "Webbreaker WebInspect scan was unable to complete! See also: {}".format(e))
            raise


handle_scan_event = None


# Use a closure for events related to scan status changes
def create_scan_event_handler(webinspect_client, scan_id, webinspect_settings):
    def scan_event_handler(event_type, external_termination=False):
        try:
            event = {}
            event['scanid'] = scan_id
            event['server'] = webinspect_client.setting_overrides.url
            event['scanname'] = webinspect_settings['webinspect_scan_name']
            event['event'] = event_type
            event['timestamp'] = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
            event['subject'] = 'WebBreaker ' + event['event']

            if webinspect_settings['webinspect_allowed_hosts']:
                event['targets'] = webinspect_settings['webinspect_allowed_hosts']
            else:
                event['targets'] = webinspect_settings['webinspect_scan_targets']

            if external_termination:
                webinspect_client.stop_scan(scan_id)
        except Exception as e:
            Logger.console.error("Oh no: {}".format(e.message))

    return scan_event_handler


# Special function here - called only when we're in a context (defined below) of intercepting process-termination
# signals. If, while a scan is executing, WebBreaker receives a termination signal from the OS, we want to
# handle that as a scan-end event prior to terminating. So, this function will be called by the python signal
# handler within the scan-running context.
def write_end_event(*args):
    handle_scan_event('scan_end', external_termination=True)
    os._exit(0)


@contextmanager
def scan_running():
    # Intercept the "please terminate" signals
    original_sigint_handler = getsignal(SIGINT)
    original_sigabrt_handler = getsignal(SIGABRT)
    original_sigterm_handler = getsignal(SIGTERM)
    for sig in (SIGABRT, SIGINT, SIGTERM):
        signal(sig, write_end_event)
    try:
        yield
    except:
        raise
    finally:
        # Go back to normal signal handling
        signal(SIGABRT, original_sigabrt_handler)
        signal(SIGINT, original_sigint_handler)
        signal(SIGTERM, original_sigterm_handler)