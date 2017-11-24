import mock
from mock import mock_open

from webbreaker.confighelper import Config
import os

try:
    import ConfigParser as configparser

    config = configparser.SafeConfigParser()
except ImportError:  # Python3
    import configparser

    config = configparser.ConfigParser()


@mock.patch('webbreaker.confighelper.Config.install_path')
def test_config_init_variables(install_mock):
    install_mock.return_value = None
    test_obj = Config()

    assert os.path.exists(test_obj.install)
    assert test_obj.install == os.path.abspath('')
    assert test_obj.config_name == 'config.ini'
    assert test_obj.config == os.path.join(test_obj.install, test_obj.config_name)

    assert test_obj.etc is None
    assert test_obj.git is None
    assert test_obj.log is None
    assert test_obj.secret is None
    assert test_obj.agent_json is None


@mock.patch('webbreaker.confighelper.Config.set_path')
@mock.patch('webbreaker.confighelper.shutil.copy')
@mock.patch('webbreaker.confighelper.config.get')
def test_install_path_no_config_file(get_mock, copy_mock, path_mock):
    path_mock.return_value = '/test/set/path'
    copy_mock.return_value = True
    get_mock.return_valule = '/config/get/called'

    test_obj = Config()
    test_obj.config = '/no/config.ini/here'
    test_obj.install_path()

    assert copy_mock.call_count == 1
    assert get_mock.call_count == 2
    assert path_mock.call_count == 12
    assert test_obj.install == '/test/set/path'


@mock.patch('webbreaker.confighelper.Config.set_path')
@mock.patch('webbreaker.confighelper.config.get')
def test_install_path_get_config_path_success(get_mock, path_mock):
    path_mock.return_value = '/test/set/path'
    get_mock.return_valule = '/config/get/called'

    test_obj = Config()
    assert get_mock.call_count == 1
    assert path_mock.call_count == 6
    assert test_obj.install == '/test/set/path'


@mock.patch('webbreaker.confighelper.Config.set_path')
@mock.patch('webbreaker.confighelper.config.get')
@mock.patch('webbreaker.confighelper.config.add_section')
@mock.patch('webbreaker.confighelper.config.set')
@mock.patch('webbreaker.confighelper.open', new_callable=mock_open, read_data="data")
def test_install_path_get_config_path_exception(open_mock, set_mock, add_mock, get_mock, path_mock):
    e = configparser.NoSectionError("Test Error")
    get_mock.side_effect = e
    add_mock.return_value = True
    set_mock.return_value = True
    path_mock.return_value = '/test/set/path'

    test_obj = Config()
    assert get_mock.call_count == 1
    assert add_mock.call_count == 1
    assert set_mock.call_count == 1
    assert path_mock.call_count == 6
    assert test_obj.install == '/test/set/path'


@mock.patch('webbreaker.confighelper.Config.set_path')
@mock.patch('webbreaker.confighelper.config.get')
def test_install_path_init_variables(get_mock, path_mock):
    path_mock.return_value = '/test/set/path'
    get_mock.return_valule = '/config/get/called'

    test_obj = Config()
    assert path_mock.call_count == 6
    assert test_obj.install == '/test/set/path'

# def test_set_path_dir_file_success():
# def test_set_path_dir_file_exception():
# def test_set_path_dir_file_exists_dir():
# def test_set_path_file_success():
# def test_set_path_file_exception():
# def test_set_path_file_exists_dir():
# def test_set_path_dir_success():
# def test_set_path_exists():
