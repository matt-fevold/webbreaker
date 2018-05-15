import mock
import pytest

from webbreaker.threadfix.scans import ThreadFixScans
from threadfixproapi.threadfixpro import ThreadFixProResponse

@mock.patch('webbreaker.threadfix.scans.ThreadFixHelper')
@mock.patch('webbreaker.threadfix.scans.loginfohelper')
@mock.patch('webbreaker.threadfix.scans.logexceptionhelper')
def test_threadfix_scans_successful_list(logex_mock, loginfo_mock, helper_mock):
    app_id = '123'
    expected_list_scans = ThreadFixProResponse(message='test', success=True, data=[{'id': app_id, 'scannerName': 'scanner name'}])
    helper_mock.return_value.api.list_scans.return_value = expected_list_scans
    helper_mock.return_value.api.get_scan_details.return_value = ThreadFixProResponse(message='test', success=True, data={'originalFileNames': ['filename.xml']})

    ThreadFixScans(app_id)
    assert helper_mock.call_count == 1
    assert loginfo_mock.LogInfoThreadfixScansListedSuccess.call_count == 1
    assert logex_mock.LogErrorNoScansFoundWithAppId.call_count == 0

@mock.patch('webbreaker.threadfix.scans.ThreadFixHelper')
@mock.patch('webbreaker.threadfix.scans.loginfohelper')
@mock.patch('webbreaker.threadfix.scans.logexceptionhelper')
def test_threadfix_scans_empty_list(logex_mock, loginfo_mock, helper_mock):
    app_id = '123'
    expected_list_scans = ThreadFixProResponse(message='no scans', success=True, data=[])
    helper_mock.return_value.api.list_scans.return_value = expected_list_scans

    ThreadFixScans(app_id)
    assert helper_mock.call_count == 1
    assert loginfo_mock.LogInfoThreadfixScansListedSuccess.call_count == 0
    assert logex_mock.LogErrorNoScansFoundWithAppId.call_count == 1

@mock.patch('webbreaker.threadfix.scans.ThreadFixHelper')
@mock.patch('webbreaker.threadfix.scans.loginfohelper')
def test_threadfix_scans_failed_response(loginfo_mock, helper_mock):
    app_id = '123'
    expected_list_scans = ThreadFixProResponse(message='error', success=False, data=[])
    helper_mock.return_value.api.list_scans.return_value = expected_list_scans

    with pytest.raises(SystemExit):
        ThreadFixScans(app_id)
    assert helper_mock.call_count == 1
    assert loginfo_mock.LogInfoThreadfixScansListedSuccess.call_count == 0