import mock
import pytest

from webbreaker.fortify.download import FortifyDownload


def attribute_error_exception(**kwargs):
    raise AttributeError('Test Failure')


def unbound_local_error_exception(**kwargs):
    raise UnboundLocalError('Test Failure')


def io_error_exception(**kwargs):
    raise IOError('Test Failure')


@mock.patch('webbreaker.fortify.download.FortifyDownload.download')
@mock.patch('webbreaker.fortify.download.FortifyAuth')
@mock.patch('webbreaker.fortify.download.FortifyConfig')
def test_fortify_download_successful_init_application_name_is_not_none(config_mock, auth_mock, download_mock):
    expected_username = 'user'
    expected_password = 'password'
    expected_application = 'Test Application'
    expected_version = 'Test Version'

    auth_mock.return_value.authenticate.return_value = expected_username, expected_password
    fortify_download = FortifyDownload(username=None,
                                       password=None,
                                       application_name=expected_application,
                                       version_name=expected_version)

    assert fortify_download.username == expected_username
    assert fortify_download.password == expected_password

    download_mock.assert_called_once_with(expected_application, expected_version)
    assert config_mock.call_count == 1
    assert auth_mock.call_count == 1
    assert download_mock.call_count == 1


@mock.patch('webbreaker.fortify.download.FortifyDownload.download')
@mock.patch('webbreaker.fortify.download.FortifyAuth')
@mock.patch('webbreaker.fortify.download.FortifyConfig')
def test_fortify_download_successful_init_application_name_is_none(config_mock, auth_mock, download_mock):
    expected_username = 'user'
    expected_password = 'password'
    expected_application = 'Test Application'
    expected_version = 'Test Version'

    auth_mock.return_value.authenticate.return_value = expected_username, expected_password
    config_mock.return_value.application_name = expected_application
    config_mock.application_name()

    fortify_download = FortifyDownload(username=None,
                                       password=None,
                                       application_name=None,
                                       version_name=expected_version)

    assert fortify_download.username == expected_username
    assert fortify_download.password == expected_password

    download_mock.assert_called_once_with(expected_application, expected_version)
    assert config_mock.call_count == 1
    assert auth_mock.call_count == 1
    assert download_mock.call_count == 1


@mock.patch('webbreaker.fortify.download.FortifyClient')
@mock.patch('webbreaker.fortify.download.FortifyAuth')
@mock.patch('webbreaker.fortify.download.FortifyConfig')
def test_fortify_download_download_successful_download(config_mock, auth_mock, client_mock):
    expected_username = 'user'
    expected_password = 'password'
    expected_application = 'Test Application'
    expected_version = 'Test Version'

    auth_mock.return_value.authenticate.return_value = expected_username, expected_password

    fortify_download = FortifyDownload(username=expected_username,
                                       password=expected_password,
                                       application_name=expected_application,
                                       version_name=expected_version)

    assert fortify_download.username == expected_username
    assert fortify_download.password == expected_password

    client_mock.assert_called_once()
    assert config_mock.call_count == 1
    assert auth_mock.call_count == 1
    assert client_mock.call_count == 1


@mock.patch('webbreaker.fortify.download.FortifyClient')
@mock.patch('webbreaker.fortify.download.FortifyAuth')
@mock.patch('webbreaker.fortify.download.FortifyConfig')
@mock.patch('webbreaker.fortify.download.Logger.app.critical')
def test_fortify_download_download_throws_attribute_error(log_mock, config_mock, auth_mock, client_mock):
    expected_username = 'user'
    expected_password = 'password'
    expected_application = 'Test Application'
    expected_version = 'Test Version'

    auth_mock.return_value.authenticate.return_value = expected_username, expected_password
    client_mock.side_effect = attribute_error_exception

    with pytest.raises(SystemExit):
        FortifyDownload(username=expected_username,
                        password=expected_password,
                        application_name=expected_application,
                        version_name=expected_version)

    log_mock.assert_called_once()


@mock.patch('webbreaker.fortify.download.FortifyClient')
@mock.patch('webbreaker.fortify.download.FortifyAuth')
@mock.patch('webbreaker.fortify.download.FortifyConfig')
@mock.patch('webbreaker.fortify.download.Logger.app.critical')
def test_fortify_download_download_throws_unbound_local_error(log_mock, config_mock, auth_mock, client_mock):
    expected_username = 'user'
    expected_password = 'password'
    expected_application = 'Test Application'
    expected_version = 'Test Version'

    auth_mock.return_value.authenticate.return_value = expected_username, expected_password
    client_mock.side_effect = unbound_local_error_exception

    with pytest.raises(SystemExit):
        FortifyDownload(username=expected_username,
                        password=expected_password,
                        application_name=expected_application,
                        version_name=expected_version)

    log_mock.assert_called_once()


@mock.patch('webbreaker.fortify.download.FortifyClient')
@mock.patch('webbreaker.fortify.download.FortifyAuth')
@mock.patch('webbreaker.fortify.download.FortifyConfig')
@mock.patch('webbreaker.fortify.download.Logger.app.error')
def test_fortify_download_download_throws_io_error(log_mock, config_mock, auth_mock, client_mock):
    expected_username = 'user'
    expected_password = 'password'
    expected_application = 'Test Application'
    expected_version = 'Test Version'

    auth_mock.return_value.authenticate.return_value = expected_username, expected_password
    client_mock.side_effect = io_error_exception

    with pytest.raises(SystemExit):
        FortifyDownload(username=expected_username,
                        password=expected_password,
                        application_name=expected_application,
                        version_name=expected_version)

    log_mock.assert_called_once()
