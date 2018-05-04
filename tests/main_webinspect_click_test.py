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


def environment_error_exception():
    raise EnvironmentError('Test Failure')


def unbound_local_error_exception():
    raise UnboundLocalError('Test Failure')


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


@mock.patch('webbreaker.__main__.WebInspectListServers.__init__')
def test_webinspect_list_servers(list_server_mock, runner):
    list_server_mock.return_value = None

    # Run the CLI --servers
    runner.invoke(webbreaker, ['webinspect', '--servers'])

    list_server_mock.assert_called_once_with()


@mock.patch('webbreaker.__main__.WebInspectListScans.__init__')
def test_webinspect_list_one_server(list_scan_mock, runner):
    list_scan_mock.return_value = None

    runner.invoke(webbreaker, ['webinspect', 'list', '--server', 'server1'])

    list_scan_mock.assert_called_once_with(None, ('server1',), None, None)


@mock.patch('webbreaker.__main__.WebInspectListScans.__init__')
def test_webinspect_list_two_servers(list_scan_mock, runner):
    list_scan_mock.return_value = None

    runner.invoke(webbreaker, ['webinspect', 'list', '--server', 'server1', '--server', 'server2'])

    list_scan_mock.assert_called_once_with(None, ('server1', 'server2'), None, None)


@mock.patch('webbreaker.__main__.WebInspectListScans.__init__')
def test_webinspect_list_two_servers_with_scan_name(list_scan_mock, runner):
    list_scan_mock.return_value = None

    runner.invoke(webbreaker, ['webinspect', 'list', '--server', 'server1', '--server', 'server2', '--scan_name',
                               'important_site'])

    list_scan_mock.assert_called_once_with('important_site', ('server1', 'server2'), None, None)


@mock.patch('webbreaker.__main__.WebInspectListScans.__init__')
def test_webinspect_list_scans(list_scan_mock, runner):
    list_scan_mock.return_value = None

    runner.invoke(webbreaker, ['webinspect', 'list'])

    list_scan_mock.assert_called_once_with(None, (), None, None)


@mock.patch('webbreaker.__main__.WebInspectListScans.__init__')
def test_webinspect_list_username_password(list_scan_mock, runner):
    list_scan_mock.return_value = None

    runner.invoke(webbreaker, ['webinspect', 'list', '--username', 'user', '--password', 'pass'])

    list_scan_mock.assert_called_once_with(None, (), 'user', 'pass')


@mock.patch('webbreaker.__main__.WebInspectDownload.__init__')
def test_webinspect_download(download_mock, runner):
    download_mock.return_value = None

    runner.invoke(webbreaker, ['webinspect', 'download', '--server', 'server', '--scan_name', 'important_site'])

    download_mock.assert_called_once_with('server', 'important_site', None, 'fpr', None, None)


@mock.patch('webbreaker.__main__.WebInspectDownload.__init__')
def test_webinspect_download_username_password(download_mock, runner):
    download_mock.return_value = None

    runner.invoke(webbreaker, ['webinspect', 'download', '--server', 'server', '--scan_name', 'important_site',
                               '--username', 'user', '--password', 'pass'])

    download_mock.assert_called_once_with('server', 'important_site', None, 'fpr', 'user', 'pass')


@mock.patch('webbreaker.__main__.WebInspectDownload.__init__')
def test_webinspect_download_extension(download_mock, runner):
    download_mock.return_value = None

    runner.invoke(webbreaker, ['webinspect', 'download', '--server', 'server', '--scan_name', 'important_site', '-x',
                               'xml'])

    download_mock.assert_called_once_with('server', 'important_site', None, 'xml', None, None)


@mock.patch('webbreaker.__main__.WebInspectDownload.__init__')
def test_webinspect_download_scan_id(download_mock, runner):
    download_mock.return_value = None

    runner.invoke(webbreaker, ['webinspect', 'download', '--server', 'server', '--scan_name', 'important_site',
                               '--scan_id', 'my_important_scan_id'])

    download_mock.assert_called_once_with('server', 'important_site', 'my_important_scan_id', 'fpr', None, None)


