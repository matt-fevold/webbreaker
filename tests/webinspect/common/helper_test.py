from webbreaker.webinspect.common.helper import WebInspectAPIHelper
import mock
from mock import  MagicMock
import pytest
from webinspectapi.webinspect import WebInspectResponse
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
    assert webinspect_api_helper_object.silent is expected_silent_flag

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
    assert webinspect_api_helper_object.silent is expected_silent_flag

    log_info_mock.assert_called_once_with(expected_host)
    assert log_info_mock.call_count == 1

    assert api_mock.call_count == 1


@mock.patch('webbreaker.webinspect.common.helper.WebInspectLogHelper.log_info_scan_start')
@mock.patch('webbreaker.webinspect.common.helper.json.dumps')
@mock.patch('webbreaker.webinspect.common.helper.WebInspectApi.create_scan')
def test_webinspect_api_helper_create_scan_success(api_mock, json_dumps_mock, log_scan_start_mock):
    # Given

    webinspect_api_helper_object = WebInspectAPIHelper(silent=True, webinspect_setting_overrides=MagicMock())
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
    webinspect_api_helper_object = WebInspectAPIHelper(silent=True, webinspect_setting_overrides=MagicMock())
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
    webinspect_api_helper_object = WebInspectAPIHelper(silent=True, webinspect_setting_overrides=MagicMock())
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
    webinspect_api_helper_object = WebInspectAPIHelper(silent=True, webinspect_setting_overrides=MagicMock())
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
    webinspect_api_helper_object = WebInspectAPIHelper(silent=True, webinspect_setting_overrides=MagicMock())
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
    webinspect_api_helper_object = WebInspectAPIHelper(silent=True, webinspect_setting_overrides=MagicMock())
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
    webinspect_api_helper_object = WebInspectAPIHelper(silent=True, webinspect_setting_overrides=MagicMock())
    webinspect_api_helper_object.api.get_policy_by_guid = api_mock

    # When
    webinspect_api_helper_object.get_policy_by_guid("test_guid")

    # Expect
    assert api_mock.call_count == 1


@mock.patch('webbreaker.webinspect.common.helper.WebInspectApi.get_policy_by_name')
def test_webinspect_api_helper_get_policy_by_name_success(api_mock):
    # Given
    webinspect_api_helper_object = WebInspectAPIHelper(silent=True, webinspect_setting_overrides=MagicMock())
    webinspect_api_helper_object.api.get_policy_by_name = api_mock

    # When
    webinspect_api_helper_object.get_policy_by_name("test_policy_name")

    # Expect
    assert api_mock.call_count == 1


@mock.patch('webbreaker.webinspect.common.helper.WebInspectApi.get_scan_by_name')
def test_webinspect_api_helper_get_scan_by_name_success(api_mock):
    # Given
    webinspect_api_helper_object = WebInspectAPIHelper(silent=True, webinspect_setting_overrides=MagicMock())
    webinspect_api_helper_object.api.get_scan_by_name = api_mock

    # When
    webinspect_api_helper_object.get_scan_by_name("test_name")

    # Expect
    assert api_mock.call_count == 1


@mock.patch('webbreaker.webinspect.common.helper.json.loads')
@mock.patch('webbreaker.webinspect.common.helper.WebInspectApi.get_current_status')
def test_webinspect_api_helper_get_scan_status_success(api_mock, json_loads_mock):
    # Given
    webinspect_api_helper_object = WebInspectAPIHelper(silent=True, webinspect_setting_overrides=MagicMock())
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
    webinspect_api_helper_object = WebInspectAPIHelper(silent=True, webinspect_setting_overrides=MagicMock())
    webinspect_api_helper_object.api.get_current_status = api_mock
    json_loads_mock.side_effect = ValueError

    # When
    webinspect_api_helper_object.get_scan_status("test_guid")

    # Expect
    assert log_error_mock.call_count == 1
    assert api_mock.call_count == 1


