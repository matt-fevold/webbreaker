
from webbreaker.common.confighelper import Config
import pytest
from mock import MagicMock
from webbreaker.webinspect.scan import ScanOverrides
from webbreaker.common.webbreakerhelper import WebBreakerHelper
from webbreaker.webinspect.common.loghelper import WebInspectLogHelper
import os

def _setup_overrides(expected_username=None, expected_password=None, expected_allowed_hosts=(), expected_start_urls=(),
                     expected_timeout=0, expected_settings='default', expected_upload_settings=None,
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


def _setup_mocks():
    """
    Avoids redundant mock setup. Can still be overwritten as necessary.
    These mocks prevent ScanOverrides.__init__ from calling some outside functions - speeding up tests
    :return:
    """
    ScanOverrides.get_endpoint = MagicMock(return_value="webinspect_url")
    ScanOverrides._parse_webinspect_overrides = MagicMock()
    WebBreakerHelper.check_run_env = MagicMock(return_value="expected_run_env")


def test_ScanOverrides_init_success():
    # Given
    # mock function calls within init so we can focus the test.
    _setup_mocks()
    overrides = _setup_overrides()

    # When
    scan_override_object = ScanOverrides(overrides)

    # Expect
    assert scan_override_object.webinspect_dir == '/path/to/git'

    assert scan_override_object.username is None
    assert scan_override_object.password is None

    assert scan_override_object.settings is 'default'
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


def test_ScanOverrides_init_failure_environment_error_exception():
    # I'm not 100% where this is raised, but I can't be certain nothing doesn't call it so going to be a bit hacky
    # and just call it somewhere to make sure it is properly handled with a sys.exit and a log call.

    # Given
    # mock function calls within init so we can focus the test
    _setup_mocks()

    WebInspectLogHelper.log_error_scan_overrides_parsing_error = MagicMock()
    WebBreakerHelper.check_run_env = MagicMock(side_effect=EnvironmentError)

    overrides = _setup_overrides()

    # When

    # if this doesn't raise SystemExit then it will fail.
    with pytest.raises(SystemExit):
        ScanOverrides(overrides)

    # Expect
    assert WebInspectLogHelper.log_error_scan_overrides_parsing_error.call_count == 1


def test_ScanOverrides_init_failure_type_error_exception():
    # I'm not 100% where this is raised, but I can't be certain nothing doesn't call it so going to be a bit hacky
    # and just call it somewhere to make sure it is properly handled with a sys.exit and a log call.

    # Given

    # mock function calls within init so we can focus the test
    _setup_mocks()

    ScanOverrides._parse_webinspect_overrides = MagicMock(side_effect=TypeError)
    WebInspectLogHelper.log_error_scan_overrides_parsing_error = MagicMock()
    overrides = _setup_overrides()

    # When
    with pytest.raises(SystemExit):
        ScanOverrides(overrides)

    assert WebInspectLogHelper.log_error_scan_overrides_parsing_error.call_count == 1


def test_ScanOverrides_get_formatted_overrides_success():
    # Test will fail for now - I want to test this after parse_webinspect_overrides to ensure everything is all good.

    # Given
    _setup_mocks()
    overrides = _setup_overrides()

    # When
    scan_overrides_object = ScanOverrides(overrides)
    formatted_overrides_dict = scan_overrides_object.get_formatted_overrides()

    # Expect
    assert formatted_overrides_dict['webinspect_settings'] == 'default'
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
    assert formatted_overrides_dict['webinspect_workflow_macros'] is None
    assert formatted_overrides_dict['webinspect_allowed_hosts'] is None
    assert formatted_overrides_dict['webinspect_scan_size'] is None
    assert formatted_overrides_dict['fortify_user'] is None


def test_ScanOverrides_parse_webinspect_overrides_success():
    # TODO not working but this is the general flow - I want to make sure each is called.

    # Given

    # can't use setup_mocks sadly - can't mock parse_webinspect_options
    ScanOverrides.get_endpoint = MagicMock(return_value="webinspect_url")
    WebBreakerHelper.check_run_env = MagicMock(return_value="expected_run_env")
    overrides = _setup_overrides()

    ScanOverrides._trim_overrides = MagicMock()
    ScanOverrides._parse_scan_name_overrides = MagicMock()
    ScanOverrides._parse_upload_settings_overrides = MagicMock()
    ScanOverrides._parse_login_macro_overrides = MagicMock()
    ScanOverrides._parse_workflow_macros_overrides = MagicMock()
    ScanOverrides._parse_upload_webmacros_overrides = MagicMock()
    ScanOverrides._parse_upload_policy_overrides = MagicMock()
    ScanOverrides._parse_upload_settings_overrides_for_scan_target = MagicMock()
    ScanOverrides._parse_assigned_hosts_overrides = MagicMock()

    # When
    ScanOverrides(overrides)  # this will call _parse_webinspect_overrides

    # Expect
    assert ScanOverrides._trim_overrides.call_count == 1
    assert ScanOverrides._parse_scan_name_overrides.call_count == 1
    assert ScanOverrides._parse_upload_settings_overrides.call_count == 1
    assert ScanOverrides._parse_login_macro_overrides.call_count == 1
    assert ScanOverrides._parse_workflow_macros_overrides.call_count == 1
    assert ScanOverrides._parse_upload_webmacros_overrides.call_count == 1
    assert ScanOverrides._parse_upload_policy_overrides.call_count == 1
    assert ScanOverrides._parse_upload_settings_overrides_for_scan_target.call_count == 1
    assert ScanOverrides._parse_assigned_hosts_overrides.call_count == 1


def test_ScanOverrides_parse_scan_name_overrides_success():
    # Given
    _setup_mocks()  # will mock _parse_webinspect_overrides so we can call the individual parse command
    overrides = _setup_overrides()

    # When
    scan_overrides_object = ScanOverrides(overrides)
    scan_overrides_object._parse_scan_name_overrides()

    # Expect
    assert scan_overrides_object.scan_name[0:11] in ['webinspect-']  # the randomly generated scan name


def test_ScanOverrides_parse_scan_name_overrides_cli_passed_scan_name_success():
    # Given
    _setup_mocks()  # will mock _parse_webinspect_overrides so we can call the individual parse command
    overrides = _setup_overrides(expected_scan_name="Expected_Scan_Name")

    # When
    scan_overrides_object = ScanOverrides(overrides)
    scan_overrides_object._parse_scan_name_overrides()

    # Expect
    assert scan_overrides_object.scan_name in ["Expected_Scan_Name"]  


def test_ScanOverrides_parse_scan_name_overrides_jenkins_job_BUILD_TAG_success():
    # Given
    _setup_mocks()  # will mock _parse_webinspect_overrides so we can call the individual parse command
    WebBreakerHelper.check_run_env = MagicMock(return_value="jenkins")
    # _parse_scan_name_overrides makes 2 calls to getevn, first one checks if there is a / in the return value and
    #   follows 2 different paths. We want to test both pathsf
    os.getenv = MagicMock(side_effect=["JOB_NAME//", "EXPECTED_BUILD_TAG"])

    overrides = _setup_overrides()

    # When
    scan_overrides_object = ScanOverrides(overrides)
    scan_overrides_object._parse_scan_name_overrides()

    # Expect
    assert scan_overrides_object.scan_name in ['EXPECTED_BUILD_TAG']
