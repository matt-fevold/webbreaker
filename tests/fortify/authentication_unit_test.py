
import pytest
import mock

from webbreaker.fortify.authentication import FortifyAuth

# fixture for passing in creds and not passing in creds via cli
@pytest.fixture(params=[
    [None, None],
    ["cli_username", "cli_password"]
])
def cli_credentials(request):
    return request.param


# fixture for passing in creds and not passing in creds via config
@pytest.fixture(params=[
    [None, None],
    ["config_username", "config_password"]
])
def config_credentials(request):
    return request.param


# mocking secret client here so we don't make any config calls - speeds up test.
@mock.patch('webbreaker.fortify.authentication.SecretClient')
def test_authenticate_cli_passed_credentials_success(secret_mock):
    fortify_auth = FortifyAuth()
    username, password = fortify_auth.authenticate("cli_username", "cli_password")

    assert username == "cli_username"
    assert password == "cli_password"


# mocking secret client so we can fake reading from the config
@mock.patch('webbreaker.fortify.authentication.SecretClient')
def test_authenticate_read_from_config_success(secret_mock):
    # have the config read the following values
    secret_mock.return_value.get.side_effect = ["config_username", "config_password"]
    fortify_auth = FortifyAuth()

    # None, None means no cli passed credentials
    username, password = fortify_auth.authenticate(None, None)

    assert username == "config_username"
    assert password == "config_password"


@mock.patch('webbreaker.fortify.authentication.auth_prompt')
# mocking secret client here so we don't make any config calls - speeds up test.
@mock.patch('webbreaker.fortify.authentication.SecretClient')
def test_authenticate_prompt_user_success(secret_mock, auth_prompt_mock):
    # When
    secret_mock.return_value.get.side_effect = [None, None]
    auth_prompt_mock.return_value = ("prompt_username", "prompt_password")

    # Given
    fortify_auth = FortifyAuth()
    # None, None means no cli passed credentials
    username, password = fortify_auth.authenticate(None, None)

    # Expect
    assert username == "prompt_username"
    assert password == "prompt_password"


@mock.patch('webbreaker.fortify.authentication.SecretClient')
def test_authenticate_write_credentials_success(secret_mock):
    fortify_auth = FortifyAuth()
    fortify_auth.write_credentials("some_username", "some_password")

    assert secret_mock.return_value.get.call_count == 2


@mock.patch('webbreaker.fortify.authentication.SecretClient')
def test_authenticate_clear_credentials_success(secret_mock):
    fortify_auth = FortifyAuth()
    fortify_auth.clear_credentials()

    secret_mock.return_value.clear_credentials.assert_called_once_with('fortify', 'username', 'password')


@mock.patch('webbreaker.fortify.authentication.SecretClient')
def test_authenticate_has_credentials_success(secret_mock):
    # have the config read the following values
    secret_mock.return_value.get.side_effect = ["config_username", "config_password"]

    fortify_auth = FortifyAuth()
    result = fortify_auth._has_auth_creds()

    assert result is True


@mock.patch('webbreaker.fortify.authentication.SecretClient')
def test_authenticate_has_credentials_fail(secret_mock):
    # have the config read the following values
    secret_mock.return_value.get.side_effect = [None, None]

    fortify_auth = FortifyAuth()
    result = fortify_auth._has_auth_creds()

    assert result is False
