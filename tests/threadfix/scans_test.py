import mock
import pytest

from webbreaker.threadfix.scans import ThreadFixScans
from threadfixproapi.threadfixpro import ThreadFixProResponse

@mock.patch('webbreaker.threadfix.scans.ThreadFixHelper')
@mock.patch('webbreaker.threadfix.scans.threadfixloghelper')
def test_threadfix_scans_successful_list(log_mock, helper_mock):
    app_id = '123'
    expected_list_scans = ThreadFixProResponse(message='test', success=True, data=[{'id': app_id, 'scannerName': 'scanner name'}])
    helper_mock.return_value.api.list_scans.return_value = expected_list_scans
    helper_mock.return_value.api.get_scan_details.return_value = ThreadFixProResponse(message='test', success=True, data={'originalFileNames': ['filename.xml']})

    ThreadFixScans(app_id)
    assert helper_mock.call_count == 1
    assert log_mock.log_info_threadfix_scans_listed_success.call_count == 1
    assert log_mock.log_error_no_scans_found_with_app_id.call_count == 0

@mock.patch('webbreaker.threadfix.scans.ThreadFixHelper')
@mock.patch('webbreaker.threadfix.scans.threadfixloghelper')
def test_threadfix_scans_empty_list(log_mock, helper_mock):
    app_id = '123'
    expected_list_scans = ThreadFixProResponse(message='no scans', success=True, data=[])
    helper_mock.return_value.api.list_scans.return_value = expected_list_scans

    ThreadFixScans(app_id)
    assert helper_mock.call_count == 1
    assert log_mock.log_info_threadfix_scans_listed_success.call_count == 0
    assert log_mock.log_error_no_scans_found_with_app_id.call_count == 1

@mock.patch('webbreaker.threadfix.scans.ThreadFixHelper')
@mock.patch('webbreaker.threadfix.scans.threadfixloghelper')
def test_threadfix_scans_failed_response(log_mock, helper_mock):
    app_id = '123'
    expected_list_scans = ThreadFixProResponse(message='error', success=False, data=[])
    helper_mock.return_value.api.list_scans.return_value = expected_list_scans

    with pytest.raises(SystemExit):
        ThreadFixScans(app_id)
    assert helper_mock.call_count == 1
    assert log_mock.log_info_threadfix_scans_listed_success.call_count == 0