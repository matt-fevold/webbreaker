
from webbreaker.common.confighelper import Config
import pytest
from mock import MagicMock
from webbreaker.webinspect.scan import ScanOverrides, WebInspectScan
from webbreaker.common.webbreakerhelper import WebBreakerHelper
from webbreaker.webinspect.common.loghelper import WebInspectLogHelper
from subprocess import CalledProcessError
import os
import mock
import requests
from git.exc import GitCommandError

try:  # python 3
    from queue import Queue, Empty
except ImportError:  # python 2
    from Queue import Queue as queue


def _setup_overrides(expected_username=None, expected_password=None, expected_allowed_hosts=(), expected_start_urls=(),
                     expected_timeout=0, expected_settings='Default', expected_upload_settings=None,
                     expected_upload_macro=None, expected_upload_webmacro=None, expected_login_macro=None,
                     expected_upload_policy=None, expected_scan_policy=None, expected_scan_name=None,
                     expected_scan_mode=None, expected_fortify_user=None, expected_size='large',
                     expected_scan_scope=None, expected_scan_start=None, expected_workflow_macro=(),
                     expected_git='/path/to/git'):
    """
    An easy way to setup the overrides for each test using the click default values, change them when needed.
    A little extra verbose here for increased test readability.
    :return:
    """
    overrides = {
        'username': expected_username,
        'password': expected_password,
        'allowed_hosts': expected_allowed_hosts,
        'start_urls': expected_start_urls,
        'workflow_macros': expected_workflow_macro,
        'timeout': expected_timeout,
        'settings': expected_settings,
        'upload_settings': expected_upload_settings,
        'upload_macro': expected_upload_macro,
        'upload_webmacros': expected_upload_webmacro,
        'login_macro': expected_login_macro,
        'upload_policy': expected_upload_policy,
        'scan_policy': expected_scan_policy,
        'scan_name': expected_scan_name,
        'scan_mode': expected_scan_mode,
        'fortify_user': expected_fortify_user,
        'size': expected_size,
        'scan_scope': expected_scan_scope,
        'scan_start': expected_scan_start,
        'git': expected_git
    }

    return overrides


@mock.patch('webbreaker.webinspect.scan.Config')
@mock.patch('webbreaker.webinspect.scan.WebInspectConfig')
@mock.patch('webbreaker.webinspect.scan.ScanOverrides')
@mock.patch('webbreaker.webinspect.scan.WebInspectScan.scan')
def test_WebinspectScan_init_success(scan_mock, scan_override_mock, wi_config_mock, config_git_mock):
    # Given
    overrides = {}  # empty dictionary

    # When
    scan_object = WebInspectScan(overrides)

    # Expect
    assert config_git_mock.call_count == 1
    assert wi_config_mock.call_count == 1
    assert scan_mock.call_count == 1


# These decorators can be a bit ugly at time - they help handle all the ugliness of teardown and setup so it's
# a net win, but can be a bit abstract at times.

@mock.patch('webbreaker.webinspect.scan.WebInspectAPIHelper.create_scan')
@mock.patch('webbreaker.webinspect.scan.WebInspectScan._scan')
@mock.patch('webbreaker.webinspect.scan.WebInspectScan._upload_settings_and_policies')
@mock.patch('webbreaker.webinspect.scan.WebInspectScan._webinspect_git_clone')
@mock.patch('webbreaker.webinspect.scan.WebInspectAuth')
@mock.patch('webbreaker.webinspect.scan.WebInspectConfig')
@mock.patch('webbreaker.webinspect.scan.ScanOverrides')
def test_WebInspectScan_scan_success(scan_override_mock, wi_config_mock, auth_mock, git_clone_mock,
                                     upload_settings_policies_mock, _scan_mock, api_create_scan_mock):
    # Given
    overrides = _setup_overrides()
    auth_mock.return_value.authenticate.return_value = ("expected_username", "expected_password")


    # When
    scan = WebInspectScan(overrides)

    # Expect
    assert api_create_scan_mock.call_count == 1
    assert _scan_mock.call_count == 1
    assert upload_settings_policies_mock.call_count == 1
    assert git_clone_mock.call_count == 1


@mock.patch('webbreaker.webinspect.scan.WebInspectLogHelper.log_error_scan_start_failed')
@mock.patch('webbreaker.webinspect.scan.WebInspectAPIHelper.create_scan')
@mock.patch('webbreaker.webinspect.scan.WebInspectScan._scan')
@mock.patch('webbreaker.webinspect.scan.WebInspectScan._upload_settings_and_policies')
@mock.patch('webbreaker.webinspect.scan.WebInspectScan._webinspect_git_clone')
@mock.patch('webbreaker.webinspect.scan.WebInspectAuth')
@mock.patch('webbreaker.webinspect.scan.WebInspectConfig')
@mock.patch('webbreaker.webinspect.scan.ScanOverrides')
def test_WebInspectScan_scan_failure_connection_error(scan_override_mock, wi_config_mock, auth_mock, git_clone_mock,
                                                      upload_settings_policies_mock, _scan_mock, api_create_scan_mock,
                                                      log_error_mock):
    # Given
    overrides = _setup_overrides()
    auth_mock.return_value.authenticate.return_value = ("expected_username", "expected_password")
    _scan_mock.side_effect = requests.ConnectionError

    # When
    with pytest.raises(SystemExit):
        scan = WebInspectScan(overrides)

    # Expect
    assert log_error_mock.call_count == 1


