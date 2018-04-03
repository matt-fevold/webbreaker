

import mock
import pytest
from webbreaker.fortify.download import FortifyDownload


# mock config to skip reading from config file
@mock.patch('webbreaker.fortify.list_application_versions.FortifyConfig')
@mock.patch('webbreaker.fortify.download.FortifyHelper.find_version_id')
@mock.patch('webbreaker.fortify.download.FortifyHelper.get_token')
@mock.patch('webbreaker.fortify.download.FortifyHelper.download_scan')
@mock.patch('webbreaker.fortify.download.FortifyAuth')
def test_fortify_download_success(auth_mock, download_mock, get_token_mock, find_version_mock, config_mock):
    version = "Some Version"
    application = "Some Application"

    auth_mock.return_value.authenticate.return_value = ('user', 'pass')
    get_token_mock.return_value.get_token.return_value = 'a valid token'

    FortifyDownload(None, None, None, version)

    find_version_mock.called_once_with(version)
    assert find_version_mock.call_count == 1

    assert download_mock.call_count == 1

# TODO add more tests after Kyler's changes are done.
