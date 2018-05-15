from webbreaker.threadfix.common.helper import ThreadFixHelper
from webbreaker.common.logexceptionhelper import LogExceptionHelper
from webbreaker.common.logexceptionhelper import LogInfoHelper

loginfohelper = LogInfoHelper()
logexceptionhelper = LogExceptionHelper()

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
            loginfohelper.LogInfoThreadfixTeamsListedSuccess()
            print('\n\n')
        else:
            logexceptionhelper.LogErrorNoTeam()
