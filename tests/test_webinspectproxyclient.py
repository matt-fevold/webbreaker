import mock
import pytest
import logging
import re
from testfixtures import LogCapture
from mock import mock_open

from webbreaker.webinspectproxyclient import WebinspectProxyClient
from webinspectapi.webinspect import WebInspectResponse

try:
    import ConfigParser as configparser

    config = configparser.SafeConfigParser()
except ImportError:  # Python3
    import configparser

    config = configparser.ConfigParser()

# Disable debugging for log clarity in testing
logging.disable(logging.DEBUG)


@pytest.fixture()
def caplog():
    return LogCapture()


class ClassHelper(object):
    def __init__(self, success=False):
        self.success = success
        self.cert = '/test/cert/path'
        self.message = 'Test api message'
        self.data = 'Test data'

    def get_endpoint(self):
        return 'test-server'

    def cert_proxy(self):
        return WebInspectResponse(success=self.success, message=self.message, data=self.data)

    def start_proxy(self, id=None, port=None, address=None):
        return WebInspectResponse(success=self.success, message=self.message, data=self.data)

    def delete_proxy(self, instance_id=None):
        return WebInspectResponse(success=self.success, message=self.message, data=self.data)

    def list_proxies(self):
        return WebInspectResponse(success=self.success, message=self.message, data=self.data)

    def get_proxy_information(self, instance_id=None):
        return WebInspectResponse(success=self.success, message=self.message, data=self.data)

    def download_proxy_webmacro(self, instance_id=None):
        return WebInspectResponse(success=self.success, message=self.message, data=self.data)

    def download_proxy_setting(self, instance_id=None):
        return WebInspectResponse(success=self.success, message=self.message, data=self.data)

    def upload_webmacro_proxy(self, id=None, macro_file_path=None):
        return WebInspectResponse(success=self.success, message=self.message, data=self.data)


def test_config_init_variables_none():
    test_obj = WebinspectProxyClient(None, None, None)

    r = re.compile('webinspect-[a-zA-Z0-9]{5}')
    assert bool(r.match(test_obj.proxy_name)) is True
    assert test_obj.port is ""
    assert test_obj.host is None


def test_config_init_variables_all_set():
    test_obj = WebinspectProxyClient('test-id', '80', 'test-server')

    assert test_obj.proxy_name == 'test-id'
    assert test_obj.port == '80'
    assert test_obj.host == "test-server"


@mock.patch('webinspectapi.webinspect.WebInspectApi')
@mock.patch('webbreaker.webinspectproxyclient.open', new_callable=mock_open, read_data="data")
def test_get_cert_proxy_success(open_mock, api_mock):
    api_mock.return_value = ClassHelper(True)

    test_obj = WebinspectProxyClient('test-id', '80', 'test-server')
    test_obj.get_cert_proxy()

    assert open_mock.call_count == 1


@mock.patch('webinspectapi.webinspect.WebInspectApi')
def test_get_cert_proxy_failure(api_mock, caplog):
    api_mock.return_value = ClassHelper(False)
    test_obj = WebinspectProxyClient('test-id', '80', 'test-server')
    test_obj.get_cert_proxy()

    caplog.check(
        ('__webbreaker__', 'ERROR', "Unable to retrieve cert.\n ERROR: Test api message "),
    )
    caplog.uninstall()


@mock.patch('webinspectapi.webinspect.WebInspectApi')
@mock.patch('webbreaker.webinspectproxyclient.open', new_callable=mock_open, read_data="data")
def test_get_cert_proxy_exception_unbound(open_mock, api_mock, caplog):
    api_mock.return_value = ClassHelper(True)

    e = UnboundLocalError("Test Error")
    open_mock.side_effect = e

    test_obj = WebinspectProxyClient('test-id', '80', 'test-server')
    test_obj.get_cert_proxy()

    caplog.check(
        ('__webbreaker__', 'ERROR', "Error saving cert locally Test Error"),
    )
    caplog.uninstall()

    assert open_mock.call_count == 1


@mock.patch('webinspectapi.webinspect.WebInspectApi')
def test_start_proxy_success(api_mock):
    api_mock.return_value = ClassHelper(True)

    test_obj = WebinspectProxyClient('test-id', '80', 'test-server')
    result = test_obj.start_proxy()

    assert api_mock.call_count == 1
    assert result == 'Test data'


