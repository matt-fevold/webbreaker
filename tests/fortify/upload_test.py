import mock
import pytest

from webbreaker.fortify.upload import FortifyUpload


def unbound_local_error_exception(**kwargs):
    raise UnboundLocalError('Test Failure')


def value_error_exception(**kwargs):
    raise ValueError('Test Failure')


def io_error_exception(**kwargs):
    raise IOError('Test Failure')


@mock.patch('webbreaker.fortify.upload.FortifyUpload.upload')
@mock.patch('webbreaker.fortify.upload.FortifyAuth')
@mock.patch('webbreaker.fortify.upload.FortifyConfig')
def test_fortify_upload_successful_init_application_name_scan_name_not_none(config_mock, auth_mock, upload_mock):
    expected_username = 'user'
    expected_password = 'password'
    expected_application = 'Test Application'
    expected_version = 'Test Version'
    expected_scan_name = 'Test Scan Name'
    expected_project_template = 'Test Template'

    auth_mock.return_value.authenticate.return_value = expected_username, expected_password
    config_mock.return_value.project_template = expected_project_template
    config_mock.project_template()

    fortify_upload = FortifyUpload(username=None,
                                   password=None,
                                   application_name=expected_application,
                                   version_name=expected_version,
                                   scan_name=expected_scan_name,
                                   custom_value=None)

    assert fortify_upload.username == expected_username
    assert fortify_upload.password == expected_password

    upload_mock.assert_called_once_with(expected_application, expected_version, expected_project_template,
                                        expected_scan_name, None)
    assert config_mock.call_count == 1
    assert auth_mock.call_count == 1
    assert upload_mock.call_count == 1


@mock.patch('webbreaker.fortify.upload.FortifyUpload.upload')
@mock.patch('webbreaker.fortify.upload.FortifyAuth')
@mock.patch('webbreaker.fortify.upload.FortifyConfig')
def test_fortify_upload_successful_init_scan_name_is_none(config_mock, auth_mock, upload_mock):
    expected_username = 'user'
    expected_password = 'password'
    expected_application = 'Test Application'
    expected_version = 'Test Version'
    expected_project_template = 'Test Template'

    auth_mock.return_value.authenticate.return_value = expected_username, expected_password
    config_mock.return_value.project_template = expected_project_template

    fortify_upload = FortifyUpload(username=None,
                                   password=None,
                                   application_name=expected_application,
                                   version_name=expected_version,
                                   scan_name=None,
                                   custom_value=None)

    assert fortify_upload.username == expected_username
    assert fortify_upload.password == expected_password

    # If scan_name is None, scan_name will equal version_name
    upload_mock.assert_called_once_with(expected_application, expected_version, expected_project_template,
                                        expected_version, None)
    assert config_mock.call_count == 1
    assert auth_mock.call_count == 1
    assert upload_mock.call_count == 1


@mock.patch('webbreaker.fortify.upload.FortifyUpload.upload')
@mock.patch('webbreaker.fortify.upload.FortifyAuth')
@mock.patch('webbreaker.fortify.upload.FortifyConfig')
def test_fortify_upload_successful_init_application_name_is_none(config_mock, auth_mock, upload_mock):
    expected_username = 'user'
    expected_password = 'password'
    expected_application = 'Test Application'
    expected_version = 'Test Version'
    expected_scan_name = 'Test Scan Name'
    expected_project_template = 'Test Template'

    auth_mock.return_value.authenticate.return_value = expected_username, expected_password
    config_mock.return_value.project_template = expected_project_template
    config_mock.return_value.application_name = expected_application

    fortify_upload = FortifyUpload(username=None,
                                   password=None,
                                   application_name=None,
                                   version_name=expected_version,
                                   scan_name=expected_scan_name,
                                   custom_value=None)

    assert fortify_upload.username == expected_username
    assert fortify_upload.password == expected_password

    # If scan_name is None, scan_name will equal version_name
    upload_mock.assert_called_once_with(expected_application, expected_version, expected_project_template,
                                        expected_scan_name, None)
    assert config_mock.call_count == 1
    assert auth_mock.call_count == 1
    assert upload_mock.call_count == 1


