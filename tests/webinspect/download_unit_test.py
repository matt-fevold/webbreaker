import mock
import pytest
from webbreaker.webinspect.download import WebInspectDownload


@mock.patch('webbreaker.webinspect.download.WebInspectDownload.download')
def test_download_init_success(download_mock):
    # Given

    # When
    WebInspectDownload(server=None,
                       scan_name=None,
                       scan_id=None,
                       extension=None,
                       username=None,
                       password=None)

    # Expect
    assert download_mock.call_count == 1

# @mock.patch('webbreaker.webinspect.download')


#@mock.patch('webbreaker.webinspect.download.')
@mock.patch('webbreaker.webinspect.download.WebInspectAPIHelper.export_scan_results')
@mock.patch('webbreaker.webinspect.download.WebInspectAPIHelper.get_scan_by_name')
@mock.patch('webbreaker.webinspect.download.WebInspectAuth')
def test_download_one_scan_found_success(auth_mock, get_scan_mock, export_scan_mock):
    # Given
    auth_mock.return_value.authenticate.return_value = ("expected_username", "expected_password")
    get_scan_mock.return_value = [{"ID": "some_id"}]  # the response is a list of dictionaries.

    # When

    # will call download
    WebInspectDownload(server=None,
                       scan_name=None,
                       scan_id=None,
                       extension=None,
                       username=None,
                       password=None)

    # Expect
    assert export_scan_mock.call_count == 1


@mock.patch('webbreaker.webinspect.download.WebInspectLogHelper.log_info_multiple_scans_found')
@mock.patch('webbreaker.webinspect.download.WebInspectAPIHelper.get_scan_by_name')
@mock.patch('webbreaker.webinspect.download.WebInspectAuth')
def test_download_multiple_scan_found_success(auth_mock, get_scan_mock, log_mock):
    # Given
    auth_mock.return_value.authenticate.return_value = ("expected_username", "expected_password")
    get_scan_mock.return_value = [{"ID": "some_id", "Name": "ScanName", "Status": "ScanStatus"},
                                  {"ID": "some_id", "Name": "ScanName", "Status": "ScanStatus"}]  # the response is a list of dictionaries.

    # When

    # will call download
    WebInspectDownload(server=None,
                       scan_name=None,
                       scan_id=None,
                       extension=None,
                       username=None,
                       password=None)

    # Expect
    assert log_mock.call_count == 1


@mock.patch('webbreaker.webinspect.download.WebInspectLogHelper.log_error_no_scans_found')
@mock.patch('webbreaker.webinspect.download.WebInspectAPIHelper.get_scan_by_name')
@mock.patch('webbreaker.webinspect.download.WebInspectAuth')
def test_download_no_scans_failure(auth_mock, get_scan_mock, log_mock):
    # Given
    auth_mock.return_value.authenticate.return_value = ("expected_username", "expected_password")
    get_scan_mock.return_value = []

    # When

    # will call download
    WebInspectDownload(server=None,
                       scan_name=None,
                       scan_id=None,
                       extension=None,
                       username=None,
                       password=None)

    # Expect
    assert log_mock.call_count == 1


@mock.patch('webbreaker.webinspect.download.WebInspectLogHelper.log_error_webinspect_download')
@mock.patch('webbreaker.webinspect.download.WebInspectAPIHelper.get_scan_by_name')
@mock.patch('webbreaker.webinspect.download.WebInspectAuth')
def test_download_failure_unbound_local_error(auth_mock, get_scan_mock, log_mock):
    # Given
    auth_mock.return_value.authenticate.return_value = ("expected_username", "expected_password")
    get_scan_mock.side_effect = UnboundLocalError

    # When

    # will call download

    WebInspectDownload(server=None,
                       scan_name=None,
                       scan_id=None,
                       extension=None,
                       username=None,
                       password=None)

    # Expect
    assert log_mock.call_count == 1


@mock.patch('webbreaker.webinspect.download.WebInspectLogHelper.log_error_webinspect_download')
@mock.patch('webbreaker.webinspect.download.WebInspectAPIHelper.get_scan_by_name')
@mock.patch('webbreaker.webinspect.download.WebInspectAuth')
def test_download_failure_type_error(auth_mock, get_scan_mock, log_mock):
    # Given
    auth_mock.return_value.authenticate.return_value = ("expected_username", "expected_password")
    get_scan_mock.side_effect = UnboundLocalError

    # When

    # will call download

    WebInspectDownload(server=None,
                       scan_name=None,
                       scan_id=None,
                       extension=None,
                       username=None,
                       password=None)

    # Expect
    assert log_mock.call_count == 1


