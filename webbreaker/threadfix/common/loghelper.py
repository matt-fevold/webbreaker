#!/usr/bin/env python
# -*- coding: utf-8 -*-

from webbreaker.common.webbreakerlogger import Logger


class ThreadFixLogHelper(object):

    def __init__(self):
        pass

    def log_error_no_team_with_name(self, args):
        Logger.app.error("Unable to find team with name {}".format(args))

    def log_error_no_team(self):
        Logger.app.error("No teams were found")

    def log_error_retrieving_application(self, args):
        Logger.app.error("Error retrieving application for team {}".format(args))

    def log_error_specify_team(self):
        Logger.app.error("Please specify either a team or team_id")

    def log_error_no_team_with_application(self, args):
        Logger.app.error("Unable to find team with application {}".format(args))

    def log_error_api_token_associated_with_local_account(self):
        Logger.app.error("Possible cause could be your API token must be associated with a local account!!")

    def log_error_no_scans_found_with_app_id(self, args):
        Logger.app.error("No scans were found for app_id {}".format(args))

    def log_error_request_download(self, args):
        Logger.app.error("Error requesting download: {}".format(args))

    def log_error_reading(self, args, e):
        Logger.app.error("Error reading {} {}".format(args, e))

    def log_error_specify_application(self, args):
        Logger.app.error("Please specify either an application or app_id! {}".format(args))

    def log_error_threadfix_retrieve_fail(self):
        Logger.app.error("Failed to retrieve applications from ThreadFix")

    def log_error_multiple_application_found(self, args):
        Logger.app.error("Multiple applications were found matching name {}. "
                         "Please specify the desired ID from below.".format(args))


     # info
    def log_info_find_application_with_matching_name(self, args):
        Logger.app.info("Attempting to find application matching name {}".format(args))

    def log_info_application_created_with_id(self, args):
        Logger.app.info("Application was successfully created with id {}".format(args))

    def log_info_threadfix_list_success(self):
        Logger.app.info("ThreadFix List successfully completed")

    def log_info_no_application_found(self, args):
        Logger.app.info("No applications were found" + args)

    def log_info_threadfix_scans_listed_success(self):
        Logger.app.info("Successfully listed Threadfix scans")

    def log_info_threadfix_teams_listed_success(self):
        Logger.app.info("Successfully listed threadfix teams")

    def log_info_upload_response(self, args):
        Logger.app.info("{}".format(args))


