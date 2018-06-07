#!/usr/bin/env python
# -*- coding: utf-8 -*-


from webbreaker.common.webbreakerlogger import Logger
from webbreaker.webinspect.authentication import WebInspectAuth
from webbreaker.webinspect.common.helper import WebInspectAPIHelper
from webbreaker.webinspect.common.loghelper import WebInspectLogHelper

webinspect_logexceptionhelper = WebInspectLogHelper()

class WebInspectDownload:
    def __init__(self, server, scan_name, scan_id, extension, username, password):
        self.download(server, scan_name, scan_id, extension, username, password)

    @staticmethod
    def download(server, scan_name, scan_id, extension, username, password):
        try:
            auth_config = WebInspectAuth()
            username, password = auth_config.authenticate(username, password)

            query_client = WebInspectAPIHelper(host=server, username=username, password=password)

            if not scan_id:
                results = query_client.get_scan_by_name(scan_name)
                if len(results) == 0:
                    webinspect_logexceptionhelper.log_error_no_scans_found(scan_name)
                elif len(results) == 1:
                    scan_id = results[0]['ID']
                    Logger.app.info("Scan matching the name {} found.".format(scan_name))
                    Logger.app.info("Downloading scan {}".format(scan_name))
                    query_client.export_scan_results(scan_id, extension, scan_name)
                else:
                    webinspect_logexceptionhelper.log_info_multiple_scans_found(scan_name)
                    print("{0:80} {1:40} {2:10}".format('Scan Name', 'Scan ID', 'Scan Status'))
                    print("{0:80} {1:40} {2:10}\n".format('-' * 80, '-' * 40, '-' * 10))
                    for result in results:
                        print("{0:80} {1:40} {2:10}".format(result['Name'], result['ID'], result['Status']))
            else:
                if query_client.get_scan_status(scan_id):
                    query_client.export_scan_results(scan_id, extension, scan_name)

                else:
                    if query_client.get_scan_status(scan_id):
                        query_client.export_scan_results(scan_id, extension, scan_name)
                    else:
                        Logger.console.error("Unable to find scan with ID matching {}".format(scan_id))

        except (UnboundLocalError, TypeError) as e:
            webinspect_logexceptionhelper.log_error_webinspect_download(e)

        # If we've made it this far, our new credentials are valid and should be saved
        if username is not None and password is not None and not auth_config.has_auth_creds():
            auth_config.write_credentials(username, password)
