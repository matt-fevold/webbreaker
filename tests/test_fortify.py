import pytest
import mock

from testfixtures import LogCapture
from webbreaker.__main__ import cli as webbreaker


@pytest.fixture(scope="module")
def runner():
    from click.testing import CliRunner
    return CliRunner()


@pytest.fixture()
def caplog():
    return LogCapture()


def value_error_exception(**kwargs):
    raise ValueError('Test Failure')


def attr_error(test_var):
    raise AttributeError('Test Failure')


@mock.patch('webbreaker.__main__.FortifyConfig')
@mock.patch('webbreaker.__main__.FortifyClient')
def test_fortify_list_success(client_mock, test_mock, runner, caplog):
    test_mock.return_value.has_auth_creds.return_value = True
    test_mock.has_auth_creds()
    client_mock.return_value.list_versions.return_value = None
    client_mock.list_versions()

    result = runner.invoke(webbreaker, ['fortify', 'list'])

    caplog.check(
        ('__webbreaker__', 'INFO', 'No Fortify username or password provided. Checking config.ini for credentials'),
        ('__webbreaker__', 'INFO', 'Fortify username and password successfully found in config.ini'),
        ('__webbreaker__', 'INFO', 'Fortify list has successfully completed'),
    )
    caplog.uninstall()

    assert result.exit_code == 0


@mock.patch('webbreaker.__main__.FortifyConfig')
@mock.patch('webbreaker.__main__.FortifyClient')
def test_fortify_list_client_init_exeception(client_mock, test_mock, runner, caplog):
    test_mock.return_value.has_auth_creds.return_value = True
    test_mock.has_auth_creds()
    client_mock.side_effect = value_error_exception

    result = runner.invoke(webbreaker, ['fortify', 'list'])

    caplog.check(
        ('__webbreaker__', 'INFO', 'No Fortify username or password provided. Checking config.ini for credentials'),
        ('__webbreaker__', 'ERROR', 'Unable to obtain a Fortify API token. Invalid Credentials'),
    )
    caplog.uninstall()

    assert result.exit_code == 0


@mock.patch('webbreaker.__main__.FortifyConfig')
@mock.patch('webbreaker.__main__.FortifyClient')
def test_fortify_list_list_list_exeception(client_mock, test_mock, runner, caplog):
    test_mock.return_value.has_auth_creds.return_value = True
    test_mock.has_auth_creds()
    client_mock.return_value.list_versions.side_effect = value_error_exception
    client_mock()

    result = runner.invoke(webbreaker, ['fortify', 'list'])

    caplog.check(
        ('__webbreaker__', 'INFO', 'No Fortify username or password provided. Checking config.ini for credentials'),
        ('__webbreaker__', 'INFO', 'Fortify username and password successfully found in config.ini'),
        ('__webbreaker__', 'ERROR', 'Unable to obtain a Fortify API token. Invalid Credentials'),
    )
    caplog.uninstall()

    assert result.exit_code == 0


@mock.patch('webbreaker.__main__.FortifyConfig')
@mock.patch('webbreaker.__main__.FortifyClient')
@mock.patch('webbreaker.__main__.fortify_prompt')
def test_fortify_list_prompt_success(prompt_mock, client_mock, test_mock, runner, caplog):
    test_mock.return_value.has_auth_creds.return_value = False
    test_mock.has_auth_creds()
    prompt_mock.return_value = "admin", "password"
    client_mock.return_value.list_versions.return_value = None
    client_mock.list_application_versions()

    result = runner.invoke(webbreaker, ['fortify', 'list'])

    caplog.check(
        ('__webbreaker__', 'INFO', 'No Fortify username or password provided. Checking config.ini for credentials'),
        ('__webbreaker__', 'INFO', 'Fortify credentials not found in config.ini'),
        ('__webbreaker__', 'INFO', 'Fortify credentials stored'),
        ('__webbreaker__', 'INFO', 'Fortify list has successfully completed'),
    )
    caplog.uninstall()

    print(result.output)
    assert result.exit_code == 0


