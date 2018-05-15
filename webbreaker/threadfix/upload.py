from webbreaker.threadfix.common.helper import ThreadFixHelper
from webbreaker.common.api_response_helper import APIHelper
from webbreaker.common.logexceptionhelper import LogExceptionHelper
from webbreaker.common.logexceptionhelper import LogInfoHelper

logexceptionhelper = LogExceptionHelper()
loginfohelper = LogInfoHelper()

class ThreadFixUpload(object):
    def __init__(self, app_id, application, scan_file):
        self.helper = ThreadFixHelper()
        if not app_id and not application:
            logexceptionhelper.LogErrorSpecifyApplication(app_id)
            return
        self._upload_scan_wrapper(app_id, application, scan_file)

    def _upload_scan(self, app_id, file_name):
        response = self.helper.api.upload_scan(app_id, file_name)
        APIHelper().check_for_response_errors(response)
        return response.data

    def _upload_scan_wrapper(self, app_id, application, scan_file):
        if not app_id:
            loginfohelper.LogInfoFindApplicationWithMatchingName(application)
            apps = self.helper.list_all_apps()
            if not apps:
                logexceptionhelper.LogErrorThreadfixRetrieveFail()
                return
            else:
                matches = []
                for app in apps:
                    if app['app_name'] == application:
                        matches.append(app.copy())
                if len(matches) == 0:
                    logexceptionhelper.LogErrorNoApplicationWithMatchingName(application)
                    return
                if len(matches) > 1:
                    logexceptionhelper.LogErrorMultipleApplicationFound(application)
                    print("{0:^10} {1:55} {2:30}".format('App ID', 'Team', 'Application'))
                    print("{0:10} {1:55} {2:30}".format('-' * 10, '-' * 55, '-' * 30))
                    for app in matches:
                        print("{0:^10} {1:55} {2:30}".format(app['app_id'], app['team_name'], app['app_name']))
                    print('\n\n')
                    return
                else:
                    app_id = matches[0]['app_id']

        upload_resp = self._upload_scan(app_id, scan_file)
        loginfohelper.LogInfoUploadResp(upload_resp)