import mock
import pytest

from webbreaker.threadfix.create import ThreadFixCreate
from threadfixproapi.threadfixpro import ThreadFixProResponse

@mock.patch('webbreaker.threadfix.create.ThreadFixHelper')
@mock.patch('webbreaker.threadfix.create.loginfohelper')
def test_threadfix_create_app_successful_no_team_id(loginfo_mock, helper_mock):
    team_id = '10'
    team = 'some team'
    test_team = {
        'id': team_id,
        'name': team
    }
    app_name = 'new app'
    url = 'someurl.com'
    new_app = {
        'id': '100',
        'application': app_name,
        'team_id': team_id,
        'url': url
    }
    helper_mock.return_value.get_team_list.return_value = [test_team]
    helper_mock.return_value.api.create_application.return_value = ThreadFixProResponse(message='test', success=True, data=new_app)

    tfc = ThreadFixCreate(None, team, app_name, url)
    assert helper_mock.call_count == 1
    assert tfc.helper.get_team_list.call_count == 1
    loginfo_mock.LogInfoApplicationCreatedWithId.assert_called_once_with(new_app['id'])

@mock.patch('webbreaker.threadfix.create.ThreadFixHelper')
@mock.patch('webbreaker.threadfix.create.loginfohelper')
@mock.patch('webbreaker.threadfix.create.logexceptionhelper')
def test_threadfix_create_app_failed_no_team_id_team_not_exist(logex_mock, loginfo_mock, helper_mock):
    team_id = '10'
    team = 'some team'
    test_team = {
        'id': team_id,
        'name': team
    }
    app_name = 'new app'
    url = 'someurl.com'

    helper_mock.return_value.get_team_list.return_value = [test_team]
    fakeTeam = 'team that does not exist'

    tfc = ThreadFixCreate(None, fakeTeam, app_name, url)
    assert helper_mock.call_count == 1
    assert tfc.helper.get_team_list.call_count == 1
    logex_mock.LogErrorNoTeamWithApplication.assert_called_once_with(fakeTeam)
    assert loginfo_mock.LogInfoApplicationCreatedWithId.call_count == 0

@mock.patch('webbreaker.threadfix.create.ThreadFixHelper')
@mock.patch('webbreaker.threadfix.create.loginfohelper')
def test_threadfix_create_app_failed_no_team_id(loginfo_mock, helper_mock):
    team_id = '10'
    team = 'some team'
    test_team = {
        'id': team_id,
        'name': team
    }
    app_name = 'new app'
    url = 'someurl.com'
    new_app = {}

    helper_mock.return_value.get_team_list.return_value = [test_team]
    helper_mock.return_value.api.create_application.return_value = ThreadFixProResponse(message='error', success=False, data=new_app)

    with pytest.raises(SystemExit):
        ThreadFixCreate(None, team, app_name, url)
    assert helper_mock.call_count == 1
    assert loginfo_mock.LogInfoApplicationCreatedWithId.call_count == 0

@mock.patch('webbreaker.threadfix.create.ThreadFixHelper')
@mock.patch('webbreaker.threadfix.create.loginfohelper')
def test_threadfix_create_app_successful_no_team(loginfo_mock, helper_mock):
    team_id = '10'
    app_name = 'new app'
    url = 'someurl.com'
    new_app = {
        'id': '100',
        'application': app_name,
        'team_id': team_id,
        'url': url
    }
    helper_mock.return_value.api.create_application.return_value = ThreadFixProResponse(message='test', success=True, data=new_app)

    tfc = ThreadFixCreate(team_id, None, app_name, url)
    assert helper_mock.call_count == 1
    assert tfc.helper.get_team_list.call_count == 0
    loginfo_mock.LogInfoApplicationCreatedWithId.assert_called_once_with(new_app['id'])

@mock.patch('webbreaker.threadfix.create.ThreadFixHelper')
@mock.patch('webbreaker.threadfix.create.loginfohelper')
def test_threadfix_create_app_failed_no_team(loginfo_mock, helper_mock):
    team_id = '10'
    app_name = 'new app'
    url = 'someurl.com'
    new_app = {}
    helper_mock.return_value.api.create_application.return_value = ThreadFixProResponse(message='error', success=False, data=new_app)

    with pytest.raises(SystemExit):
        ThreadFixCreate(team_id, None, app_name, url)
    assert helper_mock.call_count == 1
    assert loginfo_mock.LogInfoApplicationCreatedWithId.call_count == 0

@mock.patch('webbreaker.threadfix.create.ThreadFixHelper')
@mock.patch('webbreaker.threadfix.create.loginfohelper')
def test_threadfix_create_app_successful_all_params(loginfo_mock, helper_mock):
    team_id = '10'
    team = 'some team'
    app_name = 'new app'
    url = 'someurl.com'
    new_app = {
        'id': '100',
        'application': app_name,
        'team_id': team_id,
        'url': url
    }
    helper_mock.return_value.api.create_application.return_value = ThreadFixProResponse(message='test', success=True, data=new_app)

    tfc = ThreadFixCreate(team_id, team, app_name, url)
    assert helper_mock.call_count == 1
    assert tfc.helper.get_team_list.call_count == 0
    loginfo_mock.LogInfoApplicationCreatedWithId.assert_called_once_with(new_app['id'])

@mock.patch('webbreaker.threadfix.create.ThreadFixHelper')
@mock.patch('webbreaker.threadfix.create.loginfohelper')
def test_threadfix_create_app_failed_all_params(loginfo_mock, helper_mock):
    team_id = '10'
    team = 'some team'
    app_name = 'new app'
    url = 'someurl.com'
    new_app = {}

    helper_mock.return_value.api.create_application.return_value = ThreadFixProResponse(message='error', success=False, data=new_app)

    with pytest.raises(SystemExit):
        ThreadFixCreate(team_id, team, app_name, url)
    assert helper_mock.call_count == 1
    assert loginfo_mock.LogInfoApplicationCreatedWithId.call_count == 0

@mock.patch('webbreaker.threadfix.create.ThreadFixHelper')
@mock.patch('webbreaker.threadfix.create.loginfohelper')
@mock.patch('webbreaker.threadfix.create.logexceptionhelper')
def test_threadfix_create_app_failed_no_team_nor_team_id(logex_mock, loginfo_mock, helper_mock):
    app_name = 'new app'
    url = 'someurl.com'

    tfc = ThreadFixCreate(None, None, app_name, url)
    assert helper_mock.call_count == 1
    assert tfc.helper.get_team_list.call_count == 0
    assert logex_mock.LogErrorSpecifyTeam.call_count == 1
    assert loginfo_mock.LogInfoApplicationCreatedWithId.call_count == 0
