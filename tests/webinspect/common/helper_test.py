from webbreaker.webinspect.common.helper import WebInspectAPIHelper
import mock
from mock import  MagicMock
import pytest
from webbreaker.webinspect.scan import ScanOverrides
from tests.webinspect.scan_unit_test import _setup_overrides


@mock.patch('webbreaker.webinspect.common.helper.WebInspectApi')
@mock.patch('webbreaker.webinspect.common.helper.WebInspectLogHelper.log_info_using_webinspect_server')
def test_webinspect_api_helper_init_success(log_info_mock, api_mock):
    # Given
    expected_host = "test server"
    expected_username = None
    expected_password = None

    expected_silent_flag = False

    # When
    webinspect_api_helper_object = WebInspectAPIHelper(host=expected_host,
                                                       username=expected_username,
                                                       password=expected_password,
                                                       silent=expected_silent_flag)

    # Expect
    assert webinspect_api_helper_object.host == expected_host
    assert webinspect_api_helper_object.username == expected_username
    assert webinspect_api_helper_object.password == expected_password
    assert webinspect_api_helper_object.setting_overrides is None
    assert webinspect_api_helper_object.silent is False

    log_info_mock.assert_called_once_with(expected_host)
    assert log_info_mock.call_count == 1

    assert api_mock.call_count == 1


@mock.patch('webbreaker.webinspect.common.helper.WebInspectApi')
@mock.patch('webbreaker.webinspect.common.helper.WebInspectLogHelper.log_info_using_webinspect_server')
def test_webinspect_api_helper_init_with_setting_overrides_success(log_info_mock, api_mock):
    # Given
    expected_host = "test server"
    expected_username = None
    expected_password = None
    expected_silent_flag = False
    override_mock = MagicMock()
    override_mock.endpoint = "test server"

    # When
    webinspect_api_helper_object = WebInspectAPIHelper(host=None,
                                                       username=expected_username,
                                                       password=expected_password,
                                                       webinspect_setting_overrides=override_mock,
                                                       silent=expected_silent_flag)

    # Expect
    assert webinspect_api_helper_object.host == expected_host
    assert webinspect_api_helper_object.username == expected_username
    assert webinspect_api_helper_object.password == expected_password
#    assert override_mock.call_count == 1
    assert webinspect_api_helper_object.silent is False

    log_info_mock.assert_called_once_with(expected_host)
    assert log_info_mock.call_count == 1

    assert api_mock.call_count == 1


@mock.patch('webbreaker.webinspect.common.helper.json.dumps')
@mock.patch('webbreaker.webinspect.common.helper.WebInspectApi')
def test_webinspect_api_helper_create_scan_success(api_mock, json_dumps_mock):
    # Given
    override_mock = MagicMock()

    webinspect_api_helper_object = WebInspectAPIHelper(webinspect_setting_overrides=override_mock)
    webinspect_api_helper_object.api = api_mock


    # When
    webinspect_api_helper_object.create_scan()

    # Expect
    assert api_mock.call_count == 1