@mock.patch('webbreaker.webinspect.scan.WebInspectLogHelper.log_error_scan_start_failed')
@mock.patch('webbreaker.webinspect.scan.WebInspectAPIHelper.create_scan')
@mock.patch('webbreaker.webinspect.scan.WebInspectScan._scan')
@mock.patch('webbreaker.webinspect.scan.WebInspectScan._upload_settings_and_policies')
@mock.patch('webbreaker.webinspect.scan.WebInspectScan._webinspect_git_clone')
@mock.patch('webbreaker.webinspect.scan.WebInspectAuth')
@mock.patch('webbreaker.webinspect.scan.WebInspectConfig')
@mock.patch('webbreaker.webinspect.scan.ScanOverrides')
def test_WebInspectScan_scan_failure_http_error(scan_override_mock, wi_config_mock, auth_mock, git_clone_mock,
                                                      upload_settings_policies_mock, _scan_mock, api_create_scan_mock,
                                                      log_error_mock):
    # Given
    overrides = _setup_overrides()
    auth_mock.return_value.authenticate.return_value = ("expected_username", "expected_password")
    _scan_mock.side_effect = requests.HTTPError

    # When
    with pytest.raises(SystemExit):
        scan = WebInspectScan(overrides)

    # Expect
    assert log_error_mock.call_count == 1


@mock.patch('webbreaker.webinspect.scan.WebInspectAPIHelper.upload_policy')
@mock.patch('webbreaker.webinspect.scan.WebInspectAPIHelper.upload_webmacros')
@mock.patch('webbreaker.webinspect.scan.WebInspectAPIHelper.upload_settings')
@mock.patch('webbreaker.webinspect.scan.WebInspectAPIHelper.verify_scan_policy')
@mock.patch('webbreaker.webinspect.scan.Config')
@mock.patch('webbreaker.webinspect.scan.WebInspectConfig')
@mock.patch('webbreaker.webinspect.scan.ScanOverrides')
@mock.patch('webbreaker.webinspect.scan.WebInspectScan.scan')
def test_WebInspectScan_upload_settings_and_policies_success(scan_mock, scan_override_mock, wi_config_mock,
                                                             config_git_mock, verify_scan_mock, upload_settings_mock,
                                                             upload_webmacros_mock, upload_policy_mock):
    # Given
    overrides = _setup_overrides(expected_upload_settings="settings.xml", expected_upload_webmacro="upload.macro",
                                 expected_upload_policy="test policy?")

    scan_object = WebInspectScan(overrides)
    # below was done to logically isolate this test - which was harder to do than I thought.
    #   since self.webinspect_api isn't declared in the init and we have mocked the function that creates
    #   it, we have to set the api.
    scan_object._set_api(None, None)
    scan_object.webinspect_api.setting_overrides.webinspect_upload_policy = True
    scan_object.webinspect_api.setting_overrides.scan_policy = None
    # When
    scan_object._upload_settings_and_policies()

    # Expect
    assert verify_scan_mock.call_count == 1
    assert upload_settings_mock.call_count == 1
    assert upload_webmacros_mock.call_count == 1
    assert upload_policy_mock.call_count == 1


@mock.patch('webbreaker.webinspect.scan.WebInspectAPIHelper.stop_scan')
@mock.patch('webbreaker.webinspect.scan.Config')
@mock.patch('webbreaker.webinspect.scan.WebInspectConfig')
@mock.patch('webbreaker.webinspect.scan.ScanOverrides')
@mock.patch('webbreaker.webinspect.scan.WebInspectScan.scan')
def test_WebInspectScan_stop_scan_success(scan_mock, scan_override_mock, wi_config_mock, config_git_mock,
                                                       stop_scan_mock):
    # Given
    overrides = _setup_overrides()

    scan_object = WebInspectScan(overrides)
    scan_object._set_api(None, None)

    # When
    scan_object._stop_scan("scan_guid")

    # Expect
    assert stop_scan_mock.call_count == 1


@mock.patch('webbreaker.webinspect.scan.WebInspectAPIHelper.export_scan_results')
@mock.patch('webbreaker.webinspect.scan.WebInspectAPIHelper.get_scan_status')
@mock.patch('webbreaker.webinspect.scan.Config')
@mock.patch('webbreaker.webinspect.scan.WebInspectConfig')
@mock.patch('webbreaker.webinspect.scan.ScanOverrides')
@mock.patch('webbreaker.webinspect.scan.WebInspectScan.scan')
def test_WebInspectScan_scan_complete_success(scan_mock, scan_override_mock, wi_config_mock, config_git_mock,
                                              get_status_mock, export_mock):
    # Given
    overrides = _setup_overrides()
    scan_object = WebInspectScan(overrides)
    scan_object._set_api(None, None)
    scan_object.scan_id = "test_guid"
    get_status_mock.return_value = 'complete'

    # When
    scan_object._scan()

    # Expect
    assert export_mock.call_count == 2


@mock.patch('webbreaker.webinspect.scan.WebInspectAPIHelper.stop_scan')
@mock.patch('webbreaker.webinspect.scan.WebInspectAPIHelper.get_scan_status')
@mock.patch('webbreaker.webinspect.scan.Config')
@mock.patch('webbreaker.webinspect.scan.WebInspectConfig')
@mock.patch('webbreaker.webinspect.scan.ScanOverrides')
@mock.patch('webbreaker.webinspect.scan.WebInspectScan.scan')
def test_WebInspectScan_scan_not_running_failure(scan_mock, scan_override_mock, wi_config_mock, config_git_mock,
                                              get_status_mock, stop_scan_mock):
    # Given
    overrides = _setup_overrides()
    scan_object = WebInspectScan(overrides)
    scan_object._set_api(None, None)
    scan_object.scan_id = "test_guid"
    get_status_mock.return_value = 'notrunning'

    # When
    with pytest.raises(SystemExit):
        scan_object._scan()

    # Expect
    assert stop_scan_mock.call_count == 1


