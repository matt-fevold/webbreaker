#!/usr/bin/env python
# -*-coding:utf-8-*-

import json
import webbreaker.webinspect as webinspectapi
from webbreaker.webinspectconfig import WebInspectConfig
from webbreaker.webbreakerlogger import Logger
from webbreaker.confighelper import Config
import http.client


class WebinspectProxyClient(object):
    def __init__(self, host, proxy_id, port):
        if proxy_id is None:
            self.proxy_id = ""
        else:
            self.proxy_id = proxy_id

        if port is None:
            self.port = ""
        else:
            self.port = port

        if host:
            self.host = host
        else:
            # Make random like webinspect config
            self.host = WebInspectConfig().endpoints[0][0]

    def get_cert_proxy(self):
        path = Config().cert

        api = webinspectapi.WebInspectApi(self.host, verify_ssl=False)
        response = api.cert_proxy()
        if response.success:
            try:
                with open(path, 'wb') as f:
                    f.write(response.data)
                    Logger.app.info('Cert has downloaded to\t:\t{}'.format(path))
            except UnboundLocalError as e:
                Logger.app.error('Error saving cert locally {}'.format(e))
        else:
            Logger.app.error('Unable to retrieve cert.\n ERROR: {} '.format(response.message))

    def start_proxy(self):

        api = webinspectapi.WebInspectApi(self.host, verify_ssl=False)
        response = api.start_proxy(self.proxy_id, self.port, self.host)
        print(response.data)
        if response.success:
            return response.data
        else:
            Logger.app.critical("{}".format(response.message))

    def delete_proxy(self):

        api = webinspectapi.WebInspectApi(self.host, verify_ssl=False)
        response = api.delete_proxy(self.proxy_id)
        if response.success:
            Logger.app.info("Successfully deleted proxy: {}".format(self.proxy_id))
        else:
            Logger.app.critical("{}".format(response.message))

    def list_proxy(self):
        api = webinspectapi.WebInspectApi(self.host, verify_ssl=False)
        response = api.list_proxies()
        if response.success:
            return response.data
        else:
            Logger.app.critical("{}".format(response.message))

    def get_scan_by_name(self, scan_name):
        """
        Search Webinspect server for a scan matching scan_name
        :param scan_name:
        :return: List of search results
        """
        api = webinspectapi.WebInspectApi(self.host, verify_ssl=False)
        return api.get_scan_by_name(scan_name).data

    def export_scan_results(self, scan_id, scan_name, extension):
        """
        Download scan as a xml for Threadfix or other Vuln Management System
        :param scan_id:
        :param scan_name:
        :param extension:
        """
        Logger.app.debug('Exporting scan: {}'.format(scan_id))
        detail_type = 'Full' if extension == 'xml' else None
        api = webinspectapi.WebInspectApi(self.host, verify_ssl=False)
        response = api.export_scan_format(scan_id, extension, detail_type)

        if response.success:
            try:
                with open('{0}.{1}'.format(scan_name, extension), 'wb') as f:
                    Logger.app.info('Scan results file is available: {0}.{1}'.format(scan_name, extension))
                    f.write(response.data)
            except UnboundLocalError as e:
                Logger.app.error('Error saving file locally {}'.format(e))
        else:
            Logger.app.error('Unable to retrieve scan results. {} '.format(response.message))

    def list_scans(self):
        """
        List all scans found on host
        :return: response.data from the Webinspect server
        """
        api = webinspectapi.WebInspectApi(self.host, verify_ssl=False)
        response = api.list_scans()
        if response.success:
            return response.data
        else:
            Logger.app.critical("{}".format(response.message))

    def get_scan_status(self, scan_guid):
        """
        Get scan status from the Webinspect server
        :param scan_guid:
        :return: Current status of scan
        """
        api = webinspectapi.WebInspectApi(self.host, verify_ssl=False)
        try:
            response = api.get_current_status(scan_guid)
            status = json.loads(response.data_json())['ScanStatus']
            return status
        except (ValueError, TypeError, UnboundLocalError) as e:
            Logger.app.error("get_scan_status failed: {}".format(e))
            return None
