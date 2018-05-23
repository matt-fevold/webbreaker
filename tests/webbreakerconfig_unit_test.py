import mock
from webbreaker.common.webbreakerconfig import trim_ext

def test_ScanOverrides_trim_ext_success():
    # Given
    file = "/valid/path/settings.xml"

    # When
    result = trim_ext(file=file)

    # Expect
    assert result == "settings"



def test_ScanOverrides_trim_ext_file_is_none_success():
    # Given
    file = None

    # When
    result = trim_ext(file=file)

    # Expect
    assert result is None



def test_ScanOverrides_trim_ext_file_is_list_success():
    # Given

    file = ["/valid/path/settings.xml", "/valid/path/to/different.xml"]

    # When
    result = trim_ext(file=file)

    # Expect
    assert result == ["settings", "different"]


@mock.patch('webbreaker.webinspect.scan.os.path.isfile')
def test_trim_ext_file_is_list_valid_file_success(isfile_mock):
    # Given
    isfile_mock.return_value = True
    file = ["/valid/path/settings.xml", "/valid/path/to/different.xml"]

    # When
    result = trim_ext(file=file)

    # Expect
    assert result == ["/valid/path/settings", "/valid/path/to/different"]
