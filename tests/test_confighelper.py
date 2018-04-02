import mock
from mock import mock_open

from webbreaker.common.confighelper import Config
import os

try:
    import ConfigParser as configparser

    config = configparser.SafeConfigParser()
except ImportError:  # Python3
    import configparser

    config = configparser.ConfigParser()


@mock.patch('webbreaker.common.confighelper.Config.set_config')
@mock.patch('webbreaker.common.confighelper.Config.set_vars')
def test_config_init_variables(set_vars_mock, set_config_mock):
    set_vars_mock.return_value = None
    set_config_mock.return_value = None
    test_obj = Config()

    assert os.path.exists(test_obj.home)
    assert test_obj.install is None
    assert test_obj.config is None
    assert test_obj.etc is None
    assert test_obj.git is None
    assert test_obj.log is None
    assert test_obj.agent_json is None
    assert test_obj.secret is None
    assert set_config_mock.call_count == 1


@mock.patch('webbreaker.common.confighelper.Config.set_vars')
@mock.patch('webbreaker.common.confighelper.Config.set_config')
def test_set_path_no_install_success(set_config_mock, set_vars_mock):
    set_vars_mock.return_value = None
    set_config_mock.return_value = None
    result = Config().set_path(install=None)

    assert set_vars_mock.call_count == 1
    assert set_config_mock.call_count == 1
    assert result == 1


@mock.patch('webbreaker.common.confighelper.Config.set_vars')
@mock.patch('webbreaker.common.confighelper.Config.set_config')
def test_set_path_install_success(set_config_mock, set_vars_mock):
    set_vars_mock.return_value = None
    set_config_mock.return_value = None
    result = Config().set_path(install='/test/install')

    assert set_vars_mock.call_count == 1
    assert set_config_mock.call_count == 1
    assert result == 1


@mock.patch('webbreaker.common.confighelper.Config.set_vars')
@mock.patch('webbreaker.common.confighelper.Config.set_config')
@mock.patch('webbreaker.common.confighelper.os.makedirs')
@mock.patch('webbreaker.common.confighelper.open', new_callable=mock_open, read_data="data")
def test_set_path_dir_file_success(open_mock, makedirs_mock, set_config_mock, set_vars_mock):
    set_vars_mock.return_value = None
    set_config_mock.return_value = None

    result = Config().set_path(install='/test/install', dir_path='test_dir', file_name='test.file')

    assert makedirs_mock.call_count == 1
    assert open_mock.call_count == 1
    assert result == '/test/install/test_dir/test.file'


@mock.patch('webbreaker.common.confighelper.Config.set_vars')
@mock.patch('webbreaker.common.confighelper.Config.set_config')
@mock.patch('webbreaker.common.confighelper.os.makedirs')
@mock.patch('webbreaker.common.confighelper.open', new_callable=mock_open, read_data="data")
def test_set_path_dir_file_exception(open_mock, makedirs_mock, set_config_mock, set_vars_mock):
    set_vars_mock.return_value = None
    set_config_mock.return_value = None
    e = IOError("Test Error")
    open_mock.side_effect = e

    result = Config().set_path(install='/test/install', dir_path='test_dir', file_name='test.file')

    assert makedirs_mock.call_count == 1
    assert open_mock.call_count == 1
    assert result == 1


@mock.patch('webbreaker.common.confighelper.Config.set_vars')
@mock.patch('webbreaker.common.confighelper.Config.set_config')
@mock.patch('webbreaker.common.confighelper.os.path.exists')
@mock.patch('webbreaker.common.confighelper.os.makedirs')
@mock.patch('webbreaker.common.confighelper.open', new_callable=mock_open, read_data="data")
def test_set_path_dir_file_exists_dir(open_mock, makedirs_mock, exist_mock, set_config_mock, set_vars_mock):
    set_vars_mock.return_value = None
    set_config_mock.return_value = None
    exist_mock.return_value = True

    result = Config().set_path(install='/test/install', dir_path='test_dir', file_name='test.file')

    assert makedirs_mock.call_count == 0
    assert open_mock.call_count == 1
    assert result == '/test/install/test_dir/test.file'


@mock.patch('webbreaker.common.confighelper.Config.set_vars')
@mock.patch('webbreaker.common.confighelper.Config.set_config')
@mock.patch('webbreaker.common.confighelper.os.makedirs')
@mock.patch('webbreaker.common.confighelper.open', new_callable=mock_open, read_data="data")
def test_set_path_file_success(open_mock, makedirs_mock, set_config_mock, set_vars_mock):
    set_vars_mock.return_value = None
    set_config_mock.return_value = None

    result = Config().set_path(install='/test/install', file_name='test.file')

    assert makedirs_mock.call_count == 1
    assert open_mock.call_count == 1
    assert result == '/test/install/test.file'


@mock.patch('webbreaker.common.confighelper.Config.set_vars')
@mock.patch('webbreaker.common.confighelper.Config.set_config')
@mock.patch('webbreaker.common.confighelper.os.makedirs')
@mock.patch('webbreaker.common.confighelper.open', new_callable=mock_open, read_data="data")
def test_set_path_file_exception(open_mock, makedirs_mock, set_config_mock, set_vars_mock):
    set_vars_mock.return_value = None
    set_config_mock.return_value = None
    e = IOError("Test Error")
    open_mock.side_effect = e

    result = Config().set_path(install='/test/install', file_name='test.file')

    assert makedirs_mock.call_count == 1
    assert open_mock.call_count == 1
    assert result == 1