@mock.patch('webbreaker.__main__.FortifyConfig')
@mock.patch('webbreaker.__main__.FortifyClient')
@mock.patch('webbreaker.__main__.fortify_prompt')
def test_fortify_list_prompt_exception(prompt_mock, client_mock, test_mock, runner, caplog):
    test_mock.return_value.has_auth_creds.return_value = False
    test_mock.has_auth_creds()
    prompt_mock.return_value = "admin", "password"
    client_mock.side_effect = value_error_exception

    result = runner.invoke(webbreaker, ['fortify', 'list'])

    caplog.check(
        ('__webbreaker__', 'INFO', 'No Fortify username or password provided. Checking config.ini for credentials'),
        ('__webbreaker__', 'INFO', 'Fortify credentials not found in config.ini'),
        ('__webbreaker__', 'ERROR', 'Unable to obtain a Fortify API token. Invalid Credentials'),
    )
    caplog.uninstall()

    assert result.exit_code == 0


@mock.patch('webbreaker.__main__.FortifyConfig')
@mock.patch('webbreaker.__main__.FortifyClient')
@mock.patch('webbreaker.__main__.fortify_prompt')
def test_fortify_list_prompt_exception(prompt_mock, client_mock, test_mock, runner, caplog):
    test_mock.return_value.has_auth_creds.return_value = False
    test_mock.has_auth_creds()
    prompt_mock.return_value = "admin", "password"
    client_mock.return_value.list_versions.side_effect = value_error_exception
    client_mock()

    result = runner.invoke(webbreaker, ['fortify', 'list'])

    caplog.check(
        ('__webbreaker__', 'INFO', 'No Fortify username or password provided. Checking config.ini for credentials'),
        ('__webbreaker__', 'INFO', 'Fortify credentials not found in config.ini'),
        ('__webbreaker__', 'INFO', 'Fortify credentials stored'),
        ('__webbreaker__', 'ERROR', 'Unable to obtain a Fortify API token. Invalid Credentials'),
    )
    caplog.uninstall()

    assert result.exit_code == 0


@mock.patch('webbreaker.__main__.FortifyConfig')
@mock.patch('webbreaker.__main__.FortifyClient')
def test_fortify_list_application_exception(client_mock, test_mock, runner, caplog):
    test_mock.return_value.write_username.return_value = None
    test_mock.return_value.write_password.return_value = None
    test_mock.write_username()
    test_mock.write_password()
    client_mock.return_value.list_versions.side_effect = value_error_exception
    client_mock()

    result = runner.invoke(webbreaker,
                           ['fortify', 'list', '--fortify_user', 'admin', '--fortify_password', 'password'])

    caplog.check(
        ('__webbreaker__', 'INFO', 'Importing Fortify credentials'),
        ('__webbreaker__', 'INFO', 'Fortify credentials stored'),
        ('__webbreaker__', 'ERROR', 'Unable to obtain a Fortify API token. Invalid Credentials'),
    )
    caplog.uninstall()

    assert result.exit_code == 0


@mock.patch('webbreaker.__main__.FortifyConfig')
@mock.patch('webbreaker.__main__.FortifyClient')
def test_fortify_list_application_success(client_mock, test_mock, runner, caplog):
    test_mock.return_value.write_username.return_value = None
    test_mock.return_value.write_password.return_value = None
    test_mock.write_username()
    test_mock.write_password()
    client_mock.return_value.list_versions.return_value = None
    client_mock()

    result = runner.invoke(webbreaker,
                           ['fortify', 'list', '--fortify_user', 'admin', '--fortify_password', 'password'])

    caplog.check(
        ('__webbreaker__', 'INFO', 'Importing Fortify credentials'),
        ('__webbreaker__', 'INFO', 'Fortify credentials stored'),
        ('__webbreaker__', 'INFO', 'Fortify list has successfully completed'),
    )
    caplog.uninstall()

    assert result.exit_code == 0


@mock.patch('webbreaker.__main__.FortifyConfig')
@mock.patch('webbreaker.__main__.FortifyClient')
def test_fortify_list_application_success(client_mock, test_mock, runner, caplog):
    test_mock.return_value.has_auth_creds.return_value = True
    test_mock.has_auth_creds()
    client_mock.return_value.list_versions.return_value = None
    client_mock.list_application_versions()

    result = runner.invoke(webbreaker, ['fortify', 'list', '--application', 'test'])

    caplog.check(
        (
            '__webbreaker__', 'INFO', 'No Fortify username or password provided. Checking config.ini for credentials'),
        ('__webbreaker__', 'INFO', 'Fortify username and password successfully found in config.ini'),
        ('__webbreaker__', 'INFO', 'Fortify list has successfully completed'),
    )
    caplog.uninstall()

    assert result.exit_code == 0


