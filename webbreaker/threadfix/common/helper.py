from webbreaker.threadfix.threadfixconfig import ThreadFixConfig
from threadfixproapi.threadfixpro import ThreadFixProAPI
from webbreaker.common.logexceptionhelper import LogExceptionHelper
from webbreaker.common.logexceptionhelper import LogInfoHelper
from webbreaker.common.api_response_helper import APIHelper

logexceptionhelper = LogExceptionHelper()
loginfohelper = LogInfoHelper()


class ThreadFixHelper(object):
    def __init__(self):
        self.config = ThreadFixConfig()
        self.api = ThreadFixProAPI(host=self.config.host, api_key=self.config.api_key, verify_ssl=self.config.verify_ssl)

    def get_team_list(self):
        response = self.api.list_teams()
        APIHelper().check_for_response_errors(response)
        return response.data

    def list_apps_by_team(self, team_id):
        response = self.api.get_applications_by_team(team_id)
        APIHelper().check_for_response_errors(response)
        return response.data

    def list_all_apps(self, team_name=None, app_name=None):
            teams_resp = self.get_team_list()
            if teams_resp:
                team_ids = []
                applications = []
                for team in teams_resp:
                    if team_name is not None and team_name.lower() in team['name'].lower():
                        team_ids.append({'id': team['id'], 'name': team['name']})
                    elif team_name is None:
                        team_ids.append({'id': team['id'], 'name': team['name']})
                if not len(team_ids):
                    logexceptionhelper.LogErrorNoTeamWithName(team_name)
                for team in team_ids:
                    app_response = self.list_apps_by_team(team['id'])
                    if app_response:
                        for app in app_response:
                            if app_name is not None and app_name.lower() in app['name'].lower():
                                applications.append({'team_id': team['id'],
                                                     'team_name': team['name'],
                                                     'app_id': app['id'],
                                                     'app_name': app['name']})
                            elif app_name is None:
                                applications.append({'team_id': team['id'],
                                                     'team_name': team['name'],
                                                     'app_id': app['id'],
                                                     'app_name': app['name']})

                    else:

                        logexceptionhelper.LogErrorRetrievingApplication(team['name'])
                return applications

            else:
                return False