@mock.patch('webinspectapi.webinspect.WebInspectApi')
def test_start_proxy_failure(api_mock, caplog):
    api_mock.return_value = ClassHelper(False)

    test_obj = WebinspectProxyClient('test-id', '80', 'test-server')
    test_obj.start_proxy()

    caplog.check(
        ('__webbreaker__', 'CRITICAL', "Test api message"),
    )
    caplog.uninstall()

    assert api_mock.call_count == 1


@mock.patch('webinspectapi.webinspect.WebInspectApi')
def test_delete_proxy_success(api_mock, caplog):
    api_mock.return_value = ClassHelper(True)

    test_obj = WebinspectProxyClient('test-id', '80', 'test-server')
    result = test_obj.delete_proxy()

    caplog.check(
        ('__webbreaker__', 'INFO', "Proxy: 'test-id' deleted from 'test-server'"),
    )
    caplog.uninstall()

    assert api_mock.call_count == 1


@mock.patch('webinspectapi.webinspect.WebInspectApi')
def test_delete_proxy_failure(api_mock, caplog):
    api_mock.return_value = ClassHelper(False)

    test_obj = WebinspectProxyClient('test-id', '80', 'test-server')
    test_obj.delete_proxy()

    caplog.check(
        ('__webbreaker__', 'CRITICAL', "Test api message"),
    )
    caplog.uninstall()

    assert api_mock.call_count == 1


@mock.patch('webinspectapi.webinspect.WebInspectApi')
def test_list_proxy_success(api_mock):
    api_mock.return_value = ClassHelper(True)

    test_obj = WebinspectProxyClient('test-id', '80', 'test-server')
    result = test_obj.list_proxy()

    assert api_mock.call_count == 1
    assert result == 'Test data'


@mock.patch('webinspectapi.webinspect.WebInspectApi')
def test_list_proxy_failure(api_mock, caplog):
    api_mock.return_value = ClassHelper(False)

    test_obj = WebinspectProxyClient('test-id', '80', 'test-server')
    test_obj.list_proxy()

    caplog.check(
        ('__webbreaker__', 'CRITICAL', "Test api message"),
    )
    caplog.uninstall()

    assert api_mock.call_count == 1


@mock.patch('webinspectapi.webinspect.WebInspectApi')
@mock.patch('webbreaker.webinspectproxyclient.open', new_callable=mock_open, read_data="data")
def test_download_proxy_webmacro_success(open_mock, api_mock, caplog):
    api_mock.return_value = ClassHelper(True)

    test_obj = WebinspectProxyClient('test-id', '80', 'test-server')
    test_obj.download_proxy(True, False)

    caplog.check(
        ('__webbreaker__', 'INFO', "Scan results file is available: test-id-proxy.webmacro"),
    )
    caplog.uninstall()

    assert api_mock.call_count == 1
    assert open_mock.call_count == 1


@mock.patch('webinspectapi.webinspect.WebInspectApi')
@mock.patch('webbreaker.webinspectproxyclient.open', new_callable=mock_open, read_data="data")
def test_download_proxy_setting_success(open_mock, api_mock, caplog):
    api_mock.return_value = ClassHelper(True)

    test_obj = WebinspectProxyClient('test-id', '80', 'test-server')
    test_obj.download_proxy(False, True)

    caplog.check(
        ('__webbreaker__', 'INFO', "Scan results file is available: test-id-proxy.xml"),
    )
    caplog.uninstall()

    assert api_mock.call_count == 1
    assert open_mock.call_count == 1


@mock.patch('webinspectapi.webinspect.WebInspectApi')
@mock.patch('webbreaker.webinspectproxyclient.open', new_callable=mock_open, read_data="data")
def test_download_proxy_no_file_type(open_mock, api_mock, caplog):
    api_mock.return_value = ClassHelper(True)

    test_obj = WebinspectProxyClient('test-id', '80', 'test-server')
    result = test_obj.download_proxy(False, False)

    caplog.check(
        ('__webbreaker__', 'ERROR', "Please enter a file type to download."),
    )
    caplog.uninstall()

    assert result == 1
    assert api_mock.call_count == 1
    assert open_mock.call_count == 0


