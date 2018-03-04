#!/usr/bin/env python
# -*-coding:utf-8-*-

import json
import ntpath
import requests
import urllib3
from webinspectapi.webinspect import WebInspectApi
from webbreaker.webbreakerlogger import Logger
from webbreaker.webbreakerhelper import WebBreakerHelper
from webbreaker.webinspectconfig import WebInspectConfig
from webbreaker.webinspectjitscheduler import WebInspectJitScheduler
import webbreaker.webinspectjson as webinspectjson
from webbreaker.logexceptionhelper import LogExceptionHelper
import sys
from exitstatus import ExitStatus

logexceptionhelper = LogExceptionHelper()

try:
    requests.packages.urllib3.disable_warnings()
except (ImportError, AttributeError):  # Python3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class WebinspectClient(object):
    def __init__(self, webinspect_setting, username=None, password=None):
        try:
            Logger.app.debug("Starting WebInspect client initialization")

            config = WebInspectConfig()
            lb = WebInspectJitScheduler(endpoints=config.endpoints,
                                        size_list=config.sizing,
                                        size_needed=webinspect_setting['webinspect_scan_size'], username=username, password=password)
            Logger.app.info("Querying WebInspect scan engines for availability.")
            endpoint = lb.get_endpoint()

            if not endpoint:
                raise EnvironmentError("Scheduler found no available endpoints.")

            self.username = username
            self.password = password
            self.url = endpoint
            self.settings = webinspect_setting['webinspect_settings']
            self.scan_name = webinspect_setting['webinspect_scan_name']
            self.webinspect_upload_settings = webinspect_setting['webinspect_upload_settings']
            self.webinspect_upload_policy = webinspect_setting['webinspect_upload_policy']
            self.webinspect_upload_webmacros = webinspect_setting['webinspect_upload_webmacros']
            self.scan_mode = webinspect_setting['webinspect_overrides_scan_mode']
            self.scan_scope = webinspect_setting['webinspect_overrides_scan_scope']
            self.login_macro = webinspect_setting['webinspect_overrides_login_macro']
            self.scan_policy = webinspect_setting['webinspect_overrides_scan_policy']
            self.scan_start = webinspect_setting['webinspect_overrides_scan_start']
            self.start_urls = webinspect_setting['webinspect_overrides_start_urls']
            self.workflow_macros = webinspect_setting['webinspect_workflow_macros']
            self.allowed_hosts = webinspect_setting['webinspect_allowed_hosts']
            self.scan_size = webinspect_setting['webinspect_scan_size']
            self.runenv = WebBreakerHelper.check_run_env()

            Logger.app.debug("Completed webinspect client initialization")
            Logger.app.debug("url: {}".format(self.url))
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
        except (UnboundLocalError, EnvironmentError, NameError, TypeError) as e:
            logexceptionhelper.LogIncorrectWebInspectConfigs(e)
            raise


    def __settings_exists__(self):
        try:
            api = WebInspectApi(self.url, verify_ssl=False, username=self.username, password=self.password)
            response = api.list_settings()
            if response.response_code == 401:
                Logger.app.critical("An Authorization Error occured.")
                sys.exit(ExitStatus.failure)
            if response.success:
                for setting in response.data:
                    if setting in self.settings:
                        return True

        except (ValueError, UnboundLocalError) as e:
            Logger.app.error("Unable to determine if setting file exists, scan will continue without setting!"
                             "Error: {}".format(e))
        return False

    def create_scan(self):
        """
        Launches and monitors a scan
        :return: If scan was able to launch, scan_id. Otherwise none.
        """
        try:
            Logger.app.debug("Creating Scan in webinspect client")
            overrides = json.dumps(webinspectjson.formatted_settings_payload(self.settings, self.scan_name, self.runenv,
                                                                             self.scan_mode, self.scan_scope,
                                                                             self.login_macro,
                                                                             self.scan_policy, self.scan_start,
                                                                             self.start_urls, self.workflow_macros,
                                                                             self.allowed_hosts))

            api = WebInspectApi(self.url, verify_ssl=False, username=self.username, password=self.password)
            response = api.create_scan(overrides)

            if response.response_code == 401:
                Logger.app.critical("An Authorization Error occured.")
                sys.exit(ExitStatus.failure)
            logger_response = json.dumps(response, default=lambda o: o.__dict__, sort_keys=True)
            Logger.app.debug("Request sent to {0}:\n{1}".format(self.url, overrides))
            Logger.app.debug("Response from {0}:\n{1}\n".format(self.url, logger_response))

            if response.success:
                scan_id = response.data['ScanId']
                sys.stdout.write(str('WebInspect scan launched on {0} your scan id: {1}\n'.format(self.url, scan_id)))
            else:
                Logger.app.error("No scan was launched!\n {}".format(response.message))
                sys.exit(ExitStatus.failure)
            return scan_id

        except (ValueError, UnboundLocalError) as e:
            Logger.app.error("Creating the WebInspect scan failed! {}".format(e))

    def export_scan_results(self, scan_id, extension):
        """
        Save scan results to file
        :param scan_id:
        :param extension:
        :return:
        """
        # Export scan as a xml for Threadfix or other Vuln Management System
        Logger.app.info('Exporting scan: {} as {}'.format(scan_id, extension))
        detail_type = 'Full' if extension == 'xml' else None
        api = WebInspectApi(self.url, verify_ssl=False, username=self.username, password=self.password)
        response = api.export_scan_format(scan_id, extension, detail_type)
        if response.response_code == 401:
            Logger.app.critical("An authentication error occurred, exporting scan results!")
            sys.exit(ExitStatus.failure)
        if response.success:
            try:
                with open('{0}.{1}'.format(self.scan_name, extension), 'wb') as f:
                    Logger.app.debug(str('Scan results file is available: {0}.{1}\n'.format(self.scan_name, extension)))
                    f.write(response.data)
                    print(str('Scan results file is available: {0}.{1}\n'.format(self.scan_name, extension)))
            except UnboundLocalError as e:
                Logger.app.error('Error saving file locally! {}'.format(e))
        else:
            Logger.app.error('Unable to retrieve scan results! {} '.format(response.message))

    def get_policy_by_guid(self, policy_guid):
        api = WebInspectApi(self.url, verify_ssl=False, username=self.username, password=self.password)
        response = api.get_policy_by_guid(policy_guid)
        if response.response_code == 401:
            Logger.app.critical("An authentication error occurred, retriving policy identifier!")
            sys.exit(ExitStatus.failure)
        if response.success:
            return response.data
        else:
            return None

    def get_policy_by_name(self, policy_name):
        api = WebInspectApi(self.url, verify_ssl=False, username=self.username, password=self.password)
        response = api.get_policy_by_name(policy_name)
        if response.response_code == 401:
            Logger.app.critical("An authentication error occured, retrieving the policy name!")
            sys.exit(ExitStatus.failure)
        if response.success:
            return response.data
        else:
            return None

    def get_scan_issues(self, scan_name=None, scan_guid=None, pretty=False):
        try:

            if scan_name:
                api = WebInspectApi(self.url, verify_ssl=False, username=self.username, password=self.password)
                response = api.get_scan_by_name(scan_name)
                if response.response_code == 401:
                    Logger.app.critical("An authentication error occurred, retrieving scan issues!")
                    sys.exit(ExitStatus.failure)
                if response.success:
                    scan_guid = response.data[0]['ID']
                else:
                    Logger.app.error(response.message)
                    return None

            api = WebInspectApi(self.url, verify_ssl=False, username=self.username, password=self.password)
            response = api.get_scan_issues(scan_guid)
            if response.response_code == 401:
                Logger.app.critical("An authentication error occurred!")
                sys.exit(ExitStatus.failure)
            if response.success:
                return response.data_json(pretty=True)
            else:
                return None
        except (ValueError, UnboundLocalError) as e:
            Logger.app.error("There was an error getting scan issues: {}".format(e))

    def get_scan_log(self, scan_name=None, scan_guid=None):
        try:

            if scan_name:
                api = WebInspectApi(self.url, verify_ssl=False, username=self.username, password=self.password)
                response = api.get_scan_by_name(scan_name)
                if response.response_code == 401:
                    Logger.app.critical("An an authentication error occurred while retrieving scan name!")
                    sys.exit(ExitStatus.failure)
                if response.success:
                    scan_guid = response.data[0]['ID']
                else:
                    Logger.app.error(response.message)
                    return None

            api = WebInspectApi(self.url, verify_ssl=False, username=self.username, password=self.password)
            response = api.get_scan_log(scan_guid)
            if response.response_code == 401:
                Logger.app.critical("An authentication error occurred while reading the scan log!")
                sys.exit(ExitStatus.failure)
            if response.success:
                return response.data_json()
            else:
                return None
        except (ValueError, UnboundLocalError) as e:
            Logger.app.error("get_scan_log failed: {}".format(e))

    def get_scan_status(self, scan_guid):
        api = WebInspectApi(self.url, verify_ssl=False, username=self.username, password=self.password)
        try:
            response = api.get_current_status(scan_guid)
            if response.response_code == 401:
                Logger.app.critical("An Authorization Error occured.")
                sys.exit(ExitStatus.failure)
            status = json.loads(response.data_json())['ScanStatus']
            return status
        except (ValueError, UnboundLocalError, TypeError) as e:
            Logger.app.error("get_scan_status failed: {}".format(e))
            return "Unknown"

    def list_policies(self):
        try:
            api = WebInspectApi(self.url, verify_ssl=False, username=self.username, password=self.password)
            response = api.list_policies()
            if response.response_code == 401:
                Logger.app.critical("An Authorization Error occured.")
                sys.exit(ExitStatus.failure)
            if response.success:
                for policy in response.data:
                    Logger.console.info("{}".format(policy))
            else:
                Logger.app.error("{}".format(response.message))

        except (ValueError, UnboundLocalError) as e:
            Logger.app.error("list_policies failed: {}".format(e))

    def list_scans(self):

        try:
            api = WebInspectApi(self.url, verify_ssl=False, username=self.username, password=self.password)
            response = api.list_scans()
            if response.response_code == 401:
                Logger.app.critical("An Authorization Error occured.")
                sys.exit(ExitStatus.failure)
            if response.success:
                for scan in response.data:
                    Logger.console.info("{}".format(scan))
            else:
                Logger.app.error("{}".format(response.message))

        except (ValueError, UnboundLocalError) as e:
            Logger.app.error("list_scans failed: {}".format(e))

    def list_webmacros(self):
        try:
            api = WebInspectApi(self.url, verify_ssl=False, username=self.username, password=self.password)
            response = api.list_webmacros()
            if response.response_code == 401:
                Logger.app.critical("An Authorization Error occured.")
                sys.exit(ExitStatus.failure)
            if response.success:
                for webmacro in response.data:
                    Logger.console.info("{}".format(webmacro))
            else:
                Logger.app.error("{}".format(response.message))

        except (ValueError, UnboundLocalError) as e:
            Logger.app.error("list_webmacros failed: {}".format(e))

    def policy_exists(self, policy_guid):
        # true if policy exists
        api = WebInspectApi(self.url, verify_ssl=False, username=self.username, password=self.password)
        response = api.get_policy_by_guid(policy_guid)
        if response.response_code == 401:
            Logger.app.critical("An Authorization Error occured.")
            sys.exit(ExitStatus.failure)
        return response.success

    def stop_scan(self, scan_guid):
        api = WebInspectApi(self.url, verify_ssl=False, username=self.username, password=self.password)
        response = api.stop_scan(scan_guid)
        if response.response_code == 401:
            Logger.app.critical("An Authorization Error occured.")
            sys.exit(ExitStatus.failure)
        return response.success

    def upload_policy(self):
        # if a policy of the same name already exists, delete it prior to upload
        try:
            api = WebInspectApi(self.url, verify_ssl=False, username=self.username, password=self.password)
            # bit of ugliness here. I'd like to just have the policy name at this point but I don't
            # so find it in the full path
            # TODO: Verify split here
            response = api.get_policy_by_name(ntpath.basename(self.webinspect_upload_policy).split('.')[0])
            if response.response_code == 401:
                Logger.app.critical("An Authorization Error occured.")
                sys.exit(ExitStatus.failure)
            if response.success and response.response_code == 200:  # the policy exists on the server already
                api = webinspectapi.WebInspectApi(self.url, verify_ssl=False, username=self.username, password=self.password)
                response = api.delete_policy(response.data['uniqueId'])
                if response.success:
                    Logger.app.debug("Deleted policy {} from server".format(
                        ntpath.basename(self.webinspect_upload_policy).split('.')[0]))
        except (ValueError, UnboundLocalError, TypeError) as e:
            Logger.app.error("Verify if deletion of existing policy failed: {}".format(e))

        try:
            api = WebInspectApi(self.url, verify_ssl=False, username=self.username, password=self.password)
            response = api.upload_policy(self.webinspect_upload_policy)
            if response.response_code == 401:
                Logger.app.critical("An Authorization Error occured.")
                sys.exit(ExitStatus.failure)
            if response.success:
                Logger.console.debug("Uploaded policy {} to server.".format(self.webinspect_upload_policy))
            else:
                Logger.app.error("Error uploading policy {0}. {1}".format(self.webinspect_upload_policy,
                                                                          response.message))

        except (ValueError, UnboundLocalError, TypeError, NameError) as e:
            logexceptionhelper.LogErrorUploading("policy", e)
            logexceptionhelper.LogNoWebInspectServerFound(e)

    def upload_settings(self):

        try:
            api = WebInspectApi(self.url, verify_ssl=False, username=self.username, password=self.password)
            response = api.upload_settings(self.webinspect_upload_settings)
            if response.response_code == 401:
                Logger.app.critical("An Authorization Error occured.")
                sys.exit(ExitStatus.failure)
            if response.success:
                Logger.console.debug("Uploaded settings {} to server.".format(self.webinspect_upload_settings))
            else:
                Logger.app.error(
                    "Error uploading settings {0}. \nResponse Message: {1}".format(self.webinspect_upload_settings,
                                                                                   response.message))

        except (ValueError, UnboundLocalError, NameError) as e:
            logexceptionhelper.LogErrorUploading("settings", e)
            logexceptionhelper.LogNoWebInspectServerFound(e)

    def upload_webmacros(self):
        try:
            for webmacro in self.webinspect_upload_webmacros:
                api = WebInspectApi(self.url, verify_ssl=False, username=self.username, password=self.password)
                response = api.upload_webmacro(webmacro)
                if response.response_code == 401:
                    Logger.app.critical("An Authorization Error occured.")
                    sys.exit(ExitStatus.failure)
                if response.success:
                    Logger.console.debug("Uploaded webmacro {} to server.".format(webmacro))
                else:
                    Logger.app.error("Error uploading webmacro {0}. {1}".format(webmacro, response.message))

        except (ValueError, UnboundLocalError) as e:
            logexceptionhelper.LogErrorUploading("webmacro", e)
            logexceptionhelper.LogNoWebInspectServerFound(e)

    def wait_for_scan_status_change(self, scan_id):
        """
        Blocking call, will remain in this method until status of scan changes
        :param scan_id:
        :return:
        """
        # WebInspect Scan has started, wait here until it's done
        api = WebInspectApi(self.url, verify_ssl=False, username=self.username, password=self.password)
        response = api.wait_for_status_change(scan_id)  # this line is the blocker
        if response.response_code == 401:
            Logger.app.critical("An Authorization Error occured.")
            sys.exit(ExitStatus.failure)
        if response.success:
            Logger.console.debug('Scan status {}'.format(response.data))
        else:
            Logger.app.debug('Scan status not known because: {}'.format(response.message))

    def verify_scan_policy(self, config):
        try:
            if self.scan_policy:
                # two happy paths: either the provided policy refers to an existing builtin policy, or it refers to
                # a local policy we need to first upload and then use.

                if str(self.scan_policy).lower() in [str(x[0]).lower() for x in
                                                     config.mapped_policies]:
                    idx = [x for x, y in enumerate(config.mapped_policies) if
                           y[0] == str(self.scan_policy).lower()]
                    policy_guid = config.mapped_policies[idx[0]][1]
                    Logger.app.info(
                        "scan_policy {} with policyID {} has been selected.".format(self.scan_policy,
                                                                                    policy_guid))
                    Logger.app.info("Checking to make sure a policy with that ID exists in WebInspect.")
                    if not self.policy_exists(policy_guid):
                        Logger.app.error(
                            "Scan policy {} cannot be located on the WebInspect server. Stopping".format(
                                self.scan_policy))
                        sys.exit(ExitStatus.failure)
                    else:
                        Logger.app.info("Found policy {} in WebInspect.".format(policy_guid))
                else:
                    # Not a builtin. Assume that caller wants the provided policy to be uploaded
                    Logger.app.info("Provided scan policy is not built-in, so will assume it needs to be uploaded.")
                    self.upload_policy()
                    policy = self.get_policy_by_name(self.scan_policy)
                    if policy:
                        policy_guid = policy['uniqueId']
                    else:
                        Logger.app.error("The policy name is either incorrect or not available in {}."
                                         .format('.webbreaker/etc/webinspect/policies'))
                        sys.exit(ExitStatus.failure)

                # Change the provided policy name into the corresponding policy id for scan creation.
                policy_id = self.get_policy_by_guid(policy_guid)['id']
                self.scan_policy = policy_id
                Logger.app.debug("New scan policy has been set")

            else:
                Logger.app.debug("No WebInspect Scan Override Policy was selected: {}!".format
                                 (self.scan_policy))

        except (UnboundLocalError, NameError) as e:
            logexceptionhelper.LogNoWebInspectServerFound(e)
