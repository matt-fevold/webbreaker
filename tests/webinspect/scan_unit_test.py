import mock
import pytest

from webbreaker.webinspect.scan import WebInspectScan
import webbreaker.common.confighelper

@mock.patch('webbreaker.webinspect.scan.WebInspectScan.xml_parsing')
def test_xml_parsing_success(xml_parsing_mock):


    xml_parsing_mock.return_value = "test_file.xml"

    assert xml_parsing_mock.call_count == 1