@mock.patch('webbreaker.webinspect.scan.WebInspectAPIHelper.stop_scan')
@mock.patch('webbreaker.webinspect.scan.Config')
@mock.patch('webbreaker.webinspect.scan.WebInspectConfig')
@mock.patch('webbreaker.webinspect.scan.ScanOverrides')
@mock.patch('webbreaker.webinspect.scan.WebInspectScan.scan')
def test_WebInspectScan_exit_gracefully_success(scan_mock, scan_override_mock, wi_config_mock, config_git_mock,
                                                       stop_scan_mock):
    # Given
    overrides = _setup_overrides()

    scan_object = WebInspectScan(overrides)
    scan_object._set_api(None, None)
    scan_object.scan_id = "scan_guid"  # this gets set when a scan is created - we're not creating a scan here.

    # When
    with pytest.raises(SystemExit):
        scan_object._exit_scan_gracefully("scan_guid")

    # Expect
    assert stop_scan_mock.call_count == 1


@mock.patch('webbreaker.webinspect.scan.WebInspectLogHelper.log_info_default_settings')
@mock.patch('webbreaker.webinspect.scan.os')
@mock.patch('webbreaker.webinspect.scan.Config')
@mock.patch('webbreaker.webinspect.scan.WebInspectConfig')
@mock.patch('webbreaker.webinspect.scan.ScanOverrides')
@mock.patch('webbreaker.webinspect.scan.WebInspectScan.scan')
def test_WebInspectScan_webinspect_git_clone_default_success(scan_mock, scan_overrides_mock, wi_config_mock, config_mock,
                                                     os_mock, log_mock):
    # Given
    overrides = _setup_overrides()
    scan_object = WebInspectScan(overrides)
    # Kinda weird, have to set it like this since we mock scan overrides.
    scan_object.scan_overrides.settings = 'Default'

    # When
    scan_object._webinspect_git_clone()

    # Expect
    assert log_mock.call_count == 1
    assert config_mock.call_count == 1


@mock.patch('webbreaker.webinspect.scan.check_output')
@mock.patch('webbreaker.webinspect.scan.WebInspectLogHelper.log_info_updating_webinspect_configurations')
@mock.patch('webbreaker.webinspect.scan.os')
@mock.patch('webbreaker.webinspect.scan.Config')
@mock.patch('webbreaker.webinspect.scan.WebInspectConfig')
@mock.patch('webbreaker.webinspect.scan.ScanOverrides')
@mock.patch('webbreaker.webinspect.scan.WebInspectScan.scan')
def test_WebInspectScan_webinspect_git_clone_not_default_with_valid_git_dir_success(scan_mock, scan_overrides_mock, wi_config_mock, config_mock,
                                                     os_mock, log_mock, check_output_mock):
    # Given
    overrides = _setup_overrides()
    scan_object = WebInspectScan(overrides)
    # Kinda weird, have to set it like this since we mock scan overrides.
    scan_object.scan_overrides.settings = 'NotDefault'

    # When
    scan_object._webinspect_git_clone()

    # Expect
    assert log_mock.call_count == 1
    assert check_output_mock.call_count == 3


@mock.patch('webbreaker.webinspect.scan.check_output')
@mock.patch('webbreaker.webinspect.scan.WebInspectLogHelper.log_info_webinspect_git_clonning')
@mock.patch('webbreaker.webinspect.scan.os.path.exists')
@mock.patch('webbreaker.webinspect.scan.os')
@mock.patch('webbreaker.webinspect.scan.Config')
@mock.patch('webbreaker.webinspect.scan.WebInspectConfig')
@mock.patch('webbreaker.webinspect.scan.ScanOverrides')
@mock.patch('webbreaker.webinspect.scan.WebInspectScan.scan')
def test_WebInspectScan_webinspect_git_clone_not_default_with_invalid_git_dir_success(scan_mock, scan_overrides_mock, wi_config_mock, config_mock,
                                                      os_mock, os_path_exists_mock, log_mock, check_output_mock):
    # Given
    overrides = _setup_overrides()
    scan_object = WebInspectScan(overrides)
    os_path_exists_mock.return_value = False
    # Kinda weird, have to set it like this since we mock scan overrides.
    scan_object.scan_overrides.settings = 'NotDefault'

    # When
    scan_object._webinspect_git_clone()

    # Expect
    assert log_mock.call_count == 1
    assert check_output_mock.call_count == 1


@mock.patch('webbreaker.webinspect.scan.WebInspectLogHelper.log_error_git_cloning_error')
@mock.patch('webbreaker.webinspect.scan.os')
@mock.patch('webbreaker.webinspect.scan.Config')
@mock.patch('webbreaker.webinspect.scan.WebInspectConfig')
@mock.patch('webbreaker.webinspect.scan.ScanOverrides')
@mock.patch('webbreaker.webinspect.scan.WebInspectScan.scan')
def test_WebInspectScan_webinspect_git_clone_failure_type_error(scan_mock, scan_overrides_mock, wi_config_mock, config_mock,
                                                     os_mock, log_mock):
    # Given
    overrides = _setup_overrides()
    scan_object = WebInspectScan(overrides)
    config_mock.side_effect = TypeError

    # When
    scan_object._webinspect_git_clone()

    # Expect
    assert log_mock.call_count == 1


@mock.patch('webbreaker.webinspect.scan.WebInspectLogHelper.log_webinspect_config_issue')
@mock.patch('webbreaker.webinspect.scan.os.path.exists')
@mock.patch('webbreaker.webinspect.scan.os')
@mock.patch('webbreaker.webinspect.scan.Config')
@mock.patch('webbreaker.webinspect.scan.WebInspectConfig')
@mock.patch('webbreaker.webinspect.scan.ScanOverrides')
@mock.patch('webbreaker.webinspect.scan.WebInspectScan.scan')
def test_WebInspectScan_webinspect_git_clone_failure_attribute_error(scan_mock, scan_overrides_mock, wi_config_mock, config_mock,
                                                     os_mock, os_path_exists_mock, log_mock):
    # Given
    overrides = _setup_overrides()
    scan_object = WebInspectScan(overrides)
    os_path_exists_mock.side_effect = AttributeError


    # When
    with pytest.raises(AttributeError):
        scan_object._webinspect_git_clone()

    # Expect
    assert log_mock.call_count == 1


