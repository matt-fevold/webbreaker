import pytest
from webbreaker.__main__ import fortify


@pytest.fixture(scope="module")
def runner():
    from click.testing import CliRunner
    return CliRunner()


# def test_fortify_list(runner):
#     result = runner.invoke(fortify, ['list'])
#     assert result.exit_code == -1


# def test_fortify_list_user(runner):
#     result = runner.invoke(fortify, ['list'])
#     assert result.exit_code == 0
#
#
# def test_fortify_list_password(runner):
#     result = runner.invoke(fortify, ['list'])
#     assert result.exit_code == 0


# def test_fortify_list_user_password(runner):
#     result = runner.invoke(fortify, ['list', '--fortify_user', '--fortify_password'])
#     assert result.exit_code == -1


# def test_fortify_list_application(runner):
#     result = runner.invoke(fortify, ['list'])
#     assert result.exit_code == 0
#
#
# def test_fortify_upload(runner):
#     result = runner.invoke(fortify, ['upload'])
#     assert result.exit_code == 0
#
#
# def test_fortify_upload_required(runner):
#     result = runner.invoke(fortify, ['upload', '--version'])
#     assert result.exit_code == 0
#
#
# def test_fortify_upload_user(runner):
#     result = runner.invoke(fortify, ['upload', '--fortify_user'])
#     assert result.exit_code == 0
#
#
# def test_fortify_upload_password(runner):
#     result = runner.invoke(fortify, ['upload', '--fortify_password'])
#     assert result.exit_code == 0
#
#
# def test_fortify_upload_user_password(runner):
#     result = runner.invoke(fortify, ['upload', '--fortify_user', '--fortify_password'])
#     assert result.exit_code == 0
#
#
# def test_fortify_upload_app(runner):
#     result = runner.invoke(fortify, ['upload', '--application'])
#     assert result.exit_code == 0
#
#
# def test_fortify_upload_scan_name(runner):
#     result = runner.invoke(fortify, ['upload', '--scan_name'])
#     assert result.exit_code == 0
#
#
# def test_fortify_upload_version(runner):
#     result = runner.invoke(fortify, ['upload', '--version'])
#     assert result.exit_code == 0
#
#
# def test_fortify_scan(runner):
#     result = runner.invoke(fortify, ['scan'])
#     assert result.exit_code == 0
#
#
# def test_fortify_scan_required(runner):
#     result = runner.invoke(fortify, ['scan', '--version', '--build_id'])
#     assert result.exit_code == 0
#
#
# def test_fortify_scan_user(runner):
#     result = runner.invoke(fortify, ['scan', '--fortify_user'])
#     assert result.exit_code == 0
#
#
# def test_fortify_scan_password(runner):
#     result = runner.invoke(fortify, ['scan', '--fortify_password'])
#     assert result.exit_code == 0
#
#
# def test_fortify_scan_user_password(runner):
#     result = runner.invoke(fortify, ['scan', '--fortify_user', '--fortify_password'])
#     assert result.exit_code == 0
#
#
# def test_fortify_scan_app(runner):
#     result = runner.invoke(fortify, ['scan', '--application'])
#     assert result.exit_code == 0
#
#
# def test_fortify_scan_version(runner):
#     result = runner.invoke(fortify, ['scan', '--version'])
#     assert result.exit_code == 0
#
#
# def test_fortify_scan_build_id(runner):
#     result = runner.invoke(fortify, ['scan', '--build_id'])
#     assert result.exit_code == 0