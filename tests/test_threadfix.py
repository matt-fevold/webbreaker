import pytest
import mock
import logging

from testfixtures import LogCapture
from webbreaker.__main__ import cli as webbreaker

# Disable debugging for log clarity in testing
logging.disable(logging.DEBUG)


@pytest.fixture(scope="module")
def runner():
    from click.testing import CliRunner
    return CliRunner()


@pytest.fixture()
def caplog():
    return LogCapture()


@mock.patch('webbreaker.__main__.ThreadFixClient')
def test_threadfix_teams(test_mock, runner, caplog):
    test_mock.return_value.list_teams.return_value = [
        {"id": 123,
         "name": 'Marketing'
         },
        {"id": 456,
         "name": 'InfoSec'
         },
        {"id": 789,
         "name": 'Branding'
         },
        {"id": 1011,
         "name": 'Development'
         }
    ]
    test_mock.list_teams()

    result = runner.invoke(webbreaker, ['threadfix', 'teams'])

    caplog.check(
        ('__webbreaker__', 'INFO', 'Successfully listed threadfix teams'),
    )
    caplog.uninstall()

    assert """    ID     Name                          
---------- ------------------------------
   123     Marketing                     
   456     InfoSec                       
   789     Branding                      
   1011    Development   """ in result.output
    assert result.exit_code == 0


@mock.patch('webbreaker.__main__.ThreadFixClient')
def test_threadfix_teams_none(test_mock, runner, caplog):
    test_mock.return_value.list_teams.return_value = None
    test_mock.list_teams()

    result = runner.invoke(webbreaker, ['threadfix', 'teams'])

    caplog.check(
        ('__webbreaker__', 'ERROR', 'No teams were found'),
    )
    caplog.uninstall()

    assert result.exit_code == 0


@mock.patch('webbreaker.__main__.ThreadFixClient')
def test_threadfix_applications(test_mock, runner, caplog):
    test_mock.return_value.list_apps_by_team.return_value = [
        {"id": 987,
         "name": 'Super Secret Marketing App'
         },
        {"id": 654,
         "name": 'Less Secretive Marketing App'
         },
        {"id": 321,
         "name": 'Blatant Marketing App'
         }
    ]
    test_mock.list_apps_by_team()

    result = runner.invoke(webbreaker, ['threadfix', 'applications', '--team_id', 123])

    caplog.check(
        ('__webbreaker__', 'INFO', 'Successfully listed threadfix applications'),
    )
    caplog.uninstall()

    assert """    ID     Name                          
---------- ------------------------------
   987     Super Secret Marketing App    
   654     Less Secretive Marketing App  
   321     Blatant Marketing App """ in result.output
    assert result.exit_code == 0


@mock.patch('webbreaker.__main__.ThreadFixClient')
def test_threadfix_applications_none(test_mock, runner, caplog):
    test_mock.return_value.list_apps_by_team.return_value = None
    test_mock.list_apps_by_team()

    result = runner.invoke(webbreaker, ['threadfix', 'applications', '--team_id', 123])

    caplog.check(
        ('__webbreaker__', 'ERROR', 'No applications were found for team_id 123'),
    )
    caplog.uninstall()

    assert result.exit_code == 0


@mock.patch('webbreaker.__main__.ThreadFixClient')
def test_threadfix_scans(test_mock, runner, caplog):
    test_mock.return_value.list_scans_by_app.return_value = [
        {"id": 246,
         "scannerName": 'Burp Suite',
         "filename": 'blatant_marketing_app.xml'
         },
        {"id": 135,
         "scannerName": 'WebInspect',
         "filename": 'blatant_marketing_app_dyn.xml'
         },
        {"id": 112,
         "scannerName": 'Manual',
         "filename": 'matt_blatant_app.xml'
         },
    ]
    test_mock.list_scans_by_app()

    result = runner.invoke(webbreaker, ['threadfix', 'scans', '--app_id', 321])

    caplog.check(
        ('__webbreaker__', 'INFO', 'Successfully listed threadfix scans'),
    )
    caplog.uninstall()

    assert """    ID     Scanner Name                   Filename                      
---------- ------------------------------ ------------------------------
   246     Burp Suite                     blatant_marketing_app.xml     
   135     WebInspect                     blatant_marketing_app_dyn.xml 
   112     Manual                         matt_blatant_app.xml""" in result.output
    assert result.exit_code == 0


@mock.patch('webbreaker.__main__.ThreadFixClient')
def test_threadfix_scans_none(test_mock, runner, caplog):
    test_mock.return_value.list_scans_by_app.return_value = None
    test_mock.list_scans_by_app()

    result = runner.invoke(webbreaker, ['threadfix', 'scans', '--app_id', 321])

    caplog.check(
        ('__webbreaker__', 'ERROR', 'No scans were found for app_id 321'),
    )
    caplog.uninstall()

    assert result.exit_code == 0