@mock.patch('webbreaker.webinspect.scan.WebBreakerHelper.check_run_env')
@mock.patch('webbreaker.webinspect.scan.ScanOverrides._parse_webinspect_overrides')
@mock.patch('webbreaker.webinspect.scan.ScanOverrides.get_endpoint')
def test_ScanOverrides_init_success(get_endpoint_mock, parse_webinspect_mock, run_env_mock):
    # Given
    # mock function calls within init so we can focus the test.
    get_endpoint_mock.return_value = "webinspect_url"
    run_env_mock.return_value = "expected_run_env"

    overrides = _setup_overrides()

    # When
    scan_override_object = ScanOverrides(overrides)

    # Expect
    assert scan_override_object.webinspect_dir == '/path/to/git'

    assert scan_override_object.username is None
    assert scan_override_object.password is None

    assert scan_override_object.settings is 'Default'
    assert scan_override_object.scan_name is None
    assert scan_override_object.webinspect_upload_settings is None
    assert scan_override_object.webinspect_upload_policy is None
    assert scan_override_object.webinspect_upload_webmacros is None
    assert scan_override_object.scan_mode is None
    assert scan_override_object.scan_scope is None
    assert scan_override_object.login_macro is None
    assert scan_override_object.scan_policy is None
    assert scan_override_object.scan_start is None
    assert scan_override_object.scan_size == 'large'
    assert scan_override_object.fortify_user is None

    assert scan_override_object.allowed_hosts == []  # is converted from a tuple
    assert scan_override_object.start_urls == []  # converted form tuple
    assert scan_override_object.workflow_macros == []  # converted from tuple

    assert scan_override_object.endpoint == "webinspect_url"
    assert scan_override_object.runenv == "expected_run_env"


@mock.patch('webbreaker.webinspect.scan.WebBreakerHelper.check_run_env')
@mock.patch('webbreaker.webinspect.scan.ScanOverrides._parse_webinspect_overrides')
@mock.patch('webbreaker.webinspect.scan.ScanOverrides.get_endpoint')
def test_ScanOverrides_init_failure_environment_error_exception(get_endpoint_mock, parse_webinspect_mock, run_env_mock):
    # I'm not 100% where this is raised, but I can't be certain nothing doesn't call it so going to be a bit hacky
    # and just call it somewhere to make sure it is properly handled with a sys.exit and a log call.

    # Given
    # mock function calls within init so we can focus the test

    WebInspectLogHelper.log_error_scan_overrides_parsing_error = MagicMock()
    run_env_mock.side_effect = EnvironmentError

    overrides = _setup_overrides()

    # When

    # if this doesn't raise SystemExit then it will fail.
    with pytest.raises(SystemExit):
        ScanOverrides(overrides)

    # Expect
    assert WebInspectLogHelper.log_error_scan_overrides_parsing_error.call_count == 1


@mock.patch('webbreaker.webinspect.scan.WebBreakerHelper.check_run_env')
@mock.patch('webbreaker.webinspect.scan.ScanOverrides._parse_webinspect_overrides')
@mock.patch('webbreaker.webinspect.scan.ScanOverrides.get_endpoint')
def test_ScanOverrides_init_failure_type_error_exception(get_endpoint_mock, parse_webinspect_mock, run_env_mock):
    # I'm not 100% where this is raised, but I can't be certain nothing doesn't call it so going to be a bit hacky
    # and just call it somewhere to make sure it is properly handled with a sys.exit and a log call.

    # Given

    # mock function calls within init so we can focus the test

    parse_webinspect_mock.side_effect = TypeError
    WebInspectLogHelper.log_error_scan_overrides_parsing_error = MagicMock()
    overrides = _setup_overrides()

    # When
    with pytest.raises(SystemExit):
        ScanOverrides(overrides)

    assert WebInspectLogHelper.log_error_scan_overrides_parsing_error.call_count == 1


@mock.patch('webbreaker.webinspect.scan.WebBreakerHelper.check_run_env')
@mock.patch('webbreaker.webinspect.scan.ScanOverrides._parse_webinspect_overrides')
@mock.patch('webbreaker.webinspect.scan.ScanOverrides.get_endpoint')
def test_ScanOverrides_get_formatted_overrides_success(get_endpoint_mock, parse_webinspect_mock, run_env_mock):
    # Given

    overrides = _setup_overrides()

    # When
    scan_overrides_object = ScanOverrides(overrides)
    formatted_overrides_dict = scan_overrides_object.get_formatted_overrides()

    # Expect
    assert formatted_overrides_dict['webinspect_settings'] == 'Default'
    assert formatted_overrides_dict['webinspect_scan_name'] is None
    assert formatted_overrides_dict['webinspect_upload_settings'] is None
    assert formatted_overrides_dict['webinspect_upload_policy'] is None
    assert formatted_overrides_dict['webinspect_upload_webmacros'] is None
    assert formatted_overrides_dict['webinspect_overrides_scan_mode'] is None
    assert formatted_overrides_dict['webinspect_overrides_scan_scope'] is None
    assert formatted_overrides_dict['webinspect_overrides_login_macro'] is None
    assert formatted_overrides_dict['webinspect_overrides_scan_policy'] is None
    assert formatted_overrides_dict['webinspect_overrides_scan_start'] is None
    assert formatted_overrides_dict['webinspect_overrides_start_urls'] == []
    assert formatted_overrides_dict['webinspect_scan_targets'] is None
    assert formatted_overrides_dict['webinspect_workflow_macros'] == []
    assert formatted_overrides_dict['webinspect_allowed_hosts'] == []
    assert formatted_overrides_dict['webinspect_scan_size'] == 'large'
    assert formatted_overrides_dict['fortify_user'] is None


