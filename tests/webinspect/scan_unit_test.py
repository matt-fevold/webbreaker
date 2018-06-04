
from webbreaker.webinspect.scan import WebInspectScan

import mock


try:  # python 3
    from queue import Queue, Empty
except ImportError:  # python 2
    from Queue import Queue as queue


# TODO: In scan mock, need to check if xml_parsing is called once

@mock.patch('webbreaker.webinspect.scan.ET.ElementTree')
@mock.patch('webbreaker.webinspect.scan.Vulnerabilities.write_to_json')
@mock.patch('webbreaker.webinspect.scan.Vulnerabilities.write_to_console')
@mock.patch('webbreaker.webinspect.scan.Config')
@mock.patch('webbreaker.webinspect.scan.WebInspectConfig')
@mock.patch('webbreaker.webinspect.scan.ScanOverrides')
@mock.patch('webbreaker.webinspect.scan.WebInspectScan.scan')
def test_xml_parsing_success(scan_mock, scan_overrides_mock, wi_config_mock, config_mock, write_to_console_mock,
                             write_to_json_mock, element_tree_mock):
    # Given
    scan_object = WebInspectScan({})
    scan_object.scan_overrides.settings = 'litecart'
    scan_object.scan_id = "test_scan_id"
    scan_object.scan_overrides.scan_name = "test_name"
    filename = "test.xml"

    #When
    scan_object.xml_parsing(filename)

    #Expect
    assert scan_mock.call_count == 1
    assert write_to_console_mock.call_count == 1
    assert write_to_json_mock.call_count == 1
    write_to_json_mock.assert_called_once_with(filename, "test_name", "test_scan_id")
    write_to_console_mock.assert_called_once_with("test_name")

