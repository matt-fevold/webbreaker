#!/usr/bin/env python
# -*-coding:utf-8-*-

import webinspectapi.webinspect as webinspectapi
from webbreaker.webinspectconfig import WebInspectConfig
from webbreaker.webbreakerlogger import Logger
from webbreaker.confighelper import Config


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
