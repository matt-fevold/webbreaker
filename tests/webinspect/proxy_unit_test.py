import mock
import pytest
import logging
import re
from testfixtures import LogCapture
from mock import mock_open

from webbreaker.webinspect.proxy import WebInspectProxy
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
        self.data = {'uri': '/webinspect/proxy/webinspect-K431H', 'port': 51158, 'address': '10.10.100.100',
                     'instanceId': 'webinspect-K431H'}

    def get_endpoint(self):
        return 'test-server'

    def cert_proxy(self):
        return WebInspectResponse(success=self.success, message=self.message, data=self.data)

    def start_proxy(self, id=None, port=None, address=None):
        return WebInspectResponse(success=self.success, message=self.message, data=self.data)

    def delete_proxy(self, instance_id=None):
        return WebInspectResponse(success=self.success, message=self.message, data=self.data)

    # note that return value for this is a list of dictionaries - not just a dictionary
    def list_proxies(self):
        return WebInspectResponse(success=self.success, message=self.message, data=[self.data])

    def get_proxy_information(self, instance_id=None):
        return WebInspectResponse(success=self.success, message=self.message, data=self.data)

    def download_proxy_webmacro(self, instance_id=None):
        return WebInspectResponse(success=self.success, message=self.message, data=self.data)

    def download_proxy_setting(self, instance_id=None):
        return WebInspectResponse(success=self.success, message=self.message, data=self.data)

    def upload_webmacro_proxy(self, id=None, macro_file_path=None):
        return WebInspectResponse(success=self.success, message=self.message, data=self.data)


@mock.patch('webbreaker.webinspect.proxy.WebInspectConfig')
@mock.patch('webbreaker.webinspect.proxy.WebInspectApi')
@mock.patch('webbreaker.webinspect.proxy.WebInspectAuth')
def test_config_init_variables(auth_mock, api_mock, config_mock):
    # Given
    auth_mock.return_value.authenticate.return_value = ('user', 'pass')
    api_mock.return_value = ClassHelper(True)
    config_mock.return_value.endpoints = ['webinspect_server1', 'webinspect_server2']

    # When
    test_proxy_object = WebInspectProxy(False, True, None, 'test', False, None, False, False, None, False, None, None)

    # Expect
    assert test_proxy_object.proxy_name == 'test'
    assert test_proxy_object.username == 'user'
    assert test_proxy_object.password == 'pass'


# proxy --start
@mock.patch('webbreaker.webinspect.proxy.WebInspectJitScheduler')
@mock.patch('webbreaker.webinspect.proxy.WebInspectProxy._start_proxy')
@mock.patch('webbreaker.webinspect.proxy.WebInspectProxy._get_proxy_certificate')
@mock.patch('webbreaker.webinspect.proxy.WebInspectConfig')
@mock.patch('webbreaker.webinspect.proxy.WebInspectAuth')
def test_proxy_start_success(auth_mock, config_mock, get_proxy_cert_mock, start_proxy_mock, jit_mock):

    # Given
    auth_mock.return_value.authenticate.return_value = ('user', 'pass')

    config_mock.return_value.endpoints = ['webinspect_server1']

    get_proxy_cert_mock.return_value = None
    start_proxy_mock.return_value = ClassHelper(True).data

    # When
    WebInspectProxy(False, False, None, None, False, None, True, False, None, False, None, None)

    # Expect
    assert get_proxy_cert_mock.call_count == 1
    assert start_proxy_mock.call_count == 1


# proxy --list
@mock.patch('webbreaker.webinspect.proxy.WebInspectProxy._list_proxy')
@mock.patch('webbreaker.webinspect.proxy.WebInspectConfig')
@mock.patch('webbreaker.webinspect.proxy.WebInspectAuth')
def test_proxy_list_success(auth_mock,  config_mock, list_proxy_mock):

    # Given
    auth_mock.return_value.authenticate.return_value = ('user', 'pass')
    config_mock.return_value.endpoints = ['webinspect_server1']

    # need to be a list
    list_proxy_mock.return_value = [ClassHelper(True).data]

    # When
    WebInspectProxy(False, True, None, None, False, None, False, False, None, False, None, None)

    # Expect
    assert list_proxy_mock.call_count == 1


# proxy --upload
@mock.patch('webbreaker.webinspect.proxy.WebInspectProxy._verify_proxy_server')
@mock.patch('webbreaker.webinspect.proxy.WebInspectApi')
@mock.patch('webbreaker.webinspect.proxy.WebInspectConfig')
@mock.patch('webbreaker.webinspect.proxy.WebInspectAuth')
def test_proxy_upload_success(auth_mock, config_mock, api_mock, verify_proxy_server_mock):

    # Given
    auth_mock.return_value.authenticate.return_value = ('user', 'pass')
    config_mock.return_value.endpoints = ['webinspect_server1']

    api_mock.return_value = ClassHelper(True)
    verify_proxy_server_mock.return_value = ClassHelper(True).data

    # When
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        WebInspectProxy(False, False, None, 'test_proxy_name', False, None, False, False, 'test_file', False, None, None)

    # Expect
    assert api_mock.call_count == 1
    assert verify_proxy_server_mock.call_count == 1


# proxy --stop
@mock.patch('webbreaker.webinspect.proxy.WebInspectProxy._delete_proxy')
@mock.patch('webbreaker.webinspect.proxy.WebInspectProxy._download_proxy')
@mock.patch('webbreaker.webinspect.proxy.WebInspectProxy._verify_proxy_server')
@mock.patch('webbreaker.webinspect.proxy.WebInspectConfig')
@mock.patch('webbreaker.webinspect.proxy.WebInspectAuth')
def test_proxy_stop_success(auth_mock, config_mock, verify_proxy_server_mock, download_proxy_mock, delete_proxy_mock):

    # Given
    auth_mock.return_value.authenticate.return_value = ('user', 'pass')
    config_mock.return_value.endpoints = ['webinspect_server1']

    verify_proxy_server_mock.return_value = ClassHelper(True).data
    download_proxy_mock.return_value = None
    delete_proxy_mock.return_value = None

    # When
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        WebInspectProxy(False, False, None, 'test_proxy_name', False, None, False, True, None, False, None, None)

    # Expect
    assert verify_proxy_server_mock.call_count == 1
    assert delete_proxy_mock.call_count == 1
    assert download_proxy_mock.call_count == 2


# proxy --download
@mock.patch('webbreaker.webinspect.proxy.WebInspectProxy._download_proxy')
@mock.patch('webbreaker.webinspect.proxy.WebInspectProxy._verify_proxy_server')
@mock.patch('webbreaker.webinspect.proxy.WebInspectConfig')
@mock.patch('webbreaker.webinspect.proxy.WebInspectAuth')
def test_proxy_download_success(auth_mock, config_mock, verify_proxy_server_mock, download_proxy_mock):

    # Given
    auth_mock.return_value.authenticate.return_value = ('user', 'pass')
    config_mock.return_value.endpoints = ['webinspect_server1']

    verify_proxy_server_mock.return_value = ClassHelper(True).data
    download_proxy_mock.return_value = None

    # When
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        WebInspectProxy(True, False, None, 'test_proxy_name', False, None, False, False, None, False, None, None)

    # Expect
    assert verify_proxy_server_mock.call_count == 1
    assert download_proxy_mock.call_count == 1