@mock.patch('webbreaker.fortify.upload.FortifyHelper')
@mock.patch('webbreaker.fortify.upload.FortifyAuth')
@mock.patch('webbreaker.fortify.upload.FortifyConfig')
def test_fortify_upload_upload_successful_upload(config_mock, auth_mock, client_mock):
    expected_username = 'user'
    expected_password = 'password'
    expected_application = 'Test Application'
    expected_version = 'Test Version'
    expected_scan_name = 'Test Scan Name'
    expected_project_template = 'Test Template'
    expected_ssc_url = "test.url"

    auth_mock.return_value.authenticate.return_value = expected_username, expected_password
    config_mock.return_value.project_template = expected_project_template
    config_mock.return_value.ssc_url = expected_ssc_url

    fortify_upload = FortifyUpload(username=expected_username,
                                   password=expected_password,
                                   application_name=expected_application,
                                   version_name=expected_version,
                                   scan_name=expected_scan_name,
                                   custom_value=None)

    assert fortify_upload.username == expected_username
    assert fortify_upload.password == expected_password

    client_mock.assert_called_once_with(fortify_password='password', fortify_url='test.url', fortify_username='user')
    assert config_mock.call_count == 1
    assert auth_mock.call_count == 1
    assert client_mock.call_count == 1


@mock.patch('webbreaker.fortify.upload.FortifyHelper')
@mock.patch('webbreaker.fortify.upload.FortifyAuth')
@mock.patch('webbreaker.fortify.upload.FortifyConfig')
@mock.patch('webbreaker.fortify.upload.Logger.app.critical')
def test_fortify_upload_upload_throws_value_error(log_mock, config_mock, auth_mock, client_mock):
    expected_username = 'user'
    expected_password = 'password'
    expected_application = 'Test Application'
    expected_version = 'Test Version'
    expected_scan_name = 'Test Scan Name'
    expected_project_template = 'Test Template'

    auth_mock.return_value.authenticate.return_value = expected_username, expected_password
    config_mock.return_value.project_template = expected_project_template
    config_mock.project_template()
    client_mock.side_effect = value_error_exception

    with pytest.raises(SystemExit):
        FortifyUpload(username=expected_username,
                      password=expected_password,
                      application_name=expected_application,
                      version_name=expected_version,
                      scan_name=expected_scan_name,
                      custom_value=None)

    log_mock.assert_called_once()


@mock.patch('webbreaker.fortify.upload.FortifyHelper')
@mock.patch('webbreaker.fortify.upload.FortifyAuth')
@mock.patch('webbreaker.fortify.upload.FortifyConfig')
@mock.patch('webbreaker.fortify.upload.Logger.app.error')
def test_fortify_upload_upload_throws_unbound_local_error(log_mock, config_mock, auth_mock, client_mock):
    expected_username = 'user'
    expected_password = 'password'
    expected_application = 'Test Application'
    expected_version = 'Test Version'
    expected_scan_name = 'Test Scan Name'
    expected_project_template = 'Test Template'

    auth_mock.return_value.authenticate.return_value = expected_username, expected_password
    config_mock.return_value.project_template = expected_project_template
    config_mock.project_template()
    client_mock.side_effect = unbound_local_error_exception

    with pytest.raises(SystemExit):
        FortifyUpload(username=expected_username,
                      password=expected_password,
                      application_name=expected_application,
                      version_name=expected_version,
                      scan_name=expected_scan_name,
                      custom_value=None)

    log_mock.assert_called_once()


@mock.patch('webbreaker.fortify.upload.FortifyHelper')
@mock.patch('webbreaker.fortify.upload.FortifyAuth')
@mock.patch('webbreaker.fortify.upload.FortifyConfig')
@mock.patch('webbreaker.fortify.upload.Logger.app.critical')
def test_fortify_upload_upload_throws_io_error(log_mock, config_mock, auth_mock, client_mock):
    expected_username = 'user'
    expected_password = 'password'
    expected_application = 'Test Application'
    expected_version = 'Test Version'
    expected_scan_name = 'Test Scan Name'
    expected_project_template = 'Test Template'

    auth_mock.return_value.authenticate.return_value = expected_username, expected_password
    config_mock.return_value.project_template = expected_project_template
    config_mock.project_template()
    client_mock.side_effect = io_error_exception

    with pytest.raises(SystemExit):
        FortifyUpload(username=expected_username,
                      password=expected_password,
                      application_name=expected_application,
                      version_name=expected_version,
                      scan_name=expected_scan_name,
                      custom_value=None)

    log_mock.assert_called_once()
