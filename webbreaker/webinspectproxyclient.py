#!/usr/bin/env python
# -*-coding:utf-8-*-

import webinspectapi.webinspect as webinspectapi
from webbreaker.webinspectconfig import WebInspectConfig
from webbreaker.webbreakerlogger import Logger
from webbreaker.confighelper import Config


class WebinspectProxyClient(object):
    def __init__(self, host, proxy_name, port):
        if proxy_name is None:
            self.proxy_name = ""
        else:
            self.proxy_name = proxy_name

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
        response = api.start_proxy(self.proxy_name, self.port, self.host)
        print(response.data)
        if response.success:
            return response.data
        else:
            Logger.app.critical("{}".format(response.message))

    def delete_proxy(self):

        api = webinspectapi.WebInspectApi(self.host, verify_ssl=False)
        response = api.delete_proxy(self.proxy_name)
        if response.success:
            Logger.app.info("Successfully deleted proxy: {}".format(self.proxy_name))
        else:
            Logger.app.critical("{}".format(response.message))

    def list_proxy(self):
        api = webinspectapi.WebInspectApi(self.host, verify_ssl=False)
        response = api.list_proxies()
        if response.success:
            return response.data
        else:
            Logger.app.critical("{}".format(response.message))