# don't hate me, but tried to do this in a more readable way but there were unintended issues created with that.
@mock.patch('webbreaker.webinspect.scan.ScanOverrides.get_endpoint')
@mock.patch('webbreaker.webinspect.scan.WebBreakerHelper.check_run_env')
@mock.patch('webbreaker.webinspect.scan.ScanOverrides._trim_overrides')
@mock.patch('webbreaker.webinspect.scan.ScanOverrides._parse_scan_name_overrides')
@mock.patch('webbreaker.webinspect.scan.ScanOverrides._parse_upload_settings_overrides')
@mock.patch('webbreaker.webinspect.scan.ScanOverrides._parse_login_macro_overrides')
@mock.patch('webbreaker.webinspect.scan.ScanOverrides._parse_workflow_macros_overrides')
@mock.patch('webbreaker.webinspect.scan.ScanOverrides._parse_upload_webmacros_overrides')
@mock.patch('webbreaker.webinspect.scan.ScanOverrides._parse_upload_policy_overrides')
@mock.patch('webbreaker.webinspect.scan.ScanOverrides._parse_upload_settings_overrides_for_scan_target')
@mock.patch('webbreaker.webinspect.scan.ScanOverrides._parse_assigned_hosts_overrides')
def test_ScanOverrides_parse_webinspect_overrides_success(trim_mock, scan_name_mock, upload_settings_mock,
                                                          login_macro_mock, workflow_macro_mock, upload_webmacro_mock,
                                                          upload_policy_mock, upload_settings_scan_target_mock,
                                                          assigned_hosts_mock, get_endpoint_mock, check_run_env_mock):
    # Given

    # can't use setup_mocks sadly - can't mock parse_webinspect_options
    overrides = _setup_overrides()

    # When
    ScanOverrides(overrides)  # this will call _parse_webinspect_overrides

    # Expect
    assert trim_mock.call_count == 1
    assert scan_name_mock.call_count == 1
    assert upload_settings_mock.call_count == 1
    assert login_macro_mock.call_count == 1
    assert workflow_macro_mock.call_count == 1
    assert upload_webmacro_mock.call_count == 1
    assert upload_policy_mock.call_count == 1
    assert upload_settings_scan_target_mock.call_count == 1
    assert assigned_hosts_mock.call_count == 1


@mock.patch('webbreaker.webinspect.scan.WebBreakerHelper.check_run_env')
@mock.patch('webbreaker.webinspect.scan.ScanOverrides._parse_webinspect_overrides')
@mock.patch('webbreaker.webinspect.scan.ScanOverrides.get_endpoint')
def test_ScanOverrides_parse_scan_name_overrides_success(get_endpoint_mock, parse_webinspect_mock, run_env_mock):
    # Given
    overrides = _setup_overrides()
    WebInspectLogHelper.log_error_scan_overrides_parsing_error = MagicMock()

    # When
    scan_overrides_object = ScanOverrides(overrides)
    scan_overrides_object._parse_scan_name_overrides()

    # Expect
    assert scan_overrides_object.scan_name[0:11] in ['webinspect-']  # the randomly generated scan name


@mock.patch('webbreaker.webinspect.scan.WebBreakerHelper.check_run_env')
@mock.patch('webbreaker.webinspect.scan.ScanOverrides._parse_webinspect_overrides')
@mock.patch('webbreaker.webinspect.scan.ScanOverrides.get_endpoint')
def test_ScanOverrides_parse_scan_name_overrides_cli_passed_scan_name_success(get_endpoint_mock, parse_webinspect_mock, run_env_mock):
    # Given
    overrides = _setup_overrides(expected_scan_name="Expected_Scan_Name")

    # When
    scan_overrides_object = ScanOverrides(overrides)
    scan_overrides_object._parse_scan_name_overrides()

    # Expect
    assert scan_overrides_object.scan_name in ["Expected_Scan_Name"]


@mock.patch('webbreaker.webinspect.scan.os.getenv')
@mock.patch('webbreaker.webinspect.scan.WebBreakerHelper.check_run_env')
@mock.patch('webbreaker.webinspect.scan.ScanOverrides._parse_webinspect_overrides')
@mock.patch('webbreaker.webinspect.scan.ScanOverrides.get_endpoint')
def test_ScanOverrides_parse_scan_name_overrides_jenkins_job_BUILD_TAG_success(get_endpoint_mock, parse_webinspect_mock,
                                                                               run_env_mock, getenv_mock):
    # Given
    run_env_mock.return_value = "jenkins"
    # _parse_scan_name_overrides makes 2 calls to getevn, first one checks if there is a / in the return value and
    #   follows 2 different paths. We want to test both paths
    getenv_mock.side_effect = ["/JOB_NAME/", "EXPECTED_BUILD_TAG"]

    overrides = _setup_overrides()

    # When
    scan_overrides_object = ScanOverrides(overrides)
    scan_overrides_object._parse_scan_name_overrides()

    # Expect
    assert scan_overrides_object.scan_name in ['EXPECTED_BUILD_TAG']


@mock.patch('webbreaker.webinspect.scan.os.getenv')
@mock.patch('webbreaker.webinspect.scan.WebBreakerHelper.check_run_env')
@mock.patch('webbreaker.webinspect.scan.ScanOverrides._parse_webinspect_overrides')
@mock.patch('webbreaker.webinspect.scan.ScanOverrides.get_endpoint')
def test_ScanOverrides_parse_scan_name_overrides_jenkins_job_JOB_NAME_success(get_endpoint_mock, parse_webinspect_mock,
                                                                              run_env_mock, getenv_mock):
    # Given

    run_env_mock.return_value = "jenkins"
    # _parse_scan_name_overrides makes 2 calls to getevn, first one checks if there is a / in the return value and
    #   follows 2 different paths. We want to test both paths
    getenv_mock.side_effect = ["JOB_NAME", "EXPECTED_JOB_NAME"]

    overrides = _setup_overrides()

    # When
    scan_overrides_object = ScanOverrides(overrides)
    scan_overrides_object._parse_scan_name_overrides()

    # Expect
    assert scan_overrides_object.scan_name in ['EXPECTED_JOB_NAME']


