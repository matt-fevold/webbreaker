import mock
import pytest

from webbreaker.webinspect.webinspect_config import WebInspectConfig
import webbreaker.common.confighelper

#conf_get from confighelper too?

@mock.patch('webbreaker.common.confighelper.set_path')
def test_one_server_success(set_path_mock):
    #TODO: test to select the working server (first one)
    pass

def test_two_server():
    # TODO: two servers: one fail, one success, need to make sure it will go through the list
    # TODO: and select the correct server
    pass

def test_no_server_availble():
    #TODO: go through the list one at a time and exit gracefully
    pass