@mock.patch('webbreaker.__main__.ThreadFixClient')
def test_threadfix_create_app(test_mock, runner, caplog):
    test_mock.return_value.create_application.return_value = {"id": 666}
    test_mock.create_application()

    result = runner.invoke(webbreaker, ['threadfix', 'create_app', '--team_id', 456, '--name', 'New Secret App',
                                        '--url', 'https://github.com/target/webbreaker'])

    caplog.check(('__webbreaker__', 'INFO', 'Application successfully created with id 666'), )
    caplog.uninstall()

    assert result.exit_code == 0


@mock.patch('webbreaker.__main__.ThreadFixClient')
def test_threadfix_upload_success(test_mock, runner, caplog):
    test_mock.return_value.upload_scan.return_value = "Upload process has begun."
    test_mock.upload_scan()

    result = runner.invoke(webbreaker, ['threadfix', 'upload', '--app_id', 666, '--scan_file', 'kyler_secret_scan.xml'])

    caplog.check(('__webbreaker__', 'INFO', 'Upload process has begun.'), )
    caplog.uninstall()

    assert result.exit_code == 0


@mock.patch('webbreaker.__main__.ThreadFixClient')
def test_threadfix_upload_failure(test_mock, runner, caplog):
    test_mock.return_value.upload_scan.return_value = None
    test_mock.upload_scan()

    result = runner.invoke(webbreaker, ['threadfix', 'upload', '--app_id', 666, '--scan_file', 'kyler_secret_scan.xml'])

    caplog.check(('__webbreaker__', 'ERROR', 'Scan file failed to upload'), )
    caplog.uninstall()

    assert result.exit_code == 0

@mock.patch('webbreaker.__main__.ThreadFixClient')
def test_threadfix_upload_success(test_mock, runner, caplog):
    test_mock.return_value.upload_scan.return_value = "Upload process has begun."
    test_mock.upload_scan()

    result = runner.invoke(webbreaker, ['threadfix', 'upload', '--app_id', 666, '--scan_file', 'kyler_secret_scan.xml'])

    caplog.check(('__webbreaker__', 'INFO', 'Upload process has begun.'), )
    caplog.uninstall()

    assert result.exit_code == 0

@mock.patch('webbreaker.__main__.ThreadFixClient')
def test_threadfix_list_success(test_mock, runner, caplog):
    test_mock.return_value.list_all_apps.return_value = [
                                                        {
                                                          'team_name': 'Marketing',
                                                          'app_id': 123,
                                                          'app_name': 'Secret App'
                                                        },
                                                        {
                                                          'team_name': 'AppSec',
                                                          'app_id': 456,
                                                          'app_name': 'Buggy App'
                                                        }]
    test_mock.list_all_apps()

    result = runner.invoke(webbreaker, ['threadfix', 'list'])

    caplog.check(
        ('__webbreaker__', 'INFO', 'ThreadFix List successfully completed'),
    )
    caplog.uninstall()

    assert '123' in result.output
    assert 'Marketing' in result.output
    assert 'Secret App' in result.output

    assert '456' in result.output
    assert 'AppSec' in result.output
    assert 'Buggy App' in result.output

    assert result.exit_code == 0


@mock.patch('webbreaker.__main__.ThreadFixClient')
def test_threadfix_list_failure(test_mock, runner, caplog):
    test_mock.return_value.list_all_apps.return_value = False
    test_mock.list_all_apps()

    result = runner.invoke(webbreaker, ['threadfix', 'list'])

    caplog.check(('__webbreaker__', 'ERROR', 'Possible cuase could be your API token must be associated with a local account account!!'), )
    caplog.uninstall()

    assert result.exit_code == 0


@mock.patch('webbreaker.__main__.ThreadFixClient')
def test_threadfix_list_empty(test_mock, runner, caplog):
    test_mock.return_value.list_all_apps.return_value = []
    test_mock.list_all_apps()

    result = runner.invoke(webbreaker, ['threadfix', 'list'])

    caplog.check(('__webbreaker__', 'INFO', 'No applications were found'), )
    caplog.uninstall()

    assert result.exit_code == 0

@mock.patch('webbreaker.__main__.ThreadFixClient')
def test_threadfix_list_empty_query(test_mock, runner, caplog):
    test_mock.return_value.list_all_apps.return_value = []
    test_mock.list_all_apps()

    result = runner.invoke(webbreaker, ['threadfix', 'list', '--team', 'Security', '--application', 'Extra Super Secret App'])

    caplog.check(('__webbreaker__', 'INFO', 'No applications were found with team name matching Security and application name matching Extra Super Secret App'), )
    caplog.uninstall()

    assert result.exit_code == 0