@mock.patch('webinspectapi.webinspect.WebInspectApi')
@mock.patch('webbreaker.webinspectproxyclient.open', new_callable=mock_open, read_data="data")
def test_download_proxy_failure(open_mock, api_mock, caplog):
    api_mock.return_value = ClassHelper(False)

    test_obj = WebinspectProxyClient('test-id', '80', 'test-server')
    test_obj.download_proxy(True, False)

    caplog.check(
        ('__webbreaker__', 'ERROR', "Unable to retrieve file. Test api message "),
    )
    caplog.uninstall()

    assert api_mock.call_count == 1
    assert open_mock.call_count == 0


@mock.patch('webinspectapi.webinspect.WebInspectApi')
@mock.patch('webbreaker.webinspectproxyclient.open', new_callable=mock_open, read_data="data")
def test_download_proxy_unbound_exception(open_mock, api_mock, caplog):
    api_mock.return_value = ClassHelper(True)

    e = UnboundLocalError("Test Error")
    open_mock.side_effect = e

    test_obj = WebinspectProxyClient('test-id', '80', 'test-server')
    test_obj.download_proxy(True, False)

    caplog.check(
        ('__webbreaker__', 'ERROR', "Error saving file locally Test Error"),
    )
    caplog.uninstall()

    assert api_mock.call_count == 1
    assert open_mock.call_count == 1


@mock.patch('webinspectapi.webinspect.WebInspectApi')
def test_upload_proxy_setting_success(api_mock, caplog):
    api_mock.return_value = ClassHelper(True)

    test_obj = WebinspectProxyClient('test-id', '80', 'test-server')
    test_obj.upload_proxy('test-file')

    caplog.check(
        ('__webbreaker__', 'INFO', "Uploading to: 'test-id'"),
        ('__webbreaker__', 'INFO', "Uploaded 'test-file' to 'test-id' on: test-server."),
    )
    caplog.uninstall()

    assert api_mock.call_count == 1


@mock.patch('webinspectapi.webinspect.WebInspectApi')
def test_upload_proxy_failure(api_mock, caplog):
    api_mock.return_value = ClassHelper(False)

    test_obj = WebinspectProxyClient('test-id', '80', 'test-server')
    test_obj.upload_proxy('test-file')

    caplog.check(
        ('__webbreaker__', 'INFO', "Uploading to: 'test-id'"),
        ('__webbreaker__', 'ERROR', "Uploading test-file gave error: Test api message"),
    )
    caplog.uninstall()

    assert api_mock.call_count == 1


@mock.patch('webinspectapi.webinspect.WebInspectApi')
def test_upload_proxy_unbound_exception(api_mock, caplog):
    e = UnboundLocalError("Test Error")
    api_mock.side_effect = e

    test_obj = WebinspectProxyClient('test-id', '80', 'test-server')
    test_obj.upload_proxy('test-file')

    caplog.check(
        ('__webbreaker__', 'INFO', "Uploading to: 'test-id'"),
        ('__webbreaker__', 'ERROR', "Error uploading policy Test Error"),
    )
    caplog.uninstall()

    assert api_mock.call_count == 1


@mock.patch('webinspectapi.webinspect.WebInspectApi')
def test_upload_proxy_value_error_exception(api_mock, caplog):
    e = ValueError("Test Error")
    api_mock.side_effect = e

    test_obj = WebinspectProxyClient('test-id', '80', 'test-server')
    test_obj.upload_proxy('test-file')

    caplog.check(
        ('__webbreaker__', 'INFO', "Uploading to: 'test-id'"),
        ('__webbreaker__', 'ERROR', "Error uploading policy Test Error"),
    )
    caplog.uninstall()

    assert api_mock.call_count == 1


@mock.patch('webinspectapi.webinspect.WebInspectApi')
def test_get_proxy_success(api_mock):
    api_mock.return_value = ClassHelper(True)

    test_obj = WebinspectProxyClient('test-id', '80', 'test-server')
    result = test_obj.get_proxy()

    assert api_mock.call_count == 1
    assert result == 'Test data'


@mock.patch('webinspectapi.webinspect.WebInspectApi')
def test_get_proxy_failure(api_mock):
    api_mock.return_value = ClassHelper(False)

    test_obj = WebinspectProxyClient('test-id', '80', 'test-server')
    result = test_obj.get_proxy()

    assert api_mock.call_count == 1
    assert result is None