@mock.patch('webbreaker.webinspect.scan.os.path.isfile')
@mock.patch('webbreaker.webinspect.scan.WebBreakerHelper.check_run_env')
@mock.patch('webbreaker.webinspect.scan.ScanOverrides._parse_webinspect_overrides')
@mock.patch('webbreaker.webinspect.scan.ScanOverrides.get_endpoint')
def test_ScanOverrides_parse_upload_settings_overrides_success(get_endpoint_mock, parse_webinspect_mock, run_env_mock,
                                                               isfile_mock):
    # Given
    isfile_mock.return_value = False

    overrides = _setup_overrides()
    scan_overrides_object = ScanOverrides(overrides)

    # When
    scan_overrides_object._parse_upload_settings_overrides()

    # Expect
    assert scan_overrides_object.webinspect_upload_settings is None


@mock.patch('webbreaker.webinspect.scan.os.path.isfile')
@mock.patch('webbreaker.webinspect.scan.WebBreakerHelper.check_run_env')
@mock.patch('webbreaker.webinspect.scan.ScanOverrides._parse_webinspect_overrides')
@mock.patch('webbreaker.webinspect.scan.ScanOverrides.get_endpoint')
def test_ScanOverrides_parse_upload_settings_overrides_cli_passed_settings_success(get_endpoint_mock,
                                                                                   parse_webinspect_mock,
                                                                                   run_env_mock, isfile_mock):
    # Given
    isfile_mock.return_value = False
    overrides = _setup_overrides(expected_settings="NotDefault")
    scan_overrides_object = ScanOverrides(overrides)

    # When
    scan_overrides_object._parse_upload_settings_overrides()

    # Expect
    assert scan_overrides_object.webinspect_upload_settings in '/path/to/git/settings/NotDefault.xml'


@mock.patch('webbreaker.webinspect.scan.os.path.isfile')
@mock.patch('webbreaker.webinspect.scan.WebBreakerHelper.check_run_env')
@mock.patch('webbreaker.webinspect.scan.ScanOverrides._parse_webinspect_overrides')
@mock.patch('webbreaker.webinspect.scan.ScanOverrides.get_endpoint')
def test_ScanOverrides_parse_upload_settings_overrides_cli_passed_settings_found_file_success(get_endpoint_mock,
                                                                                              parse_webinspect_mock,
                                                                                              run_env_mock,
                                                                                              isfile_mock):
    # Given
    # os.path.isfile is tricky have to mock it this way or there are odd side effects
    isfile_mock.side_effect = [False, True]
    overrides = _setup_overrides(expected_settings="/valid/path/NotDefault.xml")
    scan_overrides_object = ScanOverrides(overrides)

    # When
    scan_overrides_object._parse_upload_settings_overrides()

    # Expect
    assert scan_overrides_object.webinspect_upload_settings in "/valid/path/NotDefault.xml"
    assert scan_overrides_object.settings in "/valid/path/NotDefault"


@mock.patch('webbreaker.webinspect.scan.os.path.isfile')
@mock.patch('webbreaker.webinspect.scan.WebBreakerHelper.check_run_env')
@mock.patch('webbreaker.webinspect.scan.ScanOverrides._parse_webinspect_overrides')
@mock.patch('webbreaker.webinspect.scan.ScanOverrides.get_endpoint')
def test_ScanOverrides_parse_upload_settings_cli_passed_upload_settings_success(get_endpoint_mock,
                                                                                parse_webinspect_mock,
                                                                                run_env_mock, isfile_mock):
    # Given
    overrides = _setup_overrides(expected_upload_settings="/valid/path/NotDefault.xml")
    scan_overrides_object = ScanOverrides(overrides)
    # os.path.isfile is tricky have to mock it this way or there are odd side effects
    isfile_mock.side_effect = [False, True]

    # When
    scan_overrides_object._parse_upload_settings_overrides()

    # Expect
    assert scan_overrides_object.webinspect_upload_settings == "/valid/path/NotDefault.xml"


@mock.patch('webbreaker.webinspect.scan.WebBreakerHelper.check_run_env')
@mock.patch('webbreaker.webinspect.scan.ScanOverrides._parse_webinspect_overrides')
@mock.patch('webbreaker.webinspect.scan.ScanOverrides.get_endpoint')
def test_ScanOverrides_parse_login_macro_overrides_success(get_endpoint_mock, parse_webinspect_mock, run_env_mock):
    # Given
    overrides = _setup_overrides()

    # When
    scan_overrides_object = ScanOverrides(overrides)
    scan_overrides_object._parse_login_macro_overrides()

    # Expect
    assert scan_overrides_object.login_macro is None


@mock.patch('webbreaker.webinspect.scan.WebBreakerHelper.check_run_env')
@mock.patch('webbreaker.webinspect.scan.ScanOverrides._parse_webinspect_overrides')
@mock.patch('webbreaker.webinspect.scan.ScanOverrides.get_endpoint')
def test_ScanOverrides_parse_login_macro_overrides_cli_passed_loging_macro_success(get_endpoint_mock,
                                                                                   parse_webinspect_mock,
                                                                                   run_env_mock):
    # Given
    overrides = _setup_overrides(expected_login_macro="macro.xml")

    # When
    scan_overrides_object = ScanOverrides(overrides)
    scan_overrides_object._parse_login_macro_overrides()

    # Expect
    assert scan_overrides_object.login_macro is "macro.xml"
    assert scan_overrides_object.webinspect_upload_webmacros == ["macro.xml"]


