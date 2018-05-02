import mock

from webbreaker.threadfix.teams import ThreadFixTeams

@mock.patch('webbreaker.threadfix.teams.ThreadFixHelper')
@mock.patch('webbreaker.threadfix.teams.threadfixloghelper')
def test_threadfix_teams_successful_list(log_mock, helper_mock):
    expected_list_teams = [{'id': '123', 'name': 'team name'}]
    helper_mock.return_value.get_team_list.return_value = expected_list_teams
    ThreadFixTeams()
    assert helper_mock.call_count == 1
    assert log_mock.log_info_threadfix_teams_listed_success.call_count == 1
    assert log_mock.log_error_no_team.call_count == 0

@mock.patch('webbreaker.threadfix.teams.ThreadFixHelper')
@mock.patch('webbreaker.threadfix.teams.threadfixloghelper')
def test_threadfix_teams_no_teams(log_mock, helper_mock):
    helper_mock.return_value.get_team_list.return_value = []
    ThreadFixTeams()
    assert helper_mock.call_count == 1
    assert log_mock.log_info_threadfix_teams_listed_success.call_count == 0
    assert log_mock.log_error_no_team.call_count == 1