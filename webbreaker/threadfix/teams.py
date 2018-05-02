from webbreaker.threadfix.common.helper import ThreadFixHelper
from webbreaker.threadfix.common.loghelper import ThreadFixLogHelper

threadfixloghelper = ThreadFixLogHelper()


class ThreadFixTeams(object):
    def __init__(self):
        self.helper = ThreadFixHelper()
        self._list_teams()

    def _list_teams(self):
        teams = self.helper.get_team_list()
        if teams:
            print("{0:^10} {1:30}".format('ID', 'Name'))
            print("{0:10} {1:30}".format('-' * 10, '-' * 30))
            for team in teams:
                print("{0:^10} {1:30}".format(team['id'], team['name']))
            threadfixloghelper.log_info_threadfix_teams_listed_success()
            print('\n\n')
        else:
            threadfixloghelper.log_error_no_team()
