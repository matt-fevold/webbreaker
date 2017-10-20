import pytest
import mock
import click

from testfixtures import LogCapture
from webbreaker.__main__ import cli as webbreaker


@pytest.fixture(scope="module")
def runner():
    from click.testing import CliRunner
    return CliRunner()


@pytest.fixture()
def caplog():
    return LogCapture()


def general_exception():
    raise Exception('Test Failure')


# def test_webinspect_scan_scan_name(runner):
#     result = runner.invoke(webbreaker,  ['scan', '--scan_name'])
#     assert result.exit_code == 0


def test_webinspect_scan(runner):
    result = runner.invoke(webbreaker, ['scan', '--settings tmp'])
    click.echo('CLI output is: \n\n' + result.output)
    assert result.exit_code == 2


# def test_webinspect_scan_size(runner):
#     result = runner.invoke(webbreaker,  ['scan', '--size'])
#     assert result.exit_code == 0
#
#
# def test_webinspect_scan_scan_mode(runner):
#     result = runner.invoke(webbreaker,  ['scan', '--scan_mode'])
#     assert result.exit_code == 0
#
#
# def test_webinspect_scan_scan_scope(runner):
#     result = runner.invoke(webbreaker,  ['scan', '--scan_scope'])
#     assert result.exit_code == 0
#
#
# def test_webinspect_scan_login_macro(runner):
#     result = runner.invoke(webbreaker,  ['scan', '--login_macro'])
#     assert result.exit_code == 0
#
#
# def test_webinspect_scan_scan_policy(runner):
#     result = runner.invoke(webbreaker,  ['scan', '--scan_policy'])
#     assert result.exit_code == 0
#
#
# def test_webinspect_scan_scan_start(runner):
#     result = runner.invoke(webbreaker,  ['scan', '--scan_start'])
#     assert result.exit_code == 0
#
#
# def test_webinspect_scan_start_urls(runner):
#     result = runner.invoke(webbreaker,  ['scan', '--start_urls'])
#     assert result.exit_code == 0
#
#
# def test_webinspect_scan_upload_settings(runner):
#     result = runner.invoke(webbreaker,  ['scan', '--upload_settings'])
#     assert result.exit_code == 0
#
#
# def test_webinspect_scan_upload_policy(runner):
#     result = runner.invoke(webbreaker,  ['scan', '--upload_policy'])
#     assert result.exit_code == 0
#
#
# def test_webinspect_scan_upload_webmacros(runner):
#     result = runner.invoke(webbreaker,  ['scan', '--upload_webmacros'])
#     assert result.exit_code == 0
#
#
# def test_webinspect_scan_fortify_user(runner):
#     result = runner.invoke(webbreaker,  ['scan', '--fortify_user'])
#     assert result.exit_code == 0
#
#
# def test_webinspect_scan_allowed_hosts(runner):
#     result = runner.invoke(webbreaker,  ['scan', '--allowed_hosts'])
#     assert result.exit_code == 0
#
#
# def test_webinspect_scan_workflow_macros(runner):
#     result = runner.invoke(webbreaker,  ['scan', '--workflow_macros'])
#     assert result.exit_code == 0
#

def test_webinspect_download(runner):
    result = runner.invoke(webbreaker, ['download', '--server', '--scan_name'])
    assert result.exit_code == 2


# def test_webinspect_download_scan_name(runner):
#     result = runner.invoke(webbreaker,  ['download', '--scan_name'])
#     assert result.exit_code == 0
#
#
# def test_webinspect_download_scan_id(runner):
#     result = runner.invoke(webbreaker,  ['download', '--scan_id'])
#     assert result.exit_code == 0
#
#
# def test_webinspect_download_x(runner):
#     result = runner.invoke(webbreaker,  ['download', '-x'])
#     assert result.exit_code == 0
#
#
# def test_webinspect_download_protocol(runner):
#     result = runner.invoke(webbreaker,  ['download', '--protocol'])
#     assert result.exit_code == 0


@mock.patch('webbreaker.__main__.WebinspectQueryClient')
def test_webinspect_list_no_scan_name_success(test_mock, runner, caplog):
    test_mock.return_value.list_scans.return_value = None

    result = runner.invoke(webbreaker, ['webinspect', 'list', '--server', 'test-server'])

    # list_scans handles the logging
    caplog.check()
    caplog.uninstall()

    assert result.exit_code == 0


@mock.patch('webbreaker.__main__.WebinspectQueryClient')
def test_webinspect_list_no_scan_name_failure(test_mock, runner, caplog):
    test_mock.return_value.list_scans.side_effect = general_exception

    result = runner.invoke(webbreaker, ['webinspect', 'list', '--server', 'test-server'])

    caplog.check(
        ('__webbreaker__', 'ERROR', "Unable to complete command 'webinspect list'"),
    )
    caplog.uninstall()

    assert result.exit_code == 0


@mock.patch('webbreaker.__main__.WebinspectQueryClient')
def test_webinspect_list_scan_name_match(test_mock, runner, caplog):
    test_mock.return_value.get_scan_by_name.return_value = [{'Name': 'test', 'ID': 1234, 'Status': 'test'}]
    test_mock.get_scan_by_name()

    result = runner.invoke(webbreaker,
                           ['webinspect', 'list', '--server', 'test-server', '--scan_name', 'test-name'])

    caplog.check(
        ('__webbreaker__', 'INFO', 'Successfully exported webinspect list: test-name'),
    )
    caplog.uninstall()

    assert result.exit_code == 0


@mock.patch('webbreaker.__main__.WebinspectQueryClient')
def test_webinspect_list_scan_name_no_match(test_mock, runner, caplog):
    test_mock.return_value.get_scan_by_name.return_value = []
    test_mock.get_scan_by_name()

    result = runner.invoke(webbreaker,
                           ['webinspect', 'list', '--server', 'test-server', '--scan_name', 'test-name'])

    print(result.output)
    print(caplog)
    caplog.check(
        ('__webbreaker__', 'ERROR', 'No scans matching the name test-name were found.'),
    )
    caplog.uninstall()

    assert result.exit_code == 0


@mock.patch('webbreaker.__main__.WebinspectQueryClient')
def test_webinspect_list_scan_name_error(test_mock, runner, caplog):
    test_mock.return_value.get_scan_by_name.side_effect = general_exception
    test_mock.get_scan_by_name()

    result = runner.invoke(webbreaker,
                           ['webinspect', 'list', '--server', 'test-server', '--scan_name', 'test-name'])

    caplog.check(
        ('__webbreaker__', 'ERROR', "Unable to complete command 'webinspect list'"),
    )
    caplog.uninstall()

    assert result.exit_code == 0


@mock.patch('webbreaker.__main__.WebinspectQueryClient')
def test_webinspect_list_protocol_wrong_type(test_mock, runner, caplog):
    test_mock.return_value.list_scans.return_value = None

    result = runner.invoke(webbreaker,
                           ['webinspect', 'list', '--server', 'test-server', '--protocol', 'failure'])

    # Checks for no logs, click doesn't log, just print to stdout
    caplog.check()
    caplog.uninstall()

    assert result.exit_code == 2


@mock.patch('webbreaker.__main__.WebinspectQueryClient')
def test_webinspect_list_protocol_change_success(test_mock, runner, caplog):
    test_mock.return_value.list_scans.return_value = None

    result = runner.invoke(webbreaker,
                           ['webinspect', 'list', '--server', 'http://test-server', '--protocol', 'https'])

    # WebInspectQueryClient handles all logging
    caplog.check()
    caplog.uninstall()

    assert result.exit_code == 0