@mock.patch('webbreaker.__main__.FortifyConfig')
@mock.patch('webbreaker.__main__.FortifyClient')
def test_fortify_list_application_exception(client_mock, test_mock, runner, caplog):
    test_mock.return_value.has_auth_creds.return_value = True
    test_mock.has_auth_creds()
    client_mock.return_value.list_application_versions.side_effect = attr_error
    client_mock()

    result = runner.invoke(webbreaker, ['fortify', 'list', '--application', 'test'])

    caplog.check(
        ('__webbreaker__', 'INFO', 'No Fortify username or password provided. Checking config.ini for credentials'),
        ('__webbreaker__', 'INFO', 'Fortify username and password successfully found in config.ini'),
        ('__webbreaker__', 'CRITICAL', "Unable to complete command 'fortify list': Test Failure"),
    )
    caplog.uninstall()

    assert result.exit_code == 0

@mock.patch('webbreaker.__main__.FortifyConfig')
@mock.patch('webbreaker.__main__.FortifyClient')
def test_fortify_download_success(client_mock, test_mock, runner, caplog):
    test_mock.return_value.has_auth_creds.return_value = True
    test_mock.has_auth_creds()
    client_mock.return_value.find_version_id.return_value = 123
    client_mock.find_version_id()
    client_mock.return_value.download_scan.return_value = 'testfile.fpr'
    client_mock.download_scan()

    result = runner.invoke(webbreaker, ['fortify', 'download', '--version', 'test_version'])

    caplog.check(
        ('__webbreaker__', 'INFO', 'No Fortify username or password provided. Checking config.ini for credentials'),
        ('__webbreaker__', 'INFO', 'Fortify username and password successfully found in config.ini'),
        ('__webbreaker__', 'INFO', 'Scan file for version 123 successfully written to testfile.fpr'),
    )
    caplog.uninstall()

    assert result.exit_code == 0

@mock.patch('webbreaker.__main__.FortifyConfig')
@mock.patch('webbreaker.__main__.FortifyClient')
def test_fortify_download_failure(client_mock, test_mock, runner, caplog):
    test_mock.return_value.has_auth_creds.return_value = True
    test_mock.has_auth_creds()
    client_mock.return_value.find_version_id.return_value = 123
    client_mock.find_version_id()
    client_mock.return_value.download_scan.return_value = False
    client_mock.download_scan()

    result = runner.invoke(webbreaker, ['fortify', 'download', '--version', 'test_version'])

    caplog.check(
        ('__webbreaker__', 'INFO', 'No Fortify username or password provided. Checking config.ini for credentials'),
        ('__webbreaker__', 'INFO', 'Fortify username and password successfully found in config.ini'),
        ('__webbreaker__', 'ERROR', 'Scan download for version 123 has failed'),
    )
    caplog.uninstall()

    assert result.exit_code == 0

@mock.patch('webbreaker.__main__.FortifyConfig')
@mock.patch('webbreaker.__main__.FortifyClient')
def test_fortify_download_version_id_failure(client_mock, test_mock, runner, caplog):
    test_mock.return_value.has_auth_creds.return_value = True
    test_mock.has_auth_creds()
    client_mock.return_value.find_version_id.return_value = False
    client_mock.find_version_id()
    client_mock.return_value.download_scan.return_value = False
    client_mock.download_scan()

    result = runner.invoke(webbreaker, ['fortify', 'download', '--application', 'test_app', '--version', 'test_version'])

    caplog.check(
        ('__webbreaker__', 'INFO', 'No Fortify username or password provided. Checking config.ini for credentials'),
        ('__webbreaker__', 'INFO', 'Fortify username and password successfully found in config.ini'),
        ('__webbreaker__', 'ERROR', 'No version matching test_version found under test_app in Fortify'),
    )
    caplog.uninstall()

    assert result.exit_code == 0

# TODO: Test webbreaker fortifiy upload
# TODO: Test webbreaker fortify scan
