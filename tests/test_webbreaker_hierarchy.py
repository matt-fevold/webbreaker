import pytest
from webbreaker.__main__ import cli as webbreaker


@pytest.fixture(scope="module")
def runner():
    from click.testing import CliRunner
    return CliRunner()


def test_main_hierarchy(runner):
    result = runner.invoke(webbreaker)
    assert result.exit_code == 0

    result = runner.invoke(webbreaker, ['webinspect'])
    assert result.exit_code == 0

    result = runner.invoke(webbreaker, ['fortify'])
    assert result.exit_code == 0

    result = runner.invoke(webbreaker, ['admin'])
    assert result.exit_code == 0

    result = runner.invoke(webbreaker, ['threadfix'])
    assert result.exit_code == 0


def test_webinspect_hierarchy(runner):
    result = runner.invoke(webbreaker, ['webinspect', 'download', '--help'])
    assert result.exit_code == 0

    result = runner.invoke(webbreaker, ['webinspect', 'list', '--help'])
    assert result.exit_code == 0

    result = runner.invoke(webbreaker, ['webinspect', 'scan', '--help'])
    assert result.exit_code == 0

    result = runner.invoke(webbreaker, ['webinspect', 'servers', '--help'])
    assert result.exit_code == 0


def test_fortify_hierarchy(runner):
    result = runner.invoke(webbreaker, ['fortify', 'list', '--help'])
    assert result.exit_code == 0

    result = runner.invoke(webbreaker, ['fortify', 'scan', '--help'])
    assert result.exit_code == 0

    result = runner.invoke(webbreaker, ['fortify', 'upload', '--help'])
    assert result.exit_code == 0

    result = runner.invoke(webbreaker, ['fortify', 'download', '--help'])
    assert result.exit_code == 0


def test_admin_hierarchy(runner):
    result = runner.invoke(webbreaker, ['admin', 'agent', '--help'])
    assert result.exit_code == 0

    result = runner.invoke(webbreaker, ['admin', 'credentials', '--help'])
    assert result.exit_code == 0

    result = runner.invoke(webbreaker, ['admin', 'notifier', '--help'])
    assert result.exit_code == 0

def test_threadfix_hierarchy(runner):
    result = runner.invoke(webbreaker, ['threadfix', 'teams', '--help'])
    assert result.exit_code == 0

    result = runner.invoke(webbreaker, ['threadfix', 'applications', '--help'])
    assert result.exit_code == 0

    result = runner.invoke(webbreaker, ['threadfix', 'scans', '--help'])
    assert result.exit_code == 0

    result = runner.invoke(webbreaker, ['threadfix', 'upload', '--help'])
    assert result.exit_code == 0

    result = runner.invoke(webbreaker, ['threadfix', 'create_app', '--help'])
    assert result.exit_code == 0

    result = runner.invoke(webbreaker, ['threadfix', 'list', '--help'])
    assert result.exit_code == 0