@mock.patch('webbreaker.__main__.WebInspectScan.__init__')
def test_webinspect_scan(scan_mock, runner):
    scan_mock.return_value = None

    runner.invoke(webbreaker, ['webinspect', 'scan'])

    scan_mock.assert_called_once_with({'username': None, 'start_urls': (), 'scan_scope': None, 'upload_policy': None,
                                       'upload_webmacros': None, 'scan_start': None, 'workflow_macros': (),
                                       'upload_settings': None, 'password': None, 'size': 'large', 'settings': 'Default',
                                       'scan_name': None, 'login_macro': None, 'scan_policy': None, 'allowed_hosts': (),
                                       'fortify_user': None, 'scan_mode': None, 'timeout': 0})


@mock.patch('webbreaker.__main__.WebInspectScan.__init__')
def test_webinspect_scan_custom_settings(scan_mock, runner):
    scan_mock.return_value = None

    runner.invoke(webbreaker, ['webinspect', 'scan', '--settings', 'important_site_auth'])

    scan_mock.assert_called_once_with({'username': None, 'start_urls': (), 'scan_scope': None, 'upload_policy': None,
                                       'upload_webmacros': None, 'scan_start': None, 'workflow_macros': (),
                                       'upload_settings': None, 'password': None, 'size': 'large',
                                       'settings': 'important_site_auth', 'scan_name': None, 'login_macro': None,
                                       'scan_policy': None, 'allowed_hosts': (), 'fortify_user': None,
                                       'scan_mode': None})


@mock.patch('webbreaker.__main__.WebInspectScan.__init__')
def test_webinspect_scan_custom_settings_with_username_password(scan_mock, runner):
    scan_mock.return_value = None

    runner.invoke(webbreaker, ['webinspect', 'scan', '--settings', 'important_site_auth', '--username', 'user',
                               '--password', 'pass'])

    scan_mock.assert_called_once_with({'username': 'user', 'start_urls': (), 'scan_scope': None, 'upload_policy': None,
                                       'upload_webmacros': None, 'scan_start': None, 'workflow_macros': (),
                                       'upload_settings': None, 'password': 'pass', 'size': 'large',
                                       'settings': 'important_site_auth', 'scan_name': None, 'login_macro': None,
                                       'scan_policy': None, 'allowed_hosts': (), 'fortify_user': None,
                                       'scan_mode': None})


@mock.patch('webbreaker.__main__.WebInspectScan.__init__')
def test_webinspect_scan_custom_settings_with_two_allowed_hosts(scan_mock, runner):
    scan_mock.return_value = None

    runner.invoke(webbreaker, ['webinspect', 'scan', '--settings', 'important_site_auth', '--allowed_hosts',
                               'example.com', '--allowed_hosts', 'example1.com'])

    scan_mock.assert_called_once_with({'username': None, 'start_urls': (), 'scan_scope': None, 'upload_policy': None,
                                       'upload_webmacros': None, 'scan_start': None, 'workflow_macros': (),
                                       'upload_settings': None, 'password': None, 'size': 'large',
                                       'settings': 'important_site_auth', 'scan_name': None, 'login_macro': None,
                                       'scan_policy': None, 'allowed_hosts': ('example.com', 'example1.com',),
                                       'fortify_user': None, 'scan_mode': None})


@mock.patch('webbreaker.__main__.WebInspectScan.__init__')
def test_webinspect_scan_local_custom_settings(scan_mock, runner):
    scan_mock.return_value = None

    runner.invoke(webbreaker, ['webinspect', 'scan', '--settings', '/users/me/important_site_auth'])

    scan_mock.assert_called_once_with({'username': None, 'start_urls': (), 'scan_scope': None, 'upload_policy': None,
                                       'upload_webmacros': None, 'scan_start': None, 'workflow_macros': (),
                                       'upload_settings': None, 'password': None, 'size': 'large',
                                       'settings': '/users/me/important_site_auth', 'scan_name': None,
                                       'login_macro': None, 'scan_policy': None, 'allowed_hosts': (),
                                       'fortify_user': None, 'scan_mode': None})


