

import pytest
import mock

from fortifyapi.fortify import FortifyResponse

from webbreaker.fortify.list_application_versions import FortifyListApplicationVersions

class ClassHelper(object):
    """Container for all Fortify SSC API responses, even errors."""

    def __init__(self, success=False, response_code=-1):
        self.message = 'Test api message'
        self.success = success
        self.response_code = response_code
        self.data = 'Test Data! Will likely need to change this later! '
        self.headers = 'Test Header!'

    def get_token(self):
        return 'a valid'


@mock.patch('webbreaker.fortify.list_application_versions.FortifyHelper.get_token')
@mock.patch('webbreaker.fortify.list_application_versions.FortifyHelper.list_versions')
@mock.patch('webbreaker.fortify.list_application_versions.FortifyAuth')
def test_fortify_list_success(auth_mock, list_all_mock, get_token_mock):
    auth_mock.return_value.authenticate.return_value = ('user', 'pass')
    get_token_mock.return_value.get_token.return_value = 'a valid token'

    FortifyListApplicationVersions(None, None, None)

    assert list_all_mock.call_count == 1


@mock.patch('webbreaker.fortify.list_application_versions.FortifyHelper.get_token')
@mock.patch('webbreaker.fortify.list_application_versions.FortifyHelper.list_application_versions')
@mock.patch('webbreaker.fortify.list_application_versions.FortifyAuth')
def test_fortify_list_application_success(auth_mock, list_application_mock, get_token_mock):
    auth_mock.return_value.authenticate.return_value = ('user', 'pass')
    get_token_mock.return_value.get_token.return_value = 'a valid token'

    FortifyListApplicationVersions(None, None, "Some Application")

    assert list_application_mock.call_count == 1


