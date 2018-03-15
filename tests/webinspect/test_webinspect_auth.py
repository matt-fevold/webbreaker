import pytest

import mock

from webbreaker.webinspect.webinspectauth import WebInspectAuth


@pytest.fixture(params=[
    ['true', True],
    ['false', False]
])
def true_false(request):
    return request.param

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


# want to test all paths that can be reached in the authenticate method.


@mock.patch('webbreaker.webinspect.webinspectauth.SecretClient')
@mock.patch('webbreaker.webinspect.webinspectauth.config')
def test_auth_not_required_RAN_WITH_no_cli_input_RAN_WITH_cli_input_AND_creds_in_config(mock_config, mock_secret_client, cli_credentials):
    mock_config.return_value.get.return_value = 'false'  # auth not required

    # credentials that are read in from config.
    mock_secret_client.return_value.get.side_effect = ["config_username", "config_password"]

    auth_config = WebInspectAuth()
    # run 1 None, None :: run 2 cli_username, cli_password are passed in.
    assert auth_config.authenticate(cli_credentials[0], cli_credentials[1]) == (None, None)

@mock.patch('webbreaker.webinspect.webinspectauth.SecretClient')
@mock.patch('webbreaker.webinspect.webinspectauth.config')
def test_auth_not_required_RAN_WITH_no_cli_input_RAN_WITH_cli_input_AND_no_creds_in_config(mock_config, mock_secret_client, cli_credentials):
    mock_config.return_value.get.return_value = 'false'  # auth not required

    # credentials that are read in from config.
    mock_secret_client.return_value.get.side_effect = None

    auth_config = WebInspectAuth()
    # run 1 None, None :: run 2 cli_username, cli_password are passed in.
    assert auth_config.authenticate(cli_credentials[0], cli_credentials[1]) == (None, None)


# test auth required with cli supplied credentials with and without config file credentials
@mock.patch('webbreaker.webinspect.webinspectauth.SecretClient')
@mock.patch('webbreaker.webinspect.webinspectauth.config')
def test_auth_required_cli_passed_creds_RAN_WITH_no_creds_in_config_RAN_WITH_creds_in_config(mock_config, mock_secret_client, config_credentials):
    # auth required
    mock_config.get.return_value = "true"
    # credentials read in from config: one run will have values, one run won't
    mock_secret_client.return_value.get.side_effect = config_credentials

    auth_config = WebInspectAuth()
    assert auth_config.authenticate("cli_username", "cli_password") == ("cli_username", "cli_password")


# have to break this next one into two tests since without values in config we prompt the user for input which
#   requires special handling.
@mock.patch('webbreaker.webinspect.webinspectauth.SecretClient')
@mock.patch('webbreaker.webinspect.webinspectauth.config')
def test_auth_required_creds_not_in_config_no_cli_creds_RAN_WITH_creds_in_config(mock_config, mock_secret_client):
    mock_config.get.return_value = "true" # auth required

    # credentials that are read in from config.
    mock_secret_client.return_value.get.side_effect = ["config_username", "config_password"]

    auth_config = WebInspectAuth()

    assert auth_config.authenticate(None, None) == ("config_username", "config_password")


# test the click stuff
@mock.patch('webbreaker.webinspect.webinspectauth.auth_prompt')
@mock.patch('webbreaker.webinspect.webinspectauth.SecretClient')
@mock.patch('webbreaker.webinspect.webinspectauth.config')
def test_auth_required_creds_not_in_config_no_cli_creds_RAN_WITH_no_creds_in_config(mock_config, mock_secret_client, mock_prompt):
    mock_config.get.return_value = "true"  # auth required

    # credentials that are read in from config.
    mock_secret_client.return_value.get.side_effect = [None, None]

    # We only care that auth_prompt returns a tuple of username, password so choose to mock here
    # to get around issue I was having with testing stdin and click. This is the desired effect
    #   and we don't want to test click. It works. . .
    mock_prompt.return_value = ("prompt_username", "prompt_password")

    auth_config = WebInspectAuth()
    assert auth_config.authenticate(None, None) == ("prompt_username","prompt_password")


@mock.patch('webbreaker.webinspect.webinspectauth.config')
def test__check_if_authenticate_required_true_false(mock_config, true_false):
    # auth required in config or not (returns 'true' then 'false')
    mock_config.get.return_value = true_false[0]

    auth_config = WebInspectAuth()

    assert auth_config.require_authenticate == true_false[1]


# TODO finish this test
#   was having issues raising an error with side_effects.
@mock.patch('webbreaker.webinspect.webinspectauth.config')
def test__check_if_authenticate_required_exception_handling(mock_config):
    pass


