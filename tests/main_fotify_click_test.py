#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
import mock

from webbreaker.__main__ import cli as webbreaker


@pytest.fixture()
def runner():
    from click.testing import CliRunner
    return CliRunner()


@mock.patch('webbreaker.__main__.FortifyListApplicationVersions.__init__')
def test_fortify_list_with_config_credentials_success(list_app_version_mock, runner):
    list_app_version_mock.return_value = None

    runner.invoke(webbreaker, ['fortify', 'list'])

    list_app_version_mock.assert_called_once_with(None, None, None)


@mock.patch('webbreaker.__main__.FortifyListApplicationVersions.__init__')
def test_fortify_list_with_cli_creds_success(list_app_version_mock, runner):
    list_app_version_mock.return_value = None

    runner.invoke(webbreaker, ['fortify', 'list', '--fortify_user', 'user', '--fortify_password', 'pass'])
    list_app_version_mock.assert_called_once_with('user', 'pass', None)


@mock.patch('webbreaker.__main__.FortifyDownload.__init__')
def test_fortify_download_scan_no_application_success(download_mock, runner):
    download_mock.return_value = None

    runner.invoke(webbreaker, ['fortify', 'download', '--version', 'some_version'])

    download_mock.assert_called_once_with(None, None, None, 'some_version')


@mock.patch('webbreaker.__main__.FortifyDownload.__init__')
def test_fortify_download_scan_with_application_success(download_mock, runner):
    download_mock.return_value = None

    runner.invoke(webbreaker, ['fortify', 'download', '--version', 'some_version', '--application', 'some_application'])

    download_mock.assert_called_once_with(None, None, 'some_application', 'some_version')


@mock.patch('webbreaker.__main__.FortifyUpload.__init__')
def test_fortify_upload_scan_success(upload_mock, runner):
    upload_mock.return_value = None

    runner.invoke(webbreaker, ['fortify', 'upload', '--version', 'some_version'])

    upload_mock.assert_called_once_with(None, None, None, 'some_version', None)


@mock.patch('webbreaker.__main__.FortifyUpload.__init__')
def test_fortify_upload_scan_with_application_success(upload_mock, runner):
    upload_mock.return_value = None

    runner.invoke(webbreaker, ['fortify', 'upload', '--version', 'some_version', '--application', 'some_application'])

    upload_mock.assert_called_once_with(None, None, 'some_application', 'some_version', None)


@mock.patch('webbreaker.__main__.FortifyUpload.__init__')
def test_fortify_upload_scan_with_scan_name_success(upload_mock, runner):
    upload_mock.return_value = None

    runner.invoke(webbreaker, ['fortify', 'upload', '--version', 'some_version', '--scan_name', 'some_scan_name'])

    upload_mock.assert_called_once_with(None, None, None, 'some_version', 'some_scan_name')
