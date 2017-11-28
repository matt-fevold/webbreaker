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


@mock.patch('webbreaker.confighelper.Config.set_config')
@mock.patch('webbreaker.confighelper.Config.set_path')
def test_config_init_variables(set_path_mock, set_config_mock):
    set_path_mock.return_value = '/test/path'
    set_config_mock.return_value = None
    test_obj = Config()

    assert os.path.exists(test_obj.home)
    assert test_obj.install == '/test/path'
    assert test_obj.config == '/test/path'
    assert test_obj.etc == '/test/path'
    assert test_obj.git == '/test/path'
    assert test_obj.log == '/test/path'
    assert test_obj.agent_json == '/test/path'
    assert test_obj.secret == '/test/path/.webbreaker'
    assert set_config_mock.call_count == 1


@mock.patch('webbreaker.confighelper.Config.set_config')
@mock.patch('webbreaker.confighelper.Config.install_path')
@mock.patch('webbreaker.confighelper.os.makedirs')
@mock.patch('webbreaker.confighelper.open', new_callable=mock_open, read_data="data")
def test_set_path_no_install_success(open_mock, mkdir_mock, install_path_mock, set_config_mock):
    test_obj = Config()
    test_obj.install = '/test/install/path'
    result = test_obj.set_path(dir_path='test_dir', file_name='test.file')

    assert open_mock.call_count == 1
    assert mkdir_mock.call_count == 1
    assert result == '/test/install/path/test_dir/test.file'

@mock.patch('webbreaker.confighelper.Config.set_config')
@mock.patch('webbreaker.confighelper.Config.install_path')
@mock.patch('webbreaker.confighelper.os.makedirs')
@mock.patch('webbreaker.confighelper.open', new_callable=mock_open, read_data="data")
def test_set_path_install_success(open_mock, mkdir_mock, install_path_mock, set_config_mock):
    test_obj = Config()
    test_obj.install = '/test/install/path'
    result = test_obj.set_path(install='test')

    assert open_mock.call_count == 1
    assert mkdir_mock.call_count == 1
    assert result == '/test/install/path/test_dir/test.file'



@mock.patch('webbreaker.confighelper.Config.set_config')
@mock.patch('webbreaker.confighelper.os.makedirs')
@mock.patch('webbreaker.confighelper.open', new_callable=mock_open, read_data="data")
def test_set_path_dir_file_success(open_mock, mkdir_mock, set_config_mock):
    test_obj = Config()
    test_obj.install = '/test/install/path'
    result = test_obj.set_path(dir_path='test_dir', file_name='test.file')

    assert open_mock.call_count == 1
    assert mkdir_mock.call_count == 1
    assert result == '/test/install/path/test_dir/test.file'


@mock.patch('webbreaker.confighelper.Config.set_config')
@mock.patch('webbreaker.confighelper.Config.install_path')
@mock.patch('webbreaker.confighelper.os.makedirs')
@mock.patch('webbreaker.confighelper.open', new_callable=mock_open, read_data="data")
def test_set_path_dir_file_exception(open_mock, mkdir_mock, install_path_mock, set_config_mock):
    e = IOError("Test Error")
    open_mock.side_effect = e
    test_obj = Config()
    test_obj.install = '/test/install/path'
    result = test_obj.set_path(dir_path='test_dir', file_name='test.file')

    assert open_mock.call_count == 1
    assert mkdir_mock.call_count == 1
    assert result == 1


@mock.patch('webbreaker.confighelper.Config.set_config')
@mock.patch('webbreaker.confighelper.Config.install_path')
@mock.patch('webbreaker.confighelper.os.path.exists')
@mock.patch('webbreaker.confighelper.open', new_callable=mock_open, read_data="data")
def test_set_path_dir_file_exists_dir(open_mock, exist_mock, install_path_mock, set_config_mock):
    exist_mock.return_value = True
    test_obj = Config()
    test_obj.install = '/test/install/path'
    result = test_obj.set_path(dir_path='test_dir', file_name='test.file')

    assert open_mock.call_count == 1
    assert result == '/test/install/path/test_dir/test.file'


@mock.patch('webbreaker.confighelper.Config.set_config')
@mock.patch('webbreaker.confighelper.Config.install_path')
@mock.patch('webbreaker.confighelper.os.makedirs')
@mock.patch('webbreaker.confighelper.open', new_callable=mock_open, read_data="data")
def test_set_path_file_success(open_mock, mkdir_mock, install_path_mock, set_config_mock):
    test_obj = Config()
    test_obj.install = '/test/install/path'
    result = test_obj.set_path(file_name='test.file')

    assert open_mock.call_count == 1
    assert mkdir_mock.call_count == 1
    assert result == '/test/install/path/test.file'


@mock.patch('webbreaker.confighelper.Config.set_config')
@mock.patch('webbreaker.confighelper.Config.install_path')
@mock.patch('webbreaker.confighelper.os.makedirs')
@mock.patch('webbreaker.confighelper.open', new_callable=mock_open, read_data="data")
def test_set_path_file_exception(open_mock, mkdir_mock, install_path_mock, set_config_mock):
    e = IOError("Test Error")
    open_mock.side_effect = e
    test_obj = Config()
    test_obj.install = '/test/install/path'
    result = test_obj.set_path(file_name='test.file')

    assert open_mock.call_count == 1
    assert mkdir_mock.call_count == 1
    assert result == 1


@mock.patch('webbreaker.confighelper.Config.set_config')
@mock.patch('webbreaker.confighelper.Config.install_path')
@mock.patch('webbreaker.confighelper.os.path.exists')
@mock.patch('webbreaker.confighelper.open', new_callable=mock_open, read_data="data")
def test_set_path_file_exists_dir(open_mock, exist_mock, install_path_mock, set_config_mock):
    exist_mock.return_value = True
    test_obj = Config()
    test_obj.install = '/test/install/path'
    result = test_obj.set_path(file_name='test.file')

    assert open_mock.call_count == 1
    assert result == '/test/install/path/test.file'


@mock.patch('webbreaker.confighelper.Config.install_path')
@mock.patch('webbreaker.confighelper.os.makedirs')
def test_set_path_dir_success(mkdir_mock, install_path_mock):
    test_obj = Config()
    test_obj.install = '/test/install/path'
    result = test_obj.set_path(dir_path='test_dir')

    assert mkdir_mock.call_count == 1
    assert result == '/test/install/path/test_dir'


@mock.patch('webbreaker.confighelper.Config.install_path')
@mock.patch('webbreaker.confighelper.os.path.exists')
@mock.patch('webbreaker.confighelper.open', new_callable=mock_open, read_data="data")
def test_set_path_exists(open_mock, exist_mock, install_path_mock):
    exist_mock.return_value = True
    test_obj = Config()
    test_obj.install = '/test/install/path'
    result = test_obj.set_path(dir_path='test_dir')

    assert exist_mock.call_count == 1
    assert result == '/test/install/path/test_dir'