@mock.patch('webbreaker.common.confighelper.Config.set_vars')
@mock.patch('webbreaker.common.confighelper.Config.set_config')
@mock.patch('webbreaker.common.confighelper.os.path.exists')
@mock.patch('webbreaker.common.confighelper.os.makedirs')
@mock.patch('webbreaker.common.confighelper.open', new_callable=mock_open, read_data="data")
def test_set_path_file_exists_dir(open_mock, makedirs_mock, exist_mock, set_config_mock, set_vars_mock):
    set_vars_mock.return_value = None
    set_config_mock.return_value = None
    exist_mock.return_value = True

    result = Config().set_path(install='/test/install', file_name='test.file')

    assert makedirs_mock.call_count == 0
    assert open_mock.call_count == 1
    assert result == '/test/install/test.file'


@mock.patch('webbreaker.common.confighelper.Config.set_vars')
@mock.patch('webbreaker.common.confighelper.Config.set_config')
@mock.patch('webbreaker.common.confighelper.os.makedirs')
def test_set_path_dir_success(makedirs_mock, set_config_mock, set_vars_mock):
    set_vars_mock.return_value = None
    set_config_mock.return_value = None

    result = Config().set_path(install='/test/install', dir_path='test_dir')

    assert makedirs_mock.call_count == 1
    assert result == '/test/install/test_dir'


@mock.patch('webbreaker.common.confighelper.Config.set_vars')
@mock.patch('webbreaker.common.confighelper.Config.set_config')
@mock.patch('webbreaker.common.confighelper.os.path.exists')
@mock.patch('webbreaker.common.confighelper.os.makedirs')
@mock.patch('webbreaker.common.confighelper.open', new_callable=mock_open, read_data="data")
def test_set_path_exists(open_mock, makedirs_mock, exist_mock, set_config_mock, set_vars_mock):
    set_vars_mock.return_value = None
    set_config_mock.return_value = None
    exist_mock.return_value = True

    result = Config().set_path(install='/test/install', dir_path='test_dir')

    assert exist_mock.call_count == 1
    assert makedirs_mock.call_count == 0
    assert result == '/test/install/test_dir'


@mock.patch('webbreaker.common.confighelper.Config.conf_get')
@mock.patch('webbreaker.common.confighelper.Config.set_vars')
def test_set_config_basic(set_vars_mock, conf_get_mock):
    set_vars_mock.return_value = None
    conf_get_mock.return_value = None

    Config()

    assert conf_get_mock.call_count == 55


@mock.patch('webbreaker.common.confighelper.Config.set_vars')
@mock.patch('webbreaker.common.confighelper.Config.set_config')
@mock.patch('webbreaker.common.confighelper.config.read')
@mock.patch('webbreaker.common.confighelper.config.get')
def test_conf_get_success(get_mock, read_mock, set_config_mock, set_vars_mock):
    set_vars_mock.return_value = None
    set_config_mock.return_value = None
    read_mock.return_value = True
    get_mock.return_value = 'new_test_value'

    result = Config().conf_get('test_section', 'test_option', 'test_value')

    assert read_mock.call_count == 1
    assert get_mock.call_count == 1
    assert result == 'new_test_value'


@mock.patch('webbreaker.common.confighelper.Config.set_vars')
@mock.patch('webbreaker.common.confighelper.Config.set_config')
@mock.patch('webbreaker.common.confighelper.config.read')
@mock.patch('webbreaker.common.confighelper.config.add_section')
@mock.patch('webbreaker.common.confighelper.config.set')
@mock.patch('webbreaker.common.confighelper.config.write')
@mock.patch('webbreaker.common.confighelper.open', new_callable=mock_open, read_data="data")
def test_conf_get_section_exec(open_mock, write_mock, set_mock, add_mock, read_mock, set_config_mock, set_vars_mock):
    set_vars_mock.return_value = None
    set_config_mock.return_value = None
    e = configparser.NoSectionError("Test Error")
    read_mock.side_effect = e

    result = Config().conf_get('test_section', 'test_option', 'test_value')

    assert read_mock.call_count == 1
    assert add_mock.call_count == 1
    assert set_mock.call_count == 1
    assert open_mock.call_count == 1
    assert write_mock.call_count == 1
    assert result == 'test_value'


@mock.patch('webbreaker.common.confighelper.Config.set_vars')
@mock.patch('webbreaker.common.confighelper.Config.set_config')
@mock.patch('webbreaker.common.confighelper.config.read')
@mock.patch('webbreaker.common.confighelper.config.set')
@mock.patch('webbreaker.common.confighelper.config.write')
@mock.patch('webbreaker.common.confighelper.open', new_callable=mock_open, read_data="data")
def test_conf_get_option_exec(open_mock, write_mock, set_mock, read_mock, set_config_mock, set_vars_mock):
    set_vars_mock.return_value = None
    set_config_mock.return_value = None
    e = configparser.NoOptionError("Test Error", "Error Section")
    read_mock.side_effect = e

    result = Config().conf_get('test_section', 'test_option', 'test_value')

    assert read_mock.call_count == 1
    assert set_mock.call_count == 1
    assert open_mock.call_count == 1
    assert write_mock.call_count == 1
    assert result == 'test_value'
