#!/usr/bin/env python
# -*- coding: utf-8 -*-

from webbreaker.webbreakerlogger import Logger
from webbreaker.threadfixapi.threadfix import ThreadFixAPI


class ThreadFixClient(object):
    def __init__(self, host, api_key):
        self.host = host
        self.api_key = api_key

    def upload_scan(self, app_id, file_name):
        api = ThreadFixAPI(host=self.host, api_key=self.api_key, verify_ssl=False)
        response = api.upload_scan(app_id, file_name)
        if response.success:
            return response.data
        else:
            Logger.app.error(response.message)
            return False

    def list_teams(self):
        api = ThreadFixAPI(host=self.host, api_key=self.api_key, verify_ssl=False)
        response = api.list_teams()
        if response.success:
            return response.data
        else:
            Logger.app.error(response.message)
            return False

    def list_apps_by_team(self, team_id):
        api = ThreadFixAPI(host=self.host, api_key=self.api_key, verify_ssl=False)
        response = api.get_applications_by_team(team_id)
        if response.success:
            return response.data
        else:
            Logger.app.error(response.message)
            return False

    def list_scans_by_app(self, app_id):
        api = ThreadFixAPI(host=self.host, api_key=self.api_key, verify_ssl=False)
        response = api.list_scans(app_id)
        if response.success:
            master_data = response.data
            for scan in master_data:
                response = api.get_scan_details(scan['id'])
                if response.success:
                    if len(response.data['originalFileNames']):
                        scan['filename'] = response.data['originalFileNames'][-1]
                    else:
                        scan['filename'] = 'None'
                else:
                    scan['filename'] = 'Error'
            return master_data
        else:
            Logger.app.error(response.message)
            return False

    def create_application(self, team_id, name, url):
        api = ThreadFixAPI(host=self.host, api_key=self.api_key, verify_ssl=False)
        response = api.create_application(team_id, name, url)
        if response.success:
            return response.data
        else:
            Logger.app.error(response.message)
            return False

    # TODO verify this works. Unable to test due to ThreadFix configurations
    def download_scan(self, scan_id):
        api = ThreadFixAPI(host=self.host, api_key=self.api_key, verify_ssl=False)
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
                    Logger.app.error("Error requesting download: {}".format(response.message))
                    return None
            else:
                return -1
        else:
            return False
