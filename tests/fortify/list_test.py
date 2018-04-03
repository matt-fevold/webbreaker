import mock
import pytest

from webbreaker.fortify.list import FortifyList


def attribute_error_exception(**kwargs):
    raise AttributeError('Test Failure')


def unbound_local_error_exception(**kwargs):
    raise UnboundLocalError('Test Failure')


def type_error_exception(**kwargs):
    raise TypeError('Test Failure')


@mock.patch('webbreaker.fortify.list.FortifyList.list')
@mock.patch('webbreaker.fortify.list.FortifyAuth')
@mock.patch('webbreaker.fortify.list.FortifyConfig')
def test_fortify_list_successful_init_valid_application_name(config_mock, auth_mock, list_mock):
    expected_username = 'user'
    expected_password = 'password'
    expected_application = 'Test Application'

    auth_mock.return_value.authenticate.return_value = expected_username, expected_password
    fortify_list = FortifyList(username=None,
                               password=None,
                               application_name=expected_application)

    assert fortify_list.username == expected_username
    assert fortify_list.password == expected_password

    list_mock.assert_called_once_with(expected_application)
    assert config_mock.call_count == 1
    assert auth_mock.call_count == 1


@mock.patch('webbreaker.fortify.list.FortifyList.list')
@mock.patch('webbreaker.fortify.list.FortifyAuth')
@mock.patch('webbreaker.fortify.list.FortifyConfig')
def test_fortify_list_successful_init_no_application_name(config_mock, auth_mock, list_mock):
    expected_username = 'user'
    expected_password = 'password'

    auth_mock.return_value.authenticate.return_value = expected_username, expected_password

    fortify_list = FortifyList(username=None,
                               password=None,
                               application_name=None)

    assert fortify_list.username == expected_username
    assert fortify_list.password == expected_password

    list_mock.assert_called_once_with(None)
    assert config_mock.call_count == 1
    assert auth_mock.call_count == 1


@mock.patch('webbreaker.fortify.list.FortifyClient')
@mock.patch('webbreaker.fortify.list.FortifyAuth')
@mock.patch('webbreaker.fortify.list.FortifyConfig')
def test_fortify_list_list_successful_list(config_mock, auth_mock, client_mock):
    expected_username = 'user'
    expected_password = 'password'
    expected_application = 'Test Application'

    auth_mock.return_value.authenticate.return_value = expected_username, expected_password
    fortify_list = FortifyList(username=expected_username,
                               password=expected_password,
                               application_name=expected_application)

    assert fortify_list.username == expected_username
    assert fortify_list.password == expected_password

    config_mock.assert_called_once()

    assert config_mock.call_count == 1
    assert auth_mock.call_count == 1
    assert client_mock.call_count == 1


@mock.patch('webbreaker.fortify.list.FortifyClient')
@mock.patch('webbreaker.fortify.list.FortifyAuth')
@mock.patch('webbreaker.fortify.list.FortifyConfig')
@mock.patch('webbreaker.fortify.list.Logger.app.critical')
def test_fortify_list_list_throws_attribute_error(log_mock, config_mock, auth_mock, client_mock):
    expected_username = 'user'
    expected_password = 'password'
    expected_application = 'Test Application'

    auth_mock.return_value.authenticate.return_value = expected_username, expected_password
    client_mock.side_effect = attribute_error_exception
    with pytest.raises(SystemExit):
        FortifyList(username=expected_username,
                    password=expected_password,
                    application_name=expected_application)
    log_mock.assert_called_once()


@mock.patch('webbreaker.fortify.list.FortifyClient')
@mock.patch('webbreaker.fortify.list.FortifyAuth')
@mock.patch('webbreaker.fortify.list.FortifyConfig')
@mock.patch('webbreaker.fortify.list.Logger.app.critical')
def test_fortify_list_list_throws_unbound_local_error(log_mock, config_mock, auth_mock, client_mock):
    expected_username = 'user'
    expected_password = 'password'
    expected_application = 'Test Application'

    auth_mock.return_value.authenticate.return_value = expected_username, expected_password
    client_mock.side_effect = unbound_local_error_exception
    with pytest.raises(SystemExit):
        FortifyList(username=expected_username,
                    password=expected_password,
                    application_name=expected_application)
    log_mock.assert_called_once()


@mock.patch('webbreaker.fortify.list.FortifyClient')
@mock.patch('webbreaker.fortify.list.FortifyAuth')
@mock.patch('webbreaker.fortify.list.FortifyConfig')
@mock.patch('webbreaker.fortify.list.Logger.app.critical')
def test_fortify_list_list_throws_type_error(log_mock, config_mock, auth_mock, client_mock):
    expected_username = 'user'
    expected_password = 'password'
    expected_application = 'Test Application'

    auth_mock.return_value.authenticate.return_value = expected_username, expected_password
    client_mock.side_effect = type_error_exception
    with pytest.raises(SystemExit):
        FortifyList(username=expected_username,
                    password=expected_password,
                    application_name=expected_application)
    log_mock.assert_called_once()
