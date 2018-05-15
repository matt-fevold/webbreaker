#!/usr/bin/env python
# -*- coding: utf-8 -*-

from webbreaker.common.webbreakerlogger import Logger


class FortifyLogHelper(object):

    def __init__(self):
        pass

    # ERROR
    def log_error_can_not_open_or_write_to_file(self, e):
        Logger.app.error("Couldn't open or write to file {}.".format(e))

    def log_error_no_version_match_under_application_name(self, args, application_name):
        Logger.app.error("No version matching {} found under {} in Fortify".format(args, application_name))

    def log_error_file_incorrect_value(self, args, noe):
        Logger.app.error("{} has incorrect or missing values {}".format(args, noe))

    def log_error_reading(self, args, e):
        Logger.app.error("Error reading {} {}".format(args, e))

    def log_error_invalid_ssl(self):
        Logger.app.error("'verify_ssl' must be either 'False' or a full valid CA Path.")

    def log_error_duplicate_ssc_project_versioin(self):
        Logger.app.error("There are duplicate Fortify SSC Project Version names.  Please choose another one.")

    def log_error_api_token(self):
        Logger.app.error("Unable to obtain a Fortify API token. Invalid Credentials")

    def log_error_unable_to_create_project_version(self):
        Logger.app.error("Unable to create new project version, see logs for details")

    def log_error_scan_download_version_fail(self, args):
        Logger.app.error("Scan download for version {} has failed".format(args))

    def log_error_credentials_not_stored(self):
        Logger.app.error("Unable to validate Fortify credentials. Credentials were not stored")


    # INFO
    def log_info_version_successful_written_to_file(self, args, filename):
        Logger.app.info("Scan file for version {} successfully written to {}".format(args, filename))

    def log_info_check_config(self):
        Logger.app.info("No Fortify username or password provided. Checking config.ini for credentials")

    def log_info_import_credentials(self):
        Logger.app.info("Importing Fortify credentials")

    def log_info_credentials_found_in_config(self):
        Logger.app.info("Fortify username and password successfully found in config.ini")

    def log_info_credential_not_found(self):
        Logger.app.info("Fortify credentials not found in config.ini")

    def log_info_list_success(self):
        Logger.app.info("Fortify list has successfully completed")

    def log_info_found_existing_application_version(self, args, version_name):
        Logger.app.info("Found existing Application Version '{} : {}'.".format(args, version_name))

    def log_info_file_uploaded_success(self, file_name, fortify_extension, fortify_url):
        Logger.app.info(
            "Your scan file {0}.{1}, has been successfully uploaded to {2}!".format(file_name, fortify_extension,
                                                                                    fortify_url))

    def log_info_credentials_clear_success(self):
        Logger.app.info("Successfully cleared fortify credentials from config.ini")

    def log_info_credential_stored(self):
        Logger.app.info("Fortify credentials stored")