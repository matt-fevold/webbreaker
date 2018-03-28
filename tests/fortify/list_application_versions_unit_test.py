

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


@mock.patch('webbreaker.fortify.list_application_versions.FortifyApi', autospec=True)
@mock.patch('webbreaker.fortify.list_application_versions.FortifyAuth')
def test_fortify_list_success(auth_mock, api_mock):
    auth_mock.return_value.authenticate.return_value = ('user', 'pass')
    
    FortifyListApplicationVersions(None, None, None)

    api_mock
