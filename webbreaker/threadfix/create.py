from webbreaker.threadfix.common.helper import ThreadFixHelper
from webbreaker.common.api_response_helper import APIHelper
from webbreaker.threadfix.common.loghelper import ThreadFixLogHelper

threadfixloghelper = ThreadFixLogHelper()

class ThreadFixCreate(object):
    def __init__(self, team_id, team, application, url):
        self.helper = ThreadFixHelper()
        self._create_application_wrapper(team_id, team, application, url)

    def _create_application_wrapper(self, team_id, team, application, url):
        if not team_id and not team:
            threadfixloghelper.log_error_specify_team()
            return
        if team and not team_id:
            team_id = self._get_team_id_by_name(team)
        if team_id is None:
            threadfixloghelper.log_error_no_team_with_application(team)
            return
        created_app = self._create_application(team_id, application, url)
        threadfixloghelper.log_info_application_created_with_id((created_app['id']))

    def _create_application(self, team_id, name, url):
        response = self.helper.api.create_application(team_id, name, url)
        APIHelper().check_for_response_errors(response)
        return response.data

    def _get_team_id_by_name(self, team_name):
            teams = self.helper.get_team_list()
            for team in teams:
                if team['name'] == team_name:
                    return team['id']
            return None
