import mock
import pytest

from webbreaker.threadfix.upload import ThreadFixUpload
from threadfixproapi.threadfixpro import ThreadFixProResponse

@mock.patch('webbreaker.threadfix.upload.ThreadFixHelper')
@mock.patch('webbreaker.threadfix.upload.threadfixloghelper')
def test_threadfix_upload_scan_successful_app_id(log_mock, helper_mock):
    app_id = '100'
    app_name = 'new app'
    scan_file = 'WEBINSPECT_test_2011-11-11.fpr'
    mockedResponseData = 'Scan upload process started.'

    helper_mock.return_value.api.upload_scan.return_value = ThreadFixProResponse(message='test', success=True, data=mockedResponseData)

    tfu = ThreadFixUpload(app_id, app_name, scan_file)
    assert helper_mock.call_count == 1
    tfu.helper.api.upload_scan.assert_called_once_with(app_id, scan_file)
    log_mock.log_info_upload_response.assert_called_once_with(mockedResponseData)

@mock.patch('webbreaker.threadfix.upload.ThreadFixHelper')
def test_threadfix_upload_scan_failed_app_id(helper_mock):
    app_id = '100'
    app_name = 'new app'
    scan_file = 'WEBINSPECT_test_2011-11-11.fpr'
    mockedResponseData = 'Scan upload process failed.'

    helper_mock.return_value.api.upload_scan.return_value = ThreadFixProResponse(message='test', success=False, data=mockedResponseData)

    with pytest.raises(SystemExit):
        ThreadFixUpload(app_id, app_name, scan_file)
    assert helper_mock.call_count == 1

@mock.patch('webbreaker.threadfix.upload.ThreadFixHelper')
@mock.patch('webbreaker.threadfix.upload.threadfixloghelper')
def test_threadfix_upload_scan_successful_no_app_id(log_mock, helper_mock):
    app_id = '100'
    app_name = 'new app'
    scan_file = 'WEBINSPECT_test_2011-11-11.fpr'
    mockedResponseData = 'Scan upload process started.'

    helper_mock.return_value.list_all_apps.return_value = [{'app_name': app_name, 'app_id': app_id, 'team_name': 'some team'}]
    helper_mock.return_value.api.upload_scan.return_value = ThreadFixProResponse(message='test', success=True, data=mockedResponseData)

    tfu = ThreadFixUpload(None, app_name, scan_file)
    assert helper_mock.call_count == 1
    assert tfu.helper.list_all_apps.call_count == 1
    assert log_mock.log_error_threadfix_retrieve_fail.call_count == 0
    log_mock.log_info_upload_response.assert_called_once_with(mockedResponseData)

@mock.patch('webbreaker.threadfix.upload.ThreadFixHelper')
@mock.patch('webbreaker.threadfix.upload.threadfixloghelper')
def test_threadfix_upload_scan_failed_no_app_id_no_match(log_mock, helper_mock):
    app_name = 'new app'
    scan_file = 'WEBINSPECT_test_2011-11-11.fpr'

    helper_mock.return_value.list_all_apps.return_value = [{'app_name': 'other app', 'app_id': '200', 'team_name': 'some team'}]

    tfu = ThreadFixUpload(None, app_name, scan_file)
    assert helper_mock.call_count == 1
    assert tfu.helper.list_all_apps.call_count == 1
    assert log_mock.log_error_threadfix_retrieve_fail.call_count == 0
    assert log_mock.log_info_upload_response.call_count == 0

@mock.patch('webbreaker.threadfix.upload.ThreadFixHelper')
@mock.patch('webbreaker.threadfix.upload.threadfixloghelper')
def test_threadfix_upload_scan_failed_no_app_id_multiple_matches(log_mock, helper_mock):
    app_name = 'new app'
    scan_file = 'WEBINSPECT_test_2011-11-11.fpr'

    helper_mock.return_value.list_all_apps.return_value = [{'app_name': app_name, 'app_id': '200', 'team_name': 'some team'},
                                                           {'app_name': app_name, 'app_id': '201', 'team_name': 'other team'}]

    tfu = ThreadFixUpload(None, app_name, scan_file)
    assert helper_mock.call_count == 1
    assert tfu.helper.list_all_apps.call_count == 1
    assert log_mock.log_error_threadfix_retrieve_fail.call_count == 0
    log_mock.log_error_multiple_application_found.assert_called_with(app_name)
    assert log_mock.log_info_upload_response.call_count == 0

@mock.patch('webbreaker.threadfix.upload.ThreadFixHelper')
@mock.patch('webbreaker.threadfix.upload.threadfixloghelper')
def test_threadfix_upload_scan_failed_no_app_id_empty_list(log_mock, helper_mock):
    app_name = 'new app'
    scan_file = 'WEBINSPECT_test_2011-11-11.fpr'

    helper_mock.return_value.list_all_apps.return_value = []

    tfu = ThreadFixUpload(None, app_name, scan_file)
    assert helper_mock.call_count == 1
    assert tfu.helper.list_all_apps.call_count == 1
    assert log_mock.log_error_threadfix_retrieve_fail.call_count == 1
    assert log_mock.log_info_upload_response.call_count == 0