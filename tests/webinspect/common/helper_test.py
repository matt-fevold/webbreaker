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


@mock.patch('webbreaker.webinspect.common.helper.WebInspectLogHelper.log_info_scan_start')
@mock.patch('webbreaker.webinspect.common.helper.json.dumps')
@mock.patch('webbreaker.webinspect.common.helper.WebInspectApi.create_scan')
def test_webinspect_api_helper_create_scan_success(api_mock, json_dumps_mock, log_scan_start_mock):
    # Given

    webinspect_api_helper_object = WebInspectAPIHelper(webinspect_setting_overrides=MagicMock())
    webinspect_api_helper_object.api.create_scan = api_mock



    # When
    webinspect_api_helper_object.create_scan()

    # Expect
    assert api_mock.call_count == 1
    assert log_scan_start_mock.call_count == 1


@mock.patch('webbreaker.webinspect.common.helper.WebInspectLogHelper.log_error_scan_start_failed')
@mock.patch('webbreaker.webinspect.common.helper.json.dumps')
@mock.patch('webbreaker.webinspect.common.helper.WebInspectApi.create_scan')
def test_webinspect_api_helper_create_scan_failure_value_error(api_mock, json_dumps_mock, log_scan_failed_mock):
    # Given
    webinspect_api_helper_object = WebInspectAPIHelper(webinspect_setting_overrides=MagicMock())
    json_dumps_mock.side_effect = ValueError
    webinspect_api_helper_object.api.create_scan = api_mock



    # When
    with pytest.raises(SystemExit):
        webinspect_api_helper_object.create_scan()

    # Expect
    assert api_mock.call_count == 0  # because it errors before the call
    assert log_scan_failed_mock.call_count == 1


@mock.patch('webbreaker.webinspect.common.helper.WebInspectLogHelper.log_error_scan_start_failed')
@mock.patch('webbreaker.webinspect.common.helper.json.dumps')
@mock.patch('webbreaker.webinspect.common.helper.WebInspectApi.create_scan')
def test_webinspect_api_helper_create_scan_failure_unbound_local_error(api_mock, json_dumps_mock, log_scan_failed_mock):
    # Given
    webinspect_api_helper_object = WebInspectAPIHelper(webinspect_setting_overrides=MagicMock())
    json_dumps_mock.side_effect = UnboundLocalError
    webinspect_api_helper_object.api.create_scan = api_mock



    # When
    with pytest.raises(SystemExit):
        webinspect_api_helper_object.create_scan()

    # Expect
    assert api_mock.call_count == 0  # because it errors before the call
    assert log_scan_failed_mock.call_count == 1


@mock.patch('webbreaker.webinspect.common.helper.open')
@mock.patch('webbreaker.webinspect.common.helper.WebInspectLogHelper.log_info_successful_scan_export')
@mock.patch('webbreaker.webinspect.common.helper.WebInspectApi.export_scan_format')
def test_webinspect_api_helper_export_scan_results_success(api_mock, log_export_success_mock, open_mock):
    # Given
    webinspect_api_helper_object = WebInspectAPIHelper(webinspect_setting_overrides=MagicMock())
    webinspect_api_helper_object.api.export_scan_format = api_mock

    # When
    webinspect_api_helper_object.export_scan_results('scan_id', '.xml')

    # Expect
    assert log_export_success_mock.call_count == 1
    assert api_mock.call_count == 1


@mock.patch('webbreaker.webinspect.common.helper.open')
@mock.patch('webbreaker.webinspect.common.helper.WebInspectLogHelper.log_error_failed_scan_export')
@mock.patch('webbreaker.webinspect.common.helper.WebInspectApi.export_scan_format')
def test_webinspect_api_helper_export_scan_results_failure_unbound_local_error(api_mock, log_export_failure_mock, open_mock):
    # Given
    webinspect_api_helper_object = WebInspectAPIHelper(webinspect_setting_overrides=MagicMock())
    webinspect_api_helper_object.api.export_scan_format = api_mock
    open_mock.side_effect = UnboundLocalError

    # When
    webinspect_api_helper_object.export_scan_results('scan_id', '.xml')

    # Expect
    assert log_export_failure_mock.call_count == 1
    assert api_mock.call_count == 1


