from webbreaker.threadfix.common.helper import ThreadFixHelper
from webbreaker.common.logexceptionhelper import LogExceptionHelper
from webbreaker.common.logexceptionhelper import LogInfoHelper

loginfohelper = LogInfoHelper()
logexceptionhelper = LogExceptionHelper()


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
                print('\n\n')
                loginfohelper.LogInfoThreadfixListSuccess()
            else:
                query_info = ''
                if team is not None:
                    query_info = ' with team name matching {}'.format(team)
                if application is not None:
                    if query_info == '':
                        query_info = ' with application name matching {}'.format(application)
                    else:
                        query_info = query_info + ' and application name matching {}'.format(application)
                loginfohelper.LogInfoNoApplicationFound(query_info)
        else:
            logexceptionhelper.LogErrorAPITokenAssociatedWithLocalAccount()
