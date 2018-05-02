#!/usr/bin/env python
# -*- coding: utf-8 -*-

from threadfixproapi.threadfixpro import ThreadFixProAPI
from webbreaker.threadfix.common.loghelper import ThreadFixLogHelper

threadfixloghelper = ThreadFixLogHelper()


class ThreadFixClient(object):
    def __init__(self, host, api_key):
        self.host = host
        self.api_key = api_key
      
    # TODO verify this works. Unable to test due to ThreadFix configurations
    def download_scan(self, scan_id):
        api = ThreadFixProAPI(host=self.host, api_key=self.api_key, verify_ssl=False)
        details_response = api.get_scan_details(scan_id)
        if details_response.success:
            if len(details_response.data['originalFileNames']):
                filename = details_response.data['originalFileNames'][-1]
                response = api.download_scan(scan_id, filename)
                if response.success:
                    with open(filename, 'wb') as scan_file:
                        scan_file.write(response.data)
                        return filename
                else:
                    threadfixloghelper.log_error_request_download(response.message)
                    return None
            else:
                return -1
        else:
            return False
