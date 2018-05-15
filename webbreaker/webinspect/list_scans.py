#!/usr/bin/env python
# -*-coding:utf-8-*-

from webbreaker.webinspect.authentication import WebInspectAuth
from webbreaker.webinspect.common.helper import WebInspectAPIHelper
from webbreaker.webinspect.webinspect_config import WebInspectConfig
from webbreaker.common.webbreakerlogger import Logger


class WebInspectListScans:
    def __init__(self, scan_name, server, username, password):
        self.list_scans(scan_name, server, username, password)

    @staticmethod
    def list_scans(scan_name, server, username, password):
        if server:  # if any cli servers were passed.
            servers = []
            for s in server:
                servers.append(s)
        else:
            servers = [(e[0]) for e in WebInspectConfig().endpoints]

        auth_config = WebInspectAuth()
        username, password = auth_config.authenticate(username, password)

        for server in servers:
            query_client = WebInspectAPIHelper(host=server, username=username,
                                               password=password)
            if scan_name:
                results = query_client.get_scan_by_name(scan_name)
                if results and len(results):
                    print("Scans matching the name {} found on {}".format(scan_name, server))
                    print("{0:80} {1:40} {2:10}".format('Scan Name', 'Scan ID', 'Scan Status'))
                    print("{0:80} {1:40} {2:10}\n".format('-' * 80, '-' * 40, '-' * 10))
                    for match in results:
                        print("{0:80} {1:40} {2:10}".format(match['Name'], match['ID'], match['Status']))
                else:
                    Logger.app.error("No scans matching the name {} were found on {}".format(scan_name, server))

            else:
                results = query_client.list_scans()
                if results and len(results):
                    print("Scans found on {}".format(server))
                    print("{0:80} {1:40} {2:10}".format('Scan Name', 'Scan ID', 'Scan Status'))
                    print("{0:80} {1:40} {2:10}\n".format('-' * 80, '-' * 40, '-' * 10))
                    for scan in results:
                        print("{0:80} {1:40} {2:10}".format(scan['Name'], scan['ID'], scan['Status']))
                else:
                    print("No scans found on {}".format(server))
            print('\n\n\n')
        # If we've made it this far, our new credentials are valid and should be saved
        if username is not None and password is not None and not auth_config.has_auth_creds():
            auth_config.write_credentials(username, password)
