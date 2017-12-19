import pytest
import mock
import logging

from testfixtures import LogCapture
from webbreaker.__main__ import cli as webbreaker

import json
from mock import mock_open

# Disable debugging for log clarity in testing
logging.disable(logging.DEBUG)


@pytest.fixture(scope="module")
def runner():
    from click.testing import CliRunner
    return CliRunner()


@pytest.fixture()
def caplog():
    return LogCapture()


def general_exception():
    raise Exception('Test Failure')


def general_func(**kwargs):
    return True


# Move hard coded values to params
class WebInspectResponseTest(object):
    """Container for all WebInspect API responses, even errors."""

    def __init__(self):
        self.message = "This was only a test!"
        self.success = True
        self.response_code = "200"
        self.data = {"ScanId": "FakeScanID", "ScanStatus": "complete"}

    def __str__(self):
        if self.data:
            return str(self.data)
        else:
            return self.message

    def data_json(self, pretty=False):
        """Returns the data as a valid JSON string."""
        if pretty:
            return json.dumps(self.data, sort_keys=True, indent=4, separators=(',', ': '))
        else:
            return json.dumps(self.data)


@mock.patch('webbreaker.__main__.WebinspectQueryClient')
def test_webinspect_download_req_no_scans_found(test_mock, runner, caplog):
    test_mock.return_value.get_scan_by_name.return_value = []
    test_mock.return_value.export_scan_results.return_value = None
    test_mock.get_scan_by_name()
    test_mock.export_scan_results()

    result = runner.invoke(webbreaker,
                           ['webinspect', 'download', '--server', 'test-server', '--scan_name', 'test-name'])

    caplog.check(
        ('__webbreaker__', 'ERROR', 'No scans matching the name test-name where found on this host'),
    )
    caplog.uninstall()

    assert result.exit_code == 0


@mock.patch('webbreaker.__main__.WebinspectQueryClient')
def test_webinspect_download_req_one_scan_found(test_mock, runner, caplog):
    test_mock.return_value.get_scan_by_name.return_value = [{'Name': 'test-name', 'ID': 1234, 'Status': 'test'}]
    test_mock.return_value.export_scan_results.return_value = None
    test_mock.get_scan_by_name()
    test_mock.export_scan_results()

    result = runner.invoke(webbreaker,
                           ['webinspect', 'download', '--server', 'test-server', '--scan_name', 'test-name'])

    caplog.check(
        ('__webbreaker__', 'INFO', 'Scan matching the name test-name found.'),
        ('__webbreaker__', 'INFO', 'Downloading scan test-name'),
    )
    caplog.uninstall()

    assert result.exit_code == 0


@mock.patch('webbreaker.__main__.WebinspectQueryClient')
def test_webinspect_download_req_many_scans_found(test_mock, runner, caplog):
    test_mock.return_value.get_scan_by_name.return_value = [{'Name': 'test-name', 'ID': 1234, 'Status': 'test'},
                                                            {'Name': 'test-name2', 'ID': 12345, 'Status': 'test2'}]
    test_mock.get_scan_by_name()

    result = runner.invoke(webbreaker,
                           ['webinspect', 'download', '--server', 'test-server', '--scan_name', 'test-name'])

    caplog.check(
        ('__webbreaker__', 'INFO', 'Multiple scans matching the name test-name found.'),
    )
    caplog.uninstall()

    assert result.exit_code == 0


@mock.patch('webbreaker.__main__.WebinspectQueryClient')
def test_webinspect_download_req_exception(test_mock, runner, caplog):
    test_mock.return_value.get_scan_by_name.side_effect = general_exception
    test_mock.get_scan_by_name()

    result = runner.invoke(webbreaker,
                           ['webinspect', 'download', '--server', 'test-server', '--scan_name', 'test-name'])

    caplog.check()
    caplog.uninstall()

    assert result.exit_code == -1


@mock.patch('webbreaker.__main__.WebinspectQueryClient')
def test_webinspect_list_req_success(test_mock, runner, caplog):
    test_mock.return_value.list_scans.return_value = None

    result = runner.invoke(webbreaker, ['webinspect', 'list', '--server', 'test-server'])

    # list_scans handles the logging
    caplog.check()
    caplog.uninstall()

    assert result.exit_code == 0


@mock.patch('webbreaker.__main__.WebinspectQueryClient')
def test_webinspect_list_req_exception(test_mock, runner, caplog):
    test_mock.return_value.list_scans.side_effect = general_exception

    result = runner.invoke(webbreaker, ['webinspect', 'list', '--server', 'test-server'])

    caplog.check()
    caplog.uninstall()

    assert result.exit_code == -1


@mock.patch('webbreaker.__main__.WebinspectQueryClient')
def test_webinspect_list_scan_name_match(test_mock, runner, caplog):
    test_mock.return_value.get_scan_by_name.return_value = [{'Name': 'test-name', 'ID': 1234, 'Status': 'test'}]
    test_mock.get_scan_by_name()

    result = runner.invoke(webbreaker,
                           ['webinspect', 'list', '--server', 'test-server01', '--server', 'test-server02',
                            '--scan_name', 'test-name'])

    caplog.check()
    caplog.uninstall()
    assert 'Scans matching the name test-name found on test-server01' in result.output
    assert 'Scans matching the name test-name found on test-server02' in result.output

    assert result.exit_code == 0


