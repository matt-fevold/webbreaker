#!/usr/bin/env python
# -*-coding:utf-8-*-

import random
import string
from webinspectapi.webinspect import WebInspectApi
from webbreaker.common.webbreakerlogger import Logger
from webbreaker.common.confighelper import Config
from exitstatus import ExitStatus
import sys
from webbreaker.common.api_response_helper import APIHelper
from webbreaker.webinspect.authentication import WebInspectAuth
from webbreaker.webinspect.webinspect_config import WebInspectConfig
# import webbreaker.webinspect.jit_scheduler
from webbreaker.webinspect.jit_scheduler import WebInspectJitScheduler

class WebInspectProxy:
    def __init__(self, download, list, port, proxy_name, setting, server, start, stop, upload, webmacro, username,
                 password):
        # Init Variables
        auth_config = WebInspectAuth()
        if server:
            servers = [server]
        else:
            servers = [(e[0]) for e in WebInspectConfig().endpoints]

        # Class Variables
        self.proxy_name = proxy_name
        self.username, self.password = auth_config.authenticate(username, password)
        if port:
            self.port = port
        else:
            self.port = ""

        self.proxy(list, start, stop, download, upload, webmacro, setting, servers)
        auth_config.write_credentials(self.username, self.password)

    def proxy(self, list, start, stop, download, upload, webmacro, setting, servers):
        """
        WebInspect Proxy Command Logic. Using the flag parameters WebInspect Proxy will determine which command to run.

        :param list: Used to determine to run `_list_proxy` or not. It will list all proxies on all servers.
        :param start: Used to determine to run `_start_proxy` or not. If no server was specified it will start the
                      proxy on the first server from the configuration file.
        :param stop: Used to determine to run `_stop_proxy` or not. `self.proxy_name` must be set. It will download
                     the webmacro & setting before deleting the proxy.
        :param download: Used to determine to run `_download_proxy` or not. `self.proxy_name` must be set & either
                         `webmacro` or `setting`. It will then download either the webmacro or setting from the proxy.
        :param upload: File to upload to WebInspect Proxy. If a file is specified that is all that is necessary
                       to run `_upload_proxy`.
        :param webmacro: Boolean flag used in determining what to download from proxy. See `_download_proxy`
        :param setting: Boolean flag used in determining what to download from proxy. See `_download_proxy`
        :param servers: List of servers that is either a singleton list of the specfied server or a list of servers from
                        the configuration file.
        :return: Nothing will be returned.
        """
        try:

            if start:

                server = self.get_endpoint()

                self._get_proxy_certificate(server)
                result = self._start_proxy(server)
                if result and len(result):
                    Logger.app.info("Proxy successfully started")
                    print("Server\t\t:\t'{}'".format(server))
                    print("Proxy Name\t:\t{}".format(result['instanceId']))
                    print("Proxy Address\t:\t{}".format(result['address']))
                    print("Proxy Port\t:\t{}".format(result['port']))
                else:
                    Logger.app.error("Unable to start proxy on '{}'".format(server))
                    sys.exit(ExitStatus.failure)

            elif list:
                for server in servers:
                    results = self._list_proxy(server)
                    if results and len(results):
                        print("Proxies found on {}".format(server))
                        print("{0:80} {1:40} {2:10}".format('Scan Name', 'Scan ID', 'Scan Status'))
                        print("{0:80} {1:40} {2:10}\n".format('-' * 80, '-' * 40, '-' * 10))
                        for match in results:
                            print("{0:80} {1:40} {2:10}".format(match['instanceId'], match['address'], match['port']))
                        Logger.app.info("Successfully listed proxies from: '{}'".format(server))
                    else:
                        Logger.app.error("No proxies found on '{}'".format(server))

            # For `stop, download & upload` a proxy name is required
            elif not self.proxy_name:
                Logger.app.error("Please enter a proxy name.")
                sys.exit(ExitStatus.failure)

            elif upload:
                for server in servers:
                    if self._verify_proxy_server(server):
                        self._upload_proxy(upload, server)
                        sys.exit(ExitStatus.success)
                Logger.app.error("Proxy: '{}' not found on any server.".format(self.proxy_name))
                sys.exit(ExitStatus.failure)

            elif stop:
                for server in servers:
                    if self._verify_proxy_server(server):
                        self._download_proxy(webmacro=False, setting=True, server=server)
                        self._download_proxy(webmacro=True, setting=False, server=server)
                        self._delete_proxy(server)
                        sys.exit(ExitStatus.success)
                Logger.app.error("Proxy: '{}' not found on any server.".format(self.proxy_name))
                sys.exit(ExitStatus.failure)

            elif download:
                for server in servers:
                    if self._verify_proxy_server(server):
                        self._download_proxy(webmacro, setting, server)
                        sys.exit(ExitStatus.success)
                Logger.app.error("Proxy: '{}' not found on any server.".format(self.proxy_name))
                sys.exit(ExitStatus.failure)
            else:
                Logger.app.error("Error: No proxy command was given.")
                sys.exit(ExitStatus.failure)

        except (UnboundLocalError, EnvironmentError) as e:
            Logger.app.critical("Incorrect WebInspect configurations found!! {}".format(e))
            sys.exit(ExitStatus.failure)

    def get_endpoint(self):
        jit_scheduler = WebInspectJitScheduler(username=self.username,
                                                                                   password=self.password)
        Logger.app.info("Querying WebInspect scan engines for availability.")

        endpoint = jit_scheduler.get_endpoint()
        return endpoint

    def _get_proxy_certificate(self, server):
        path = Config().cert
        api = WebInspectApi(server, verify_ssl=False, username=self.username, password=self.password)

        response = api.cert_proxy()
        APIHelper().check_for_response_errors(response)

        try:
            with open(path, 'wb') as f:
                f.write(response.data)
                Logger.app.info('Certificate has downloaded to\t:\t{}'.format(path))
        except UnboundLocalError as e:
            Logger.app.error('Error saving certificate locally {}'.format(e))

    def _start_proxy(self, server):
        if self.proxy_name is None:
            self._generate_random_proxy_name()
        api = WebInspectApi(server, verify_ssl=False, username=self.username, password=self.password)

        response = api.start_proxy(self.proxy_name, self.port, "")
        APIHelper().check_for_response_errors(response)

        return response.data

    def _delete_proxy(self, server):
        api = WebInspectApi(server, verify_ssl=False, username=self.username, password=self.password)

        response = api.delete_proxy(self.proxy_name)
        APIHelper().check_for_response_errors(response)

        Logger.app.info("Proxy: '{0}' deleted from '{1}'".format(self.proxy_name, server))

    def _list_proxy(self, server):
        if self.proxy_name is None:
            self._generate_random_proxy_name()
        api = WebInspectApi(server, verify_ssl=False, username=self.username, password=self.password)

        response = api.list_proxies()
        APIHelper().check_for_response_errors(response)
        return response.data

    def _download_proxy(self, webmacro, setting, server):

        api = WebInspectApi(server, verify_ssl=False, username=self.username, password=self.password)

        if webmacro:
            response = api.download_proxy_webmacro(self.proxy_name)
            extension = 'webmacro'
        elif setting:
            response = api.download_proxy_setting(self.proxy_name)
            extension = 'xml'
        else:
            Logger.app.error("Please enter a file type to download.")
            sys.exit(ExitStatus.failure)

        APIHelper().check_for_response_errors(response)

        try:
            with open('{0}-proxy.{1}'.format(self.proxy_name, extension), 'wb') as f:
                Logger.app.info('Scan results file is available: {0}-proxy.{1}'.format(self.proxy_name, extension))
                f.write(response.data)
        except UnboundLocalError as e:
            Logger.app.error('Error saving file locally {}'.format(e))
            sys.exit(ExitStatus.failure)

    def _upload_proxy(self, upload_file, server):
        try:
            api = WebInspectApi(server, verify_ssl=False, username=self.username, password=self.password)
            response = api.upload_webmacro_proxy(self.proxy_name, upload_file)
            APIHelper().check_for_response_errors(response)

            Logger.app.info("Uploaded '{0}' to '{1}' on: {2}.".format(upload_file, self.proxy_name, server))

        except (ValueError, UnboundLocalError) as e:
            Logger.app.error("Error uploading policy {}".format(e))
            sys.exit(ExitStatus.failure)

    def _verify_proxy_server(self, server):
        api = WebInspectApi(server, verify_ssl=False, username=self.username, password=self.password)
        response = api.get_proxy_information(self.proxy_name)
        APIHelper().check_for_response_errors(response)

        return response.data

    def _generate_random_proxy_name(self):
        self.proxy_name = "webinspect" + "-" + "".join(
            random.choice(string.ascii_uppercase + string.digits) for _ in range(5))


if __name__ == '__main__':
    WebInspectProxy(False, False, None, None, False, None, True, False, None, False, None, None)
