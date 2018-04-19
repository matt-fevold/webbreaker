import mock
import pytest
import logging
import re
from testfixtures import LogCapture
from mock import mock_open

from webbreaker.webinspect.scan import WebInspectScan
from webbreaker.webinspect.common.helper import WebInspectAPIHelper


@mock.patch('webbreaker.webinspect.scan.WebInspectAPIHelper.create_scan')
@mock.patch('webbreaker.webinspect.scan.WebInspectAPIHelper')
# config mock is here so it doesn't read from the config file.
@mock.patch('webbreaker.webinspect.scan.WebInspectConfig')
@mock.patch('webbreaker.webinspect.scan.WebInspectAuth')
def test_scan_success(auth_mock, config_mock, api_mock, create_scan_api_mock):
    # have the auth return a username/pw without reading any config
    auth_mock.return_value.authenticate.return_value = ('user', 'pass')

    api_mock.return_value.get_scan_status.return_value = 'complete'

    #
    api_mock.return_value.wait_for_scan_status_change = create_scan_api_mock

    overrides = {
        'username': None,
        'password': None,
        'allowed_hosts': (),
        'start_urls': (),
        'workflow_macros': ()
    }

    WebInspectScan(overrides)

    assert create_scan_api_mock.call_count == 1