@mock.patch('webbreaker.webinspect.scan.WebBreakerHelper.check_run_env')
@mock.patch('webbreaker.webinspect.scan.ScanOverrides._parse_webinspect_overrides')
@mock.patch('webbreaker.webinspect.scan.ScanOverrides.get_endpoint')
def test_ScanOverrides_parse_login_macro_overrides_cli_passed_loging_macro_2_upload_webmacros_success(get_endpoint_mock,
                                                                                                      parse_webinspect_mock,
                                                                                                      run_env_mock):
    # Given
    overrides = _setup_overrides(expected_login_macro="macro.xml", expected_upload_webmacro=["different_macro.xml"])

    # When
    scan_overrides_object = ScanOverrides(overrides)
    scan_overrides_object._parse_login_macro_overrides()

    # Expect
    assert scan_overrides_object.login_macro is "macro.xml"
    assert scan_overrides_object.webinspect_upload_webmacros == ["different_macro.xml", "macro.xml"]


@mock.patch('webbreaker.webinspect.scan.WebBreakerHelper.check_run_env')
@mock.patch('webbreaker.webinspect.scan.ScanOverrides._parse_webinspect_overrides')
@mock.patch('webbreaker.webinspect.scan.ScanOverrides.get_endpoint')
def test_ScanOverrides_parse_workflow_macros_overrides_success(get_endpoint_mock, parse_webinspect_mock, run_env_mock):
    # Given
    overrides = _setup_overrides()

    # When
    scan_override_object = ScanOverrides(overrides)
    scan_override_object._parse_workflow_macros_overrides()

    # Expect
    assert scan_override_object.workflow_macros == []


@mock.patch('webbreaker.webinspect.scan.WebBreakerHelper.check_run_env')
@mock.patch('webbreaker.webinspect.scan.ScanOverrides._parse_webinspect_overrides')
@mock.patch('webbreaker.webinspect.scan.ScanOverrides.get_endpoint')
def test_ScanOverrides_parse_workflow_macros_overrides_cli_passed_workflow_macros_success(get_endpoint_mock,
                                                                                          parse_webinspect_mock,
                                                                                          run_env_mock):
    # Given
    overrides = _setup_overrides(expected_workflow_macro=("workflow_macro.xml",))

    # When
    scan_override_object = ScanOverrides(overrides)
    scan_override_object._parse_workflow_macros_overrides()

    # Expect
    assert scan_override_object.workflow_macros == ["workflow_macro.xml"]
    assert scan_override_object.webinspect_upload_webmacros == ["workflow_macro.xml"]


@mock.patch('webbreaker.webinspect.scan.WebBreakerHelper.check_run_env')
@mock.patch('webbreaker.webinspect.scan.ScanOverrides._parse_webinspect_overrides')
@mock.patch('webbreaker.webinspect.scan.ScanOverrides.get_endpoint')
def test_ScanOverrides_parse_upload_webmacros_overrides_success(get_endpoint_mock, parse_webinspect_mock, run_env_mock):
    # Given
    overrides = _setup_overrides()

    # When
    scan_overrides_object = ScanOverrides(overrides)
    scan_overrides_object._parse_upload_webmacros_overrides()

    # Expect
    assert scan_overrides_object.webinspect_upload_webmacros is None

#
# @mock.patch('webbreaker.webinspect.scan.os.path.isfile')
# @mock.patch('webbreaker.webinspect.scan.WebBreakerHelper.check_run_env')
# @mock.patch('webbreaker.webinspect.scan.ScanOverrides._parse_webinspect_overrides')
# @mock.patch('webbreaker.webinspect.scan.ScanOverrides.get_endpoint')
# def test_ScanOverrides_parse_upload_webmacros_overrides_cli_passed_upload_webmacro_success(get_endpoint_mock,
#                                                                                           parse_webinspect_mock,
#                                                                                           run_env_mock, isfile_mock):
#     # Given
#     isfile_mock.return_value = False
#     overrides = _setup_overrides(expected_upload_webmacro="some.webmacro")
#
#     # When
#     scan_overrides_object = ScanOverrides(overrides)
#     scan_overrides_object._parse_upload_webmacros_overrides()
#
#     # Expect
#     # assert scan_overrides_object.webinspect_upload_webmacros is None
#     assert 0
#     # TODO I'm pretty sure this is borked.
#
#
# def test_ScanOverrides_parse_upload_policy_overrides():
#     assert 0
#     # TODO This test + removing the upload click arguments

@mock.patch('webbreaker.webinspect.scan.WebBreakerHelper.check_run_env')
@mock.patch('webbreaker.webinspect.scan.ScanOverrides._parse_webinspect_overrides')
@mock.patch('webbreaker.webinspect.scan.ScanOverrides.get_endpoint')
def test_ScanOverrides_parse_upload_setings_overrides_for_scan_target_success(get_endpoint_mock, parse_webinspect_mock,
                                                                              run_env_mock):
    # Given
    overrides = _setup_overrides()

    # When
    scan_overrides_object = ScanOverrides(overrides)
    scan_overrides_object._parse_upload_settings_overrides_for_scan_target()

    # Expect
    assert scan_overrides_object.targets is None


@mock.patch('webbreaker.webinspect.scan.ScanOverrides._get_scan_targets')
@mock.patch('webbreaker.webinspect.scan.WebBreakerHelper.check_run_env')
@mock.patch('webbreaker.webinspect.scan.ScanOverrides._parse_webinspect_overrides')
@mock.patch('webbreaker.webinspect.scan.ScanOverrides.get_endpoint')
def test_ScanOverrides_parse_upload_setings_overrides_for_scan_target_cli_passed_upload_settings_success(get_endpoint_mock,
                                                                                                         parse_webinspect_mock,
                                                                                                         run_env_mock,
                                                                                                         scan_targets_mock):
    # Given
    # mock this because we aren't testing this here.
    scan_targets_mock.return_value = {"some.site.com", "some.other.site"}

    overrides = _setup_overrides(expected_upload_settings="settings.xml")

    # When
    scan_overrides_object = ScanOverrides(overrides)
    scan_overrides_object._parse_upload_settings_overrides_for_scan_target()

    # Expect
    assert scan_overrides_object.targets == {'some.other.site', 'some.site.com'}


