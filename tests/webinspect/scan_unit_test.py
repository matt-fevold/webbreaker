
from webbreaker.common.confighelper import Config
import pytest
from mock import MagicMock
from webbreaker.webinspect.scan import ScanOverrides
from webbreaker.common.webbreakerhelper import WebBreakerHelper
from webbreaker.webinspect.common.loghelper import WebInspectLogHelper


def _setup_overrides(expected_username=None, expected_password=None, expected_allowed_hosts=(), expected_start_urls=(),
                     expected_timeout=0, expected_settings='default', expected_upload_settings=None,
                     expected_upload_macro=None, expected_upload_webmacro=None, expected_login_macro=None,
                     expected_upload_policy=None, expected_scan_policy=None, expected_scan_name=None,
                     expected_scan_mode=None, expected_fortify_user=None, expected_size='large',
                     expected_scan_scope=None, expected_scan_start=None, expected_workflow_macro=()):
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
        'scan_start': expected_scan_start
    }

    return overrides


def test_ScanOverrides_init_success():
    # mock function calls within init so we can focus the test.
    Config.git = MagicMock(return_value='/path/to/git')  # mock so no file read
    ScanOverrides.get_endpoint = MagicMock(return_value="webinspect_url")
    ScanOverrides._parse_webinspect_overrides = MagicMock()
    WebBreakerHelper.check_run_env = MagicMock(return_value="expected_run_env")

    # Given

    overrides = _setup_overrides()

    # When
    scan_override_object = ScanOverrides(overrides)

    # Expect
    # assert scan_override_object.webinspect_dir == '/path/to/git'

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

    # mock function calls within init so we can focus the test
    Config.git = MagicMock()  # mock so no file read
    ScanOverrides.get_endpoint = MagicMock()
    ScanOverrides._parse_webinspect_overrides = MagicMock()
    WebInspectLogHelper.log_error_scan_overrides_parsing_error = MagicMock()

    # Given
    WebInspectLogHelper.log_error_scan_overrides_parsing_error = MagicMock()
    WebBreakerHelper.check_run_env = MagicMock(side_effect=EnvironmentError)
    overrides = _setup_overrides()


    # When
    with pytest.raises(SystemExit):
        ScanOverrides(overrides)

    assert WebInspectLogHelper.log_error_scan_overrides_parsing_error.call_count == 1


def test_ScanOverrides_init_failure_type_error_exception():
    # I'm not 100% where this is raised, but I can't be certain nothing doesn't call it so going to be a bit hacky
    # and just call it somewhere to make sure it is properly handled with a sys.exit and a log call.

    # mock function calls within init so we can focus the test
    Config.git = MagicMock()  # mock so no file read
    ScanOverrides.get_endpoint = MagicMock()
    ScanOverrides._parse_webinspect_overrides = MagicMock()
    WebBreakerHelper.check_run_env = MagicMock()

    # Given
    ScanOverrides._parse_webinspect_overrides = MagicMock(side_effect=TypeError)
    WebInspectLogHelper.log_error_scan_overrides_parsing_error = MagicMock()
    overrides = _setup_overrides()

    # When
    with pytest.raises(SystemExit):
        ScanOverrides(overrides)

    assert WebInspectLogHelper.log_error_scan_overrides_parsing_error.call_count == 1


def test_ScanOverrides_parse_webinspect_overrides_success():
    pass
