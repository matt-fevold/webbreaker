import mock
import pytest

from webbreaker.threadfix.upload import ThreadFixUpload
from threadfixproapi.threadfixpro import ThreadFixProResponse

@mock.patch('webbreaker.threadfix.upload.ThreadFixHelper')
@mock.patch('webbreaker.threadfix.upload.loginfohelper')
@mock.patch('webbreaker.threadfix.upload.logexceptionhelper')
def test_threadfix_upload_scan_successful_app_id(logex_mock, loginfo_mock, helper_mock):
    app_id = '100'
    app_name = 'new app'
    scan_file = 'WEBINSPECT_test_2011-11-11.fpr'
    mockedResponseData = 'Scan upload process started.'

    helper_mock.return_value.api.upload_scan.return_value = ThreadFixProResponse(message='test', success=True, data=mockedResponseData)

    tfu = ThreadFixUpload(app_id, app_name, scan_file)
    assert helper_mock.call_count == 1
    tfu.helper.api.upload_scan.assert_called_once_with(app_id, scan_file)
    loginfo_mock.LogInfoUploadResp.assert_called_once_with(mockedResponseData)

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
@mock.patch('webbreaker.threadfix.upload.loginfohelper')
@mock.patch('webbreaker.threadfix.upload.logexceptionhelper')
def test_threadfix_upload_scan_successful_no_app_id(logex_mock, loginfo_mock, helper_mock):
    app_id = '100'
    app_name = 'new app'
    scan_file = 'WEBINSPECT_test_2011-11-11.fpr'
    mockedResponseData = 'Scan upload process started.'

    helper_mock.return_value.list_all_apps.return_value = [{'app_name': app_name, 'app_id': app_id, 'team_name': 'some team'}]
    helper_mock.return_value.api.upload_scan.return_value = ThreadFixProResponse(message='test', success=True, data=mockedResponseData)

    tfu = ThreadFixUpload(None, app_name, scan_file)
    assert helper_mock.call_count == 1
    assert tfu.helper.list_all_apps.call_count == 1
    assert logex_mock.LogErrorThreadfixRetrieveFail.call_count == 0
    loginfo_mock.LogInfoUploadResp.assert_called_once_with(mockedResponseData)

@mock.patch('webbreaker.threadfix.upload.ThreadFixHelper')
@mock.patch('webbreaker.threadfix.upload.loginfohelper')
@mock.patch('webbreaker.threadfix.upload.logexceptionhelper')
def test_threadfix_upload_scan_failed_no_app_id_no_match(logex_mock, loginfo_mock, helper_mock):
    app_name = 'new app'
    scan_file = 'WEBINSPECT_test_2011-11-11.fpr'

    helper_mock.return_value.list_all_apps.return_value = [{'app_name': 'other app', 'app_id': '200', 'team_name': 'some team'}]

    tfu = ThreadFixUpload(None, app_name, scan_file)
    assert helper_mock.call_count == 1
    assert tfu.helper.list_all_apps.call_count == 1
    assert logex_mock.LogErrorThreadfixRetrieveFail.call_count == 0
    logex_mock.LogErrorNoApplicationWithMatchingName.assert_called_with(app_name)
    assert loginfo_mock.LogInfoUploadResp.call_count == 0

@mock.patch('webbreaker.threadfix.upload.ThreadFixHelper')
@mock.patch('webbreaker.threadfix.upload.loginfohelper')
@mock.patch('webbreaker.threadfix.upload.logexceptionhelper')
def test_threadfix_upload_scan_failed_no_app_id_multiple_matches(logex_mock, loginfo_mock, helper_mock):
    app_name = 'new app'
    scan_file = 'WEBINSPECT_test_2011-11-11.fpr'

    helper_mock.return_value.list_all_apps.return_value = [{'app_name': app_name, 'app_id': '200', 'team_name': 'some team'},
                                                           {'app_name': app_name, 'app_id': '201', 'team_name': 'other team'}]

    tfu = ThreadFixUpload(None, app_name, scan_file)
    assert helper_mock.call_count == 1
    assert tfu.helper.list_all_apps.call_count == 1
    assert logex_mock.LogErrorThreadfixRetrieveFail.call_count == 0
    logex_mock.LogErrorMultipleApplicationFound.assert_called_with(app_name)
    assert loginfo_mock.LogInfoUploadResp.call_count == 0

@mock.patch('webbreaker.threadfix.upload.ThreadFixHelper')
@mock.patch('webbreaker.threadfix.upload.loginfohelper')
@mock.patch('webbreaker.threadfix.upload.logexceptionhelper')
def test_threadfix_upload_scan_failed_no_app_id_empty_list(logex_mock, loginfo_mock, helper_mock):
    app_name = 'new app'
    scan_file = 'WEBINSPECT_test_2011-11-11.fpr'

    helper_mock.return_value.list_all_apps.return_value = []

    tfu = ThreadFixUpload(None, app_name, scan_file)
    assert helper_mock.call_count == 1
    assert tfu.helper.list_all_apps.call_count == 1
    assert logex_mock.LogErrorThreadfixRetrieveFail.call_count == 1
    assert loginfo_mock.LogInfoUploadResp.call_count == 0