@mock.patch('webbreaker.webinspect.common.helper.open')
@mock.patch('webbreaker.webinspect.common.helper.WebInspectLogHelper.log_error_failed_scan_export')
@mock.patch('webbreaker.webinspect.common.helper.WebInspectApi.export_scan_format')
def test_webinspect_api_helper_export_scan_results_io_error(api_mock, log_export_failure_mock, open_mock):
    # Given
    webinspect_api_helper_object = WebInspectAPIHelper(webinspect_setting_overrides=MagicMock())
    webinspect_api_helper_object.api.export_scan_format = api_mock
    open_mock.side_effect = IOError

    # When
    webinspect_api_helper_object.export_scan_results('scan_id', '.xml')

    # Expect
    assert log_export_failure_mock.call_count == 1
    assert api_mock.call_count == 1


@mock.patch('webbreaker.webinspect.common.helper.WebInspectApi.get_policy_by_guid')
def test_webinspect_api_helper_get_policy_by_guid_success(api_mock):
    # Given
    webinspect_api_helper_object = WebInspectAPIHelper(webinspect_setting_overrides=MagicMock())
    webinspect_api_helper_object.api.get_policy_by_guid = api_mock

    # When
    webinspect_api_helper_object.get_policy_by_guid("test_guid")

    # Expect
    assert api_mock.call_count == 1


@mock.patch('webbreaker.webinspect.common.helper.WebInspectApi.get_policy_by_name')
def test_webinspect_api_helper_get_policy_by_name_success(api_mock):
    # Given
    webinspect_api_helper_object = WebInspectAPIHelper(webinspect_setting_overrides=MagicMock())
    webinspect_api_helper_object.api.get_policy_by_name = api_mock

    # When
    webinspect_api_helper_object.get_policy_by_name("test_policy_name")

    # Expect
    assert api_mock.call_count == 1


@mock.patch('webbreaker.webinspect.common.helper.WebInspectApi.get_scan_by_name')
def test_webinspect_api_helper_get_scan_by_name_success(api_mock):
    # Given
    webinspect_api_helper_object = WebInspectAPIHelper(webinspect_setting_overrides=MagicMock())
    webinspect_api_helper_object.api.get_scan_by_name = api_mock

    # When
    webinspect_api_helper_object.get_scan_by_name("test_name")

    # Expect
    assert api_mock.call_count == 1


@mock.patch('webbreaker.webinspect.common.helper.json.loads')
@mock.patch('webbreaker.webinspect.common.helper.WebInspectApi.get_current_status')
def test_webinspect_api_helper_get_scan_status_success(api_mock, json_loads_mock):
    # Given
    webinspect_api_helper_object = WebInspectAPIHelper(webinspect_setting_overrides=MagicMock())
    webinspect_api_helper_object.api.get_current_status = api_mock
    json_loads_mock.side_effect = None

    # When
    webinspect_api_helper_object.get_scan_status("test_guid")

    # Expect
    assert api_mock.call_count == 1


@mock.patch('webbreaker.webinspect.common.helper.WebInspectLogHelper.log_error_get_scan_status')
@mock.patch('webbreaker.webinspect.common.helper.json.loads')
@mock.patch('webbreaker.webinspect.common.helper.WebInspectApi.get_current_status')
def test_webinspect_api_helper_get_scan_status_failure_value_error(api_mock, json_loads_mock, log_error_mock):
    # Given
    webinspect_api_helper_object = WebInspectAPIHelper(webinspect_setting_overrides=MagicMock())
    webinspect_api_helper_object.api.get_current_status = api_mock
    json_loads_mock.side_effect = ValueError

    # When
    webinspect_api_helper_object.get_scan_status("test_guid")

    # Expect
    assert log_error_mock.call_count == 1
    assert api_mock.call_count == 1


