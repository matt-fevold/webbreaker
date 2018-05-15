import mock

from webbreaker.threadfix.teams import ThreadFixTeams

@mock.patch('webbreaker.threadfix.teams.ThreadFixHelper')
@mock.patch('webbreaker.threadfix.teams.loginfohelper')
@mock.patch('webbreaker.threadfix.teams.logexceptionhelper')
def test_threadfix_teams_successful_list(logex_mock, loginfo_mock, helper_mock):
    expected_list_teams = [{'id': '123', 'name': 'team name'}]
    helper_mock.return_value.get_team_list.return_value = expected_list_teams
    ThreadFixTeams()
    assert helper_mock.call_count == 1
    assert loginfo_mock.LogInfoThreadfixTeamsListedSuccess.call_count == 1
    assert logex_mock.LogErrorNoTeam.call_count == 0

@mock.patch('webbreaker.threadfix.teams.ThreadFixHelper')
@mock.patch('webbreaker.threadfix.teams.loginfohelper')
@mock.patch('webbreaker.threadfix.teams.logexceptionhelper')
def test_threadfix_teams_no_teams(logex_mock, loginfo_mock, helper_mock):
    helper_mock.return_value.get_team_list.return_value = []
    ThreadFixTeams()
    assert helper_mock.call_count == 1
    assert loginfo_mock.LogInfoThreadfixTeamsListedSuccess.call_count == 0
    assert logex_mock.LogErrorNoTeam.call_count == 1