@mock.patch('webbreaker.webinspect.scan.ScanOverrides._get_scan_targets')
@mock.patch('webbreaker.webinspect.scan.WebBreakerHelper.check_run_env')
@mock.patch('webbreaker.webinspect.scan.ScanOverrides._parse_webinspect_overrides')
@mock.patch('webbreaker.webinspect.scan.ScanOverrides.get_endpoint')
def test_ScanOverrides_parse_upload_setings_overrides_for_scan_target_failure_NameError_exception(get_endpoint_mock,
                                                                                                  parse_webinspect_mock,
                                                                                                  run_env_mock,
                                                                                                  scan_targets_mock):
    # Given
    # a file that can't be found
    overrides = _setup_overrides(expected_upload_settings="settings.xml")
    scan_targets_mock.side_effect = NameError
    WebInspectLogHelper.log_no_settings_file = MagicMock()

    # When
    scan_overrides_object = ScanOverrides(overrides)
    with pytest.raises(SystemExit):
        scan_overrides_object._parse_upload_settings_overrides_for_scan_target()

    # Expect
    assert WebInspectLogHelper.log_no_settings_file.call_count == 1


@mock.patch('webbreaker.webinspect.scan.WebBreakerHelper.check_run_env')
@mock.patch('webbreaker.webinspect.scan.ScanOverrides._parse_webinspect_overrides')
@mock.patch('webbreaker.webinspect.scan.ScanOverrides.get_endpoint')
def test_ScanOverrides_parse_assigned_hosts_overrides_success(get_endpoint_mock, parse_webinspect_mock, run_env_mock):
    # Given
    overrides = _setup_overrides()

    # When
    scan_overrides_object = ScanOverrides(overrides)
    scan_overrides_object._parse_assigned_hosts_overrides()

    # Expect
    assert scan_overrides_object.allowed_hosts == []  # nothing passed


@mock.patch('webbreaker.webinspect.scan.WebBreakerHelper.check_run_env')
@mock.patch('webbreaker.webinspect.scan.ScanOverrides._parse_webinspect_overrides')
@mock.patch('webbreaker.webinspect.scan.ScanOverrides.get_endpoint')
def test_ScanOverrides_parse_assigned_hosts_overrides_with_start_urls_success(get_endpoint_mock, parse_webinspect_mock,
                                                                              run_env_mock):
    # Given
    overrides = _setup_overrides(expected_start_urls=["some.site.com"])

    # When
    scan_overrides_object = ScanOverrides(overrides)
    scan_overrides_object._parse_assigned_hosts_overrides()

    # Expect
    assert scan_overrides_object.allowed_hosts == ["some.site.com"]


@mock.patch('webbreaker.webinspect.scan.WebBreakerHelper.check_run_env')
@mock.patch('webbreaker.webinspect.scan.ScanOverrides._parse_webinspect_overrides')
@mock.patch('webbreaker.webinspect.scan.ScanOverrides.get_endpoint')
def test_ScanOverrides_parse_assigned_hosts_overrides_with_allowed_hosts_success(get_endpoint_mock,
                                                                                 parse_webinspect_mock,
                                                                                 run_env_mock):
    # Given
    overrides = _setup_overrides(expected_allowed_hosts=["some.site.com"])

    # When
    scan_overrides_object = ScanOverrides(overrides)
    scan_overrides_object._parse_assigned_hosts_overrides()

    # Expect
    assert scan_overrides_object.allowed_hosts == ["some.site.com"]


@mock.patch('webbreaker.webinspect.scan.WebBreakerHelper.check_run_env')
@mock.patch('webbreaker.webinspect.scan.ScanOverrides._parse_webinspect_overrides')
@mock.patch('webbreaker.webinspect.scan.ScanOverrides.get_endpoint')
def test_ScanOverrides_parse_assigned_hosts_overrides_with_allowed_hosts_and_start_urls_success(get_endpoint_mock,
                                                                                                parse_webinspect_mock,
                                                                                                run_env_mock):
    # Given
    overrides = _setup_overrides(expected_allowed_hosts=["some.site.com"], expected_start_urls=["wrong.site.com"])

    # When
    scan_overrides_object = ScanOverrides(overrides)
    scan_overrides_object._parse_assigned_hosts_overrides()

    # Expect
    assert scan_overrides_object.allowed_hosts == ["some.site.com"]



# def test_ScanOverrides_get_endpoint_success():
#     # Given
#     ScanOverrides.get_endpoint = MagicMock(return_value="webinspect_url")
#     ScanOverrides._parse_webinspect_overrides = MagicMock()
#     WebBreakerHelper.check_run_env = MagicMock(return_value="expected_run_env")
#
#     assert 0
#     # TODO this will be have to be redone/abstracted when I work on proxy


@mock.patch('webbreaker.webinspect.scan.trim_ext')
@mock.patch('webbreaker.webinspect.scan.WebBreakerHelper.check_run_env')
@mock.patch('webbreaker.webinspect.scan.ScanOverrides._parse_webinspect_overrides')
@mock.patch('webbreaker.webinspect.scan.ScanOverrides.get_endpoint')
def test_ScanOverrides_trim_overrides_success(get_endpoint_mock, parse_webinspect_mock, run_env_mock, trim_mock):
    # Trim ext is tested elsewhere so in this test all we really care about is that it is called 7 times.

    # Given
    overides = _setup_overrides()
    scan_overrides_object = ScanOverrides(overides)

    # When
    scan_overrides_object._trim_overrides()

    # Expect
    assert trim_mock.call_count == 7