@mock.patch('webbreaker.__main__.WebinspectQueryClient')
def test_webinspect_list_scan_name_match_multi_server(test_mock, runner, caplog):
    test_mock.return_value.get_scan_by_name.return_value = [{'Name': 'test-name', 'ID': 1234, 'Status': 'test'}]
    test_mock.get_scan_by_name()

    result = runner.invoke(webbreaker,
                           ['webinspect', 'list', '--server', 'test-server', '--server', 'test-server2', '--scan_name',
                            'test-name'])

    caplog.check()
    caplog.uninstall()

    assert result.exit_code == 0


@mock.patch('webbreaker.__main__.WebinspectQueryClient')
def test_webinspect_list_scan_name_no_match(test_mock, runner, caplog):
    test_mock.return_value.get_scan_by_name.return_value = []
    test_mock.get_scan_by_name()

    result = runner.invoke(webbreaker,
                           ['webinspect', 'list', '--server', 'test-server', '--scan_name', 'test-name'])

    caplog.check(
        ('__webbreaker__', 'ERROR', 'No scans matching the name test-name were found on test-server'),
    )
    caplog.uninstall()

    assert result.exit_code == 0


@mock.patch('webbreaker.__main__.WebinspectQueryClient')
def test_webinspect_list_scan_name_no_match_multi_server(test_mock, runner, caplog):
    test_mock.return_value.get_scan_by_name.return_value = []
    test_mock.get_scan_by_name()

    result = runner.invoke(webbreaker,
                           ['webinspect', 'list', '--server', 'test-server', '--server', 'test-server2', '--scan_name',
                            'test-name'])

    caplog.check(
        ('__webbreaker__', 'ERROR', 'No scans matching the name test-name were found on test-server'),
        ('__webbreaker__', 'ERROR', 'No scans matching the name test-name were found on test-server2'),
    )
    caplog.uninstall()

    assert result.exit_code == 0


@mock.patch('webbreaker.__main__.WebinspectQueryClient')
def test_webinspect_list_scan_name_error(test_mock, runner, caplog):
    test_mock.return_value.get_scan_by_name.side_effect = general_exception
    test_mock.get_scan_by_name()

    result = runner.invoke(webbreaker,
                           ['webinspect', 'list', '--server', 'test-server', '--scan_name', 'test-name'])

    caplog.check()
    caplog.uninstall()

    assert result.exit_code == -1


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


# TODO: webbreaker webinespect download

# TODO: webinspect scan [OPTIONS]
# Write a test for False success and failure in create_scan. Just change WebInspectResponseTest() to False


@mock.patch('webbreaker.__main__.create_scan_event_handler')
@mock.patch('webbreaker.webinspectclient.WebInspectJitScheduler')
@mock.patch('webbreaker.webinspectclient.webinspectapi.WebInspectApi')
@mock.patch('webbreaker.webinspectclient.open', new_callable=mock_open, read_data="data")
@mock.patch('webbreaker.__main__.open', new_callable=mock_open, read_data="data")
def test_webinspect_scan_req(main_open_mock, open_mock, scan_mock, endpoint_mock, email_mock, runner, caplog):
    endpoint_mock.return_value.get_endpoint.return_value = "test.hq.target.com"
    endpoint_mock.has_auth_creds()

    scan_mock.return_value.create_scan.return_value = WebInspectResponseTest()
    scan_mock.create_scan()
    scan_mock.return_value.get_current_status.return_value = WebInspectResponseTest()
    scan_mock.get_current_status()
    scan_mock.return_value.export_scan_format.return_value = WebInspectResponseTest()
    scan_mock.export_scan_format()

    email_mock.handle_scan_event = True

    result = runner.invoke(webbreaker,
                           ['webinspect', 'scan'])

    caplog.check(
        ('__webbreaker__', 'INFO', "Finding endpoints. Expect a slight delay"),
        ('__webbreaker__', 'INFO', "Launching a scan"),
        ('__webbreaker__', 'INFO', "Execution is waiting on scan status change"),
        ('__webbreaker__', 'INFO', "Scan status has changed to complete."),
        ('__webbreaker__', 'INFO', "Exporting scan: FakeScanID as fpr"),
        ('__webbreaker__', 'INFO', "Exporting scan: FakeScanID as xml"),
        ('__webbreaker__', 'INFO', "Webbreaker WebInspect has completed."),
    )
    caplog.uninstall()

    assert result.exit_code == 0


@mock.patch('webbreaker.__main__.WebInspectConfig')
def test_webinspect_servers(test_mock, runner, caplog):
    result = runner.invoke(webbreaker, ['webinspect', 'servers'])

    # WebInspectConfig handles all logging
    caplog.check()
    caplog.uninstall()

    assert result.exit_code == 0