@mock.patch('webbreaker.webinspect.list_servers.WebInspectConfig')
def test_webinspect_list_servers(test_mock, runner, caplog):
    result = runner.invoke(webbreaker, ['webinspect', 'servers'])

    # WebInspectConfig handles all logging
    caplog.check()
    caplog.uninstall()

    assert result.exit_code == 0


# WebInspect CLI Proxy Testing

@mock.patch('webbreaker.__main__.WebInspectProxy.__init__')
def test_webinspect_proxy_list_available_proxies(proxy_mock, runner):
    proxy_mock.return_value = None

    runner.invoke(webbreaker, ['webinspect', 'proxy', '--list', '--server', 'https://test-server'])

    proxy_mock.assert_called_once_with(False, True, None, None, False, 'https://test-server', False, False, None, False,
                                       None, None)


@mock.patch('webbreaker.__main__.WebInspectProxy.__init__')
def test_webinspect_proxy_start(proxy_mock, runner):
    proxy_mock.return_value = None

    runner.invoke(webbreaker, ['webinspect', 'proxy', '--start', '--proxy_name', 'test'])

    proxy_mock.assert_called_once_with(False, False, None, 'test', False, None, True, False, None, False,
                                       None, None)


@mock.patch('webbreaker.__main__.WebInspectProxy.__init__')
def test_webinspect_proxy_start_with_port_name(proxy_mock, runner):
    proxy_mock.return_value = None

    runner.invoke(webbreaker, ['webinspect', 'proxy', '--start','--port', '9001', '--proxy_name', 'test'])

    proxy_mock.assert_called_once_with(False, False, '9001', 'test', False, None, True, False, None, False,
                                       None, None)


@mock.patch('webbreaker.__main__.WebInspectProxy.__init__')
def test_webinspect_proxy_download_webmacro(proxy_mock, runner):
    proxy_mock.return_value = None

    runner.invoke(webbreaker, ['webinspect', 'proxy', '--download', '--webmacro', '--proxy_name', 'test'])

    proxy_mock.assert_called_once_with(True, False, None, 'test', False, None, False, False, None, True,
                                       None, None)


@mock.patch('webbreaker.__main__.WebInspectProxy.__init__')
def test_webinspect_proxy_download_setting(proxy_mock, runner):
    proxy_mock.return_value = None

    runner.invoke(webbreaker, ['webinspect', 'proxy', '--download', '--setting', '--proxy_name', 'test'])

    proxy_mock.assert_called_once_with(True, False, None, 'test', True, None, False, False, None, False,
                                       None, None)


@mock.patch('webbreaker.__main__.WebInspectProxy.__init__')
def test_webinspect_proxy_upload(proxy_mock, runner):
    proxy_mock.return_value = None

    runner.invoke(webbreaker, ['webinspect', 'proxy', '--upload', 'test-proxy.webmacro', '--proxy_name', 'test'])

    proxy_mock.assert_called_once_with(False, False, None, 'test', False, None, False, False, 'test-proxy.webmacro',
                                       False, None, None)


@mock.patch('webbreaker.__main__.WebInspectProxy.__init__')
def test_webinspect_proxy_stop(proxy_mock, runner):
    proxy_mock.return_value = None

    runner.invoke(webbreaker, ['webinspect', 'proxy', '--stop', '--proxy_name', 'test'])

    proxy_mock.assert_called_once_with(False, False, None, 'test', False, None, False, True, None, False,
                                       None, None)


@mock.patch('webbreaker.__main__.WebInspectWiswag.__init__')
def test_webinspect_wiswag(wiswag_mock, runner):
    wiswag_mock.return_value = None

    runner.invoke(webbreaker, ['webinspect', 'wiswag', '--url', 'http://petstore.swagger.io/v2/swagger.json', '--wiswag_name', 'Petstore'])

    wiswag_mock.assert_called_once_with('http://petstore.swagger.io/v2/swagger.json', 'Petstore', None, None, None)
