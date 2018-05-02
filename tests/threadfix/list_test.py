import mock

from webbreaker.threadfix.list import ThreadFixList

@mock.patch('webbreaker.threadfix.list.ThreadFixHelper')
@mock.patch('webbreaker.threadfix.list.threadfixloghelper')
def test_threadfix_list_successful_list(log_mock, helper_mock):
    team = 'Team Name'
    application = 'Test App'
    expected_list_apps = [{'team_id': '10',
                          'team_name': team,
                          'app_id': '100',
                          'app_name': application}]
    helper_mock.return_value.list_all_apps.return_value = expected_list_apps
    ThreadFixList(team=team, application=application)

    assert helper_mock.call_count == 1
    assert log_mock.log_info_threadfix_list_success.call_count == 1
    assert log_mock.log_ingo_no_application_found.call_count == 0
    assert log_mock.log_error_api_token_associated_with_local_account.call_count == 0

@mock.patch('webbreaker.threadfix.list.ThreadFixHelper')
@mock.patch('webbreaker.threadfix.list.threadfixloghelper')
def test_threadfix_list_bad_query(log_mock, helper_mock):
    expected_list_apps = []
    helper_mock.return_value.list_all_apps.return_value = expected_list_apps
    team = 'fake team'
    application = 'fake app'
    ThreadFixList(team, application)

    assert helper_mock.call_count == 1
    assert log_mock.log_info_threadfix_list_success.call_count == 0
    assert log_mock.log_info_no_application_found.call_count == 1
    assert log_mock.log_error_api_token_associated_with_local_account.call_count == 0