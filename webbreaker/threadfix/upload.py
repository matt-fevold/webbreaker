from webbreaker.threadfix.common.helper import ThreadFixHelper
from webbreaker.common.api_response_helper import APIHelper
from webbreaker.threadfix.common.loghelper import ThreadFixLogHelper

threadfixloghelper = ThreadFixLogHelper()


class ThreadFixUpload(object):
    def __init__(self, app_id, application, scan_file):
        self.helper = ThreadFixHelper()
        if not app_id and not application:
            threadfixloghelper.log_error_specify_application(app_id)
            return
        self._upload_scan_wrapper(app_id, application, scan_file)

    def _upload_scan(self, app_id, file_name):
        response = self.helper.api.upload_scan(app_id, file_name)
        APIHelper().check_for_response_errors(response)
        return response.data

    def _upload_scan_wrapper(self, app_id, application, scan_file):
        if not app_id:
            threadfixloghelper.log_info_find_application_with_matching_name(application)
            apps = self.helper.list_all_apps()
            if not apps:
                threadfixloghelper.log_error_threadfix_retrieve_fail()
                return
            else:
                matches = []
                for app in apps:
                    if app['app_name'] == application:
                        matches.append(app.copy())
                if len(matches) == 0:
                    threadfixloghelper.log_info_find_application_with_matching_name(application)
                    return
                if len(matches) > 1:
                    threadfixloghelper.log_error_multiple_application_found(application)
                    print("{0:^10} {1:55} {2:30}".format('App ID', 'Team', 'Application'))
                    print("{0:10} {1:55} {2:30}".format('-' * 10, '-' * 55, '-' * 30))
                    for app in matches:
                        print("{0:^10} {1:55} {2:30}".format(app['app_id'], app['team_name'], app['app_name']))
                    print('\n\n')
                    return
                else:
                    app_id = matches[0]['app_id']

        upload_resp = self._upload_scan(app_id, scan_file)
        threadfixloghelper.log_info_upload_response(upload_resp)