@mock.patch('webbreaker.webinspect.common.helper.WebInspectLogHelper.log_error_get_scan_status')
@mock.patch('webbreaker.webinspect.common.helper.json.loads')
@mock.patch('webbreaker.webinspect.common.helper.WebInspectApi.get_current_status')
def test_webinspect_api_helper_get_scan_status_failure_type_error(api_mock, json_loads_mock, log_error_mock):
    # Given
    webinspect_api_helper_object = WebInspectAPIHelper(silent=True, webinspect_setting_overrides=MagicMock())
    webinspect_api_helper_object.api.get_current_status = api_mock
    json_loads_mock.side_effect = TypeError

    # When
    webinspect_api_helper_object.get_scan_status("test_guid")

    # Expect
    assert log_error_mock.call_count == 1
    assert api_mock.call_count == 1


@mock.patch('webbreaker.webinspect.common.helper.WebInspectLogHelper.log_error_get_scan_status')
@mock.patch('webbreaker.webinspect.common.helper.json.loads')
@mock.patch('webbreaker.webinspect.common.helper.WebInspectApi.get_current_status')
def test_webinspect_api_helper_get_scan_status_failure_unbound_local_error(api_mock, json_loads_mock, log_error_mock):
    # Given
    webinspect_api_helper_object = WebInspectAPIHelper(silent=True, webinspect_setting_overrides=MagicMock())
    webinspect_api_helper_object.api.get_current_status = api_mock
    json_loads_mock.side_effect = UnboundLocalError

    # When
    webinspect_api_helper_object.get_scan_status("test_guid")

    # Expect
    assert log_error_mock.call_count == 1
    assert api_mock.call_count == 1


@mock.patch('webbreaker.webinspect.common.helper.WebInspectApi.list_scans')
def test_webinspect_api_helper_list_scans_success(api_mock):
    # Given
    webinspect_api_helper_object = WebInspectAPIHelper(silent=True, webinspect_setting_overrides=MagicMock())
    webinspect_api_helper_object.api.list_scans = api_mock


    # When
    webinspect_api_helper_object.list_scans()

    # Expect
    assert api_mock.call_count == 1


@mock.patch('webbreaker.webinspect.common.helper.WebInspectLogHelper.log_error_list_scans')
@mock.patch('webbreaker.webinspect.common.helper.WebInspectApi.list_scans')
def test_webinspect_api_helper_list_scans_failure_value_error(api_mock, log_error_mock):
    # Given
    webinspect_api_helper_object = WebInspectAPIHelper(silent=True, webinspect_setting_overrides=MagicMock())
    webinspect_api_helper_object.api.list_scans = api_mock
    api_mock.side_effect = ValueError

    # When
    webinspect_api_helper_object.list_scans()

    # Expect
    assert log_error_mock.call_count == 1
    assert api_mock.call_count == 1


@mock.patch('webbreaker.webinspect.common.helper.WebInspectLogHelper.log_error_list_scans')
@mock.patch('webbreaker.webinspect.common.helper.WebInspectApi.list_scans')
def test_webinspect_api_helper_list_scans_failure_unbound_local_error(api_mock, log_error_mock):
    # Given
    webinspect_api_helper_object = WebInspectAPIHelper(silent=True, webinspect_setting_overrides=MagicMock())
    webinspect_api_helper_object.api.list_scans = api_mock
    api_mock.side_effect = UnboundLocalError

    # When
    webinspect_api_helper_object.list_scans()

    # Expect
    assert log_error_mock.call_count == 1
    assert api_mock.call_count == 1


@mock.patch('webbreaker.webinspect.common.helper.WebInspectLogHelper.log_error_list_scans')
@mock.patch('webbreaker.webinspect.common.helper.WebInspectApi.list_scans')
def test_webinspect_api_helper_list_scans_failure_name_error(api_mock, log_error_mock):
    # Given
    webinspect_api_helper_object = WebInspectAPIHelper(silent=True, webinspect_setting_overrides=MagicMock())
    webinspect_api_helper_object.api.list_scans = api_mock
    api_mock.side_effect = NameError

    # When
    webinspect_api_helper_object.list_scans()

    # Expect
    assert log_error_mock.call_count == 1
    assert api_mock.call_count == 1


@mock.patch('webbreaker.webinspect.common.helper.WebInspectApi.list_running_scans')
def test_webinspect_api_helper_list_running_scans_success(api_mock):
    # Given
    webinspect_api_helper_object = WebInspectAPIHelper(silent=True, webinspect_setting_overrides=MagicMock())
    webinspect_api_helper_object.api.list_running_scans = api_mock

    # When
    webinspect_api_helper_object.list_running_scans()

    # Expect
    assert api_mock.call_count == 1


@mock.patch('webbreaker.webinspect.common.helper.WebInspectApi.get_policy_by_guid')
def test_webinspect_api_helper_policy_exists_success(api_mock):
    # Given
    webinspect_api_helper_object = WebInspectAPIHelper(silent=True, webinspect_setting_overrides=MagicMock())
    webinspect_api_helper_object.api.get_policy_by_guid = api_mock
    policy_guid = "test_guid"

    # When
    webinspect_api_helper_object.policy_exists(policy_guid)

    # Expect
    assert api_mock.call_count == 1


@mock.patch('webbreaker.webinspect.common.helper.WebInspectApi.stop_scan')
def test_webinspect_api_helper_stop_scan_success(api_mock):
    # Given
    webinspect_api_helper_object = WebInspectAPIHelper(silent=True, webinspect_setting_overrides=MagicMock())
    webinspect_api_helper_object.api.stop_scan = api_mock
    scan_guid = "test_guid"

    # When
    webinspect_api_helper_object.stop_scan(scan_guid)

    # Expect
    assert api_mock.call_count == 1


@mock.patch('webbreaker.webinspect.common.helper.ntpath.basename')
@mock.patch('webbreaker.webinspect.common.helper.WebInspectApi.get_policy_by_name')
@mock.patch('webbreaker.webinspect.common.helper.WebInspectApi.delete_policy')
@mock.patch('webbreaker.webinspect.common.helper.WebInspectApi.upload_policy')
def test_webinspect_api_upload_policy_no_existing_policy_success(upload_policy_mock,  delete_policy_mock, get_policy_mock, ntpath_mock):
    # Given
    # There is no existing policy by this name so no deletion
    webinspect_api_helper_object = WebInspectAPIHelper(silent=True, webinspect_setting_overrides=MagicMock())

    # When
    webinspect_api_helper_object.upload_policy()

    # Expect
    assert get_policy_mock.call_count == 1
    assert delete_policy_mock.call_count == 0
    assert upload_policy_mock.call_count == 1


@mock.patch('webbreaker.webinspect.common.helper.ntpath.basename')
@mock.patch('webbreaker.webinspect.common.helper.WebInspectApi.get_policy_by_name')
@mock.patch('webbreaker.webinspect.common.helper.WebInspectApi.delete_policy')
@mock.patch('webbreaker.webinspect.common.helper.WebInspectApi.upload_policy')
def test_webinspect_api_upload_policy_delete_existing_policy_success(upload_policy_mock,  delete_policy_mock, get_policy_mock, ntpath_mock):
    # Given
    # There is existing policy by this name so deletion
    webinspect_api_helper_object = WebInspectAPIHelper(silent=True, webinspect_setting_overrides=MagicMock())
    expected_response = WebInspectResponse(response_code=200, success=True, data={'test_data': 'test_data',
                                                                                  'uniqueId': "12345"})  # there is an existing policy on the server
    get_policy_mock.return_value = expected_response

    # When
    webinspect_api_helper_object.upload_policy()

    # Expect
    assert get_policy_mock.call_count == 1
    assert delete_policy_mock.call_count == 1
    assert upload_policy_mock.call_count == 1


@mock.patch('webbreaker.webinspect.common.helper.WebInspectLogHelper.log_error_policy_deletion')
@mock.patch('webbreaker.webinspect.common.helper.ntpath.basename')
@mock.patch('webbreaker.webinspect.common.helper.WebInspectApi.get_policy_by_name')
@mock.patch('webbreaker.webinspect.common.helper.WebInspectApi.delete_policy')
@mock.patch('webbreaker.webinspect.common.helper.WebInspectApi.upload_policy')
def test_webinspect_api_upload_policy_failure_value_error(upload_policy_mock,  delete_policy_mock, get_policy_mock, ntpath_mock, log_error_mock):
    # not 100% sure where these tests fail, but want to make sure we catch it properly

    # Given
    webinspect_api_helper_object = WebInspectAPIHelper(silent=True, webinspect_setting_overrides=MagicMock())
    get_policy_mock.side_effect = ValueError


    # When
    webinspect_api_helper_object.upload_policy()

    # Expect
    assert log_error_mock.call_count == 1
    assert get_policy_mock.call_count == 1
    assert delete_policy_mock.call_count == 0
    assert upload_policy_mock.call_count == 1


@mock.patch('webbreaker.webinspect.common.helper.WebInspectLogHelper.log_error_policy_deletion')
@mock.patch('webbreaker.webinspect.common.helper.ntpath.basename')
@mock.patch('webbreaker.webinspect.common.helper.WebInspectApi.get_policy_by_name')
@mock.patch('webbreaker.webinspect.common.helper.WebInspectApi.delete_policy')
@mock.patch('webbreaker.webinspect.common.helper.WebInspectApi.upload_policy')
def test_webinspect_api_upload_policy_failure_unbound_local_error(upload_policy_mock,  delete_policy_mock, get_policy_mock, ntpath_mock, log_error_mock):
    # not 100% sure where these tests fail, but want to make sure we catch it properly

    # Given
    webinspect_api_helper_object = WebInspectAPIHelper(silent=True, webinspect_setting_overrides=MagicMock())
    get_policy_mock.side_effect = UnboundLocalError


    # When
    webinspect_api_helper_object.upload_policy()

    # Expect
    assert log_error_mock.call_count == 1
    assert get_policy_mock.call_count == 1
    assert delete_policy_mock.call_count == 0
    assert upload_policy_mock.call_count == 1


@mock.patch('webbreaker.webinspect.common.helper.WebInspectLogHelper.log_error_policy_deletion')
@mock.patch('webbreaker.webinspect.common.helper.ntpath.basename')
@mock.patch('webbreaker.webinspect.common.helper.WebInspectApi.get_policy_by_name')
@mock.patch('webbreaker.webinspect.common.helper.WebInspectApi.delete_policy')
@mock.patch('webbreaker.webinspect.common.helper.WebInspectApi.upload_policy')
def test_webinspect_api_upload_policy_failure_type_error(upload_policy_mock,  delete_policy_mock, get_policy_mock, ntpath_mock, log_error_mock):
    # not 100% sure where these tests fail, but want to make sure we catch it properly

    # Given
    webinspect_api_helper_object = WebInspectAPIHelper(silent=True, webinspect_setting_overrides=MagicMock())
    get_policy_mock.side_effect = TypeError


    # When
    webinspect_api_helper_object.upload_policy()

    # Expect
    assert log_error_mock.call_count == 1
    assert get_policy_mock.call_count == 1
    assert delete_policy_mock.call_count == 0
    assert upload_policy_mock.call_count == 1


@mock.patch('webbreaker.webinspect.common.helper.WebInspectLogHelper.log_error_policy_deletion')
@mock.patch('webbreaker.webinspect.common.helper.ntpath.basename')
@mock.patch('webbreaker.webinspect.common.helper.WebInspectApi.get_policy_by_name')
@mock.patch('webbreaker.webinspect.common.helper.WebInspectApi.delete_policy')
@mock.patch('webbreaker.webinspect.common.helper.WebInspectApi.upload_policy')
def test_webinspect_api_upload_policy_failure_uncaught_error(upload_policy_mock,  delete_policy_mock, get_policy_mock, ntpath_mock, log_error_mock):
    # I'm not confident this is a great test - but if something unexpected exception happens we want to at least test how it's handled.. . ?

    # Given
    webinspect_api_helper_object = WebInspectAPIHelper(silent=True, webinspect_setting_overrides=MagicMock())
    get_policy_mock.side_effect = IOError  # a random error that isn't handled


    # When
    with pytest.raises(Exception):
        webinspect_api_helper_object.upload_policy()

    # Expect
    assert log_error_mock.call_count == 0  # we break before this
    assert get_policy_mock.call_count == 1
    assert delete_policy_mock.call_count == 0
    assert upload_policy_mock.call_count == 0  # we break before this


@mock.patch('webbreaker.webinspect.common.helper.WebInspectApi.upload_settings')
def test_webinspect_api_helper_upload_settings_success(api_mock):
    # Given
    webinspect_api_helper_object = WebInspectAPIHelper(silent=True, webinspect_setting_overrides=MagicMock())
    webinspect_api_helper_object.api.upload_settings = api_mock

    # When
    webinspect_api_helper_object.upload_settings()

    # Expect
    assert api_mock.call_count == 1


@mock.patch('webbreaker.webinspect.common.helper.WebInspectLogHelper.log_no_webinspect_server_found')
@mock.patch('webbreaker.webinspect.common.helper.WebInspectLogHelper.log_error_uploading')
@mock.patch('webbreaker.webinspect.common.helper.WebInspectApi.upload_settings')
def test_webinspect_api_helper_upload_settings_failed_value_error(api_mock, log_error_mock, log_no_server_mock):
    # Given
    webinspect_api_helper_object = WebInspectAPIHelper(silent=True, webinspect_setting_overrides=MagicMock())
    api_mock.side_effect = ValueError
    webinspect_api_helper_object.api.upload_settings = api_mock
    

    # When
    webinspect_api_helper_object.upload_settings()

    # Expect
    assert  log_no_server_mock.call_count == 1
    assert log_error_mock.call_count == 1
    assert api_mock.call_count == 1


@mock.patch('webbreaker.webinspect.common.helper.WebInspectLogHelper.log_no_webinspect_server_found')
@mock.patch('webbreaker.webinspect.common.helper.WebInspectLogHelper.log_error_uploading')
@mock.patch('webbreaker.webinspect.common.helper.WebInspectApi.upload_settings')
def test_webinspect_api_helper_upload_settings_failed_unbound_local_error(api_mock, log_error_mock, log_no_server_mock):
    # Given
    webinspect_api_helper_object = WebInspectAPIHelper(silent=True, webinspect_setting_overrides=MagicMock())
    api_mock.side_effect = UnboundLocalError
    webinspect_api_helper_object.api.upload_settings = api_mock

    # When
    webinspect_api_helper_object.upload_settings()

    # Expect
    assert log_no_server_mock.call_count == 1
    assert log_error_mock.call_count == 1
    assert api_mock.call_count == 1


@mock.patch('webbreaker.webinspect.common.helper.WebInspectLogHelper.log_no_webinspect_server_found')
@mock.patch('webbreaker.webinspect.common.helper.WebInspectLogHelper.log_error_uploading')
@mock.patch('webbreaker.webinspect.common.helper.WebInspectApi.upload_settings')
def test_webinspect_api_helper_upload_settings_failed_name_error(api_mock, log_error_mock, log_no_server_mock):
    # Given
    webinspect_api_helper_object = WebInspectAPIHelper(silent=True, webinspect_setting_overrides=MagicMock())
    api_mock.side_effect = NameError
    webinspect_api_helper_object.api.upload_settings = api_mock

    # When
    webinspect_api_helper_object.upload_settings()

    # Expect
    assert log_no_server_mock.call_count == 1
    assert log_error_mock.call_count == 1
    assert api_mock.call_count == 1

####


@mock.patch('webbreaker.webinspect.common.helper.WebInspectApi.upload_webmacro')
def test_webinspect_api_helper_upload_webmacro_success(api_mock):
    # Given
    webinspect_api_helper_object = WebInspectAPIHelper(silent=True, webinspect_setting_overrides=mock)
    webinspect_api_helper_object.setting_overrides.webinspect_upload_webmacros = ['test_list']
    webinspect_api_helper_object.setting_overrides.endpoint = "test_host"

    webinspect_api_helper_object.api.upload_webmacro = api_mock

    # When
    webinspect_api_helper_object.upload_webmacros()

    # Expect
    assert api_mock.call_count == 1


@mock.patch('webbreaker.webinspect.common.helper.WebInspectLogHelper.log_no_webinspect_server_found')
@mock.patch('webbreaker.webinspect.common.helper.WebInspectLogHelper.log_error_uploading')
@mock.patch('webbreaker.webinspect.common.helper.WebInspectApi.upload_webmacro')
def test_webinspect_api_helper_upload_webmacro_failed_value_error(api_mock, log_error_mock, log_no_server_mock):
    # Given
    webinspect_api_helper_object = WebInspectAPIHelper(silent=True, webinspect_setting_overrides=MagicMock())
    webinspect_api_helper_object.setting_overrides.webinspect_upload_webmacros = ['test_list']
    api_mock.side_effect = ValueError
    webinspect_api_helper_object.api.upload_webmacro = api_mock

    # When
    webinspect_api_helper_object.upload_webmacros()

    # Expect
    assert log_no_server_mock.call_count == 1
    assert log_error_mock.call_count == 1
    assert api_mock.call_count == 1


@mock.patch('webbreaker.webinspect.common.helper.WebInspectLogHelper.log_no_webinspect_server_found')
@mock.patch('webbreaker.webinspect.common.helper.WebInspectLogHelper.log_error_uploading')
@mock.patch('webbreaker.webinspect.common.helper.WebInspectApi.upload_webmacro')
def test_webinspect_api_helper_upload_settings_failed_unbound_local_error(api_mock, log_error_mock, log_no_server_mock):
    # Given
    webinspect_api_helper_object = WebInspectAPIHelper(silent=True, webinspect_setting_overrides=MagicMock())
    webinspect_api_helper_object.setting_overrides.webinspect_upload_webmacros = ['test_list']
    api_mock.side_effect = UnboundLocalError
    webinspect_api_helper_object.api.upload_webmacro = api_mock

    # When
    webinspect_api_helper_object.upload_webmacros()

    # Expect
    assert log_no_server_mock.call_count == 1
    assert log_error_mock.call_count == 1
    assert api_mock.call_count == 1


@mock.patch('webbreaker.webinspect.common.helper.WebInspectAPIHelper._check_if_built_in')
@mock.patch('webbreaker.webinspect.common.helper.WebInspectAPIHelper._get_index')
@mock.patch('webbreaker.webinspect.common.helper.WebInspectApi.get_policy_by_guid')
def test_webinspect_api_verify_scan_policy(get_policy_by_guid_mock, get_index_mock, check_if_built_in_mock):
    # Given
    # webinspect_api_helper_object = WebInspectAPIHelper(silent=True, webinspect_setting_overrides=MagicMock())
    # webinspect_api_helper_object.setting_overrides.scan_policy = "test_policy"
    # get_policy_by_guid_mock.return_value = WebInspectResponse(success=True)
    # webinspect_api_helper_object.api.get_policy_by_guid = get_policy_by_guid_mock
    #
    # check_if_built_in_mock.return_value = True
    #
    # test_config = MagicMock()
    #
    # # When
    # webinspect_api_helper_object.verify_scan_policy(test_config)
    #
    # # Expect
    # assert check_if_built_in_mock.call_count == 1
    # assert get_index_mock.call_count == 1
    # assert get_policy_by_guid_mock.call_count == 1
    # TODO: this test was taking too long to write.     
    assert 0

