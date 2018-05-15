from webbreaker.threadfix.common.helper import ThreadFixHelper
from webbreaker.common.api_response_helper import APIHelper
from webbreaker.common.logexceptionhelper import LogExceptionHelper
from webbreaker.common.logexceptionhelper import LogInfoHelper

logexceptionhelper = LogExceptionHelper()
loginfohelper = LogInfoHelper()

class ThreadFixScans(object):
    def __init__(self, app_id):
        self.helper = ThreadFixHelper()
        self._list_scans(app_id)

    def _list_scans(self, app_id):
        scans = self._list_scans_by_app(app_id)
        if scans:
            print("{0:^10} {1:30} {2:30}".format('ID', 'Scanner Name', 'Filename'))
            print("{0:10} {1:30} {2:30}".format('-' * 10, '-' * 30, '-' * 30))
            for scan in scans:
                print("{0:^10} {1:30} {2:30}".format(scan['id'], scan['scannerName'], scan['filename']))
            loginfohelper.LogInfoThreadfixScansListedSuccess()
            print('\n\n')
        else:
            logexceptionhelper.LogErrorNoScansFoundWithAppId(app_id)

    def _list_scans_by_app(self, app_id):
        api = self.helper.api
        response = api.list_scans(app_id)
        APIHelper().check_for_response_errors(response)
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
