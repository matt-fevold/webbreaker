from webbreaker.threadfix.common.helper import ThreadFixHelper
from webbreaker.threadfix.common.loghelper import ThreadFixLogHelper

threadfixloghelper = ThreadFixLogHelper()


class ThreadFixList(object):
    def __init__(self, team, application):
        self.helper = ThreadFixHelper()
        self._list_applications(team, application)

    def _list_applications(self, team, application):
        applications = self.helper.list_all_apps(team, application)
        if applications is not False:
            if len(applications):
                print("{0:^10} {1:55} {2:30}".format('App ID', 'Team', 'Application'))
                print("{0:10} {1:55} {2:30}".format('-' * 10, '-' * 55, '-' * 30))
                for app in applications:
                    print("{0:^10} {1:55} {2:30}".format(app['app_id'], app['team_name'], app['app_name']))
                threadfixloghelper.log_info_threadfix_list_success()
            else:
                query_info = ''
                if team is not None:
                    query_info = ' with team name matching {}'.format(team)
                if application is not None:
                    if query_info == '':
                        query_info = ' with application name matching {}'.format(application)
                    else:
                        query_info = query_info + ' and application name matching {}'.format(application)
                threadfixloghelper.log_info_no_application_found(query_info)
        else:
            threadfixloghelper.log_error_api_token_associated_with_local_account()
