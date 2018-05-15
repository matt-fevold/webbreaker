#!/usr/bin/env python
# -*- coding: utf-8 -*-

from webbreaker.common.webbreakerlogger import Logger


# Okay - this will not look nice future person reading this. This needs to be fixed again after we
#   get our testing in a nicer spot - currently some tests check for logging output (not anything we've refactored
#   recently (~2.1.5)) but those will change as more work is done. TODO


# TODO need to move threadfix logger out into its own file similar to webinspect and fortify after refactoring is done on threadfix (Hayley)

class LogExceptionHelper(object):

    def __init__(self):
        pass

    #__main__
    def log_error_git_command(self, args):
        Logger.app.error("Please install the git client or add it to your PATH variable ->"
                         " https://git-scm.com/download.  See log {}!!!".format(args))

    #ThreadFix
    def log_error_no_team(self):
        Logger.app.error("No teams were found")

    def log_error_no_team_with_name(self, args):
        Logger.app.error("Unable to find team with name {}".format(args))

    def log_error_specify_team(self):
        Logger.app.error("Please specify either a team or team_id")

    def log_error_no_application_with_team_id(self, args):
        Logger.app.error("No applications were found for team_id {}".format(args))

    def log_error_no_team_with_application(self, args):
        Logger.app.error("Unable to find team with application {}".format(args))

    def log_error_application_not_created(self):
        Logger.app.error("Application was not created, either the application exists, invalid token, or Threadfix"
                         " is unavailable!! ")

    def log_error_threadfix_response(self, args):
        Logger.app.error("{}\n".format(args) + "Threadfix exited")

    def log_error_reading(self, args, e):
        Logger.app.error("Error reading {} {}".format(args, e))

    def log_error_retrieving_application(self, args):
        Logger.app.error("Error retrieving application for team {}".format(args))

    def log_error_request_download(self, args):
        Logger.app.error("Error requesting download: {}".format(args))

    def log_error_no_scans_found_with_app_id(self, args):
        Logger.app.error("No scans were found for app_id {}".format(args))

    def log_error_specify_application(self, args):
        Logger.app.error("Please specify either an application or app_id! {}".format(args))

    def log_error_threadfix_retrieve_fail(self):
        Logger.app.error("Failed to retrieve applications from ThreadFix")

    def log_error_no_application_with_matching_name(self, args):
        Logger.app.error("No application was found matching name {}".format(args))

    def log_error_multiple_application_found(self, args):
        Logger.app.error("Multiple applications were found matching name {}. "
                         "Please specify the desired ID from below.".format(args))

    def log_error_scan_fail_to_uplaod(self):
        Logger.app.error("Scan file failed to upload!")

    def log_error_api_token_associated_with_local_account(self):
        Logger.app.error("Possible cause could be your API token must be associated with a local account!!")


class LogInfoHelper(object):

    def __init__(self):
        pass

    #__main__
    def log_info_credentials_store_success(self):
        Logger.app.info("Credentials stored successfully")

    def log_info_webinspect_credential_clear_success(self):
        Logger.app.info("Successfully cleared WebInspect credentials from config.ini")

    def log_info_application_created_with_id(self, args):
        Logger.app.info("Application was successfully created with id {}".format(args))

    #Threadfix
    def log_info_threadfix_scans_listed_success(self):
        Logger.app.info("Successfully listed Threadfix scans")

    def log_info_find_application_with_matching_name(self, args):
        Logger.app.info("Attempting to find application matching name {}".format(args))

    def log_info_upload_response(self, args):
        Logger.app.info("{}".format(args))

    def log_info_threadfix_list_success(self):
        Logger.app.info("ThreadFix List successfully completed")

    def log_info_no_application_found(self, args):
        Logger.app.info("No applications were found" + args)

    def log_info_threadfix_application_list_success(self):
        Logger.app.info("Successfully listed threadfix applications")

    def log_info_threadfix_teams_listed_success(self):
        Logger.app.info("Successfully listed threadfix teams")
