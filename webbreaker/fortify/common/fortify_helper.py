#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import socket
import sys

from exitstatus import ExitStatus
from webbreaker.common.webbreakerhelper import WebBreakerHelper
from webbreaker.common.webbreakerlogger import Logger
from fortifyapi.fortify import FortifyApi
from webbreaker.common.api_response_helper import APIHelper
from webbreaker.common.logexceptionhelper import LogExceptionHelper

logexceptionhelper = LogExceptionHelper()


class FortifyClient(object):
    def __init__(self, fortify_url, fortify_username, fortify_password):
        # Static
        self.extension = 'fpr'

        # Required Globals
        self.fortify_url = fortify_url
        self.username = fortify_username
        self.password = fortify_password
        self.runenv = WebBreakerHelper.check_run_env()
        self.api = self._setup_fortify_ssc_api()

    def download_scan(self, application_name, version_name):
        version_id = self._get_version_id(application_name, version_name)

        if version_id:
            response, file_name = self.api.download_artifact_scan(version_id)

            if response.success:
                file_content = response.data
                with open(file_name, 'wb') as f:
                    f.write(file_content)
                Logger.app.info("Scan file for version {} successfully written to {}".format(version_id, file_name))
            else:
                Logger.app.error("Error downloading scan file: {}".format(response.message))
                sys.exit(ExitStatus.failure)

        else:
            Logger.app.error(
                "No version matching {} found under {} in Fortify".format(version_name, application_name))
            sys.exit(ExitStatus.failure)

    def list_application_versions(self, application_name):
        response = self.api.get_all_project_versions()
        APIHelper().check_for_response_errors(response)

        print("{0:^8} {1:30} {2:30}".format('ID', 'Application', 'Version'))
        print("{0:8} {1:30} {2:30}".format('-' * 8, '-' * 30, '-' * 30))
        for version in response.data['data']:
            if application_name is None or application_name == version['project']['name']:
                print("{0:8} {1:30} {2:30}".format(version['id'], version['project']['name'], version['name']))
        Logger.app.info("Fortify list has successfully completed")

    def upload_scan(self, application_name, version_name, project_template, file_name):
        """
        If the Application & Version already exists, do nothing.
        If the Application exists but NOT Version, upload (create) a new Version.
        If the Application doesn't exist, log and exit with error code.
        :param application_name:
        :param version_name:
        :param project_template:
        :param file_name: Scan name to upload. It will be appended with '.fpr' to create the filename
        :return: Nothing
        """
        try:
            file_name = self._trim_ext(file_name)
            application_id = self._get_application_id(application_name)

            # An Application was found matching application_name
            if application_id:
                version_id = self._get_version_id(application_name, version_name)

                # Application & Version where found. Unable to Upload.
                if version_id:
                    Logger.app.error(
                        "Found existing Application Version {}: {}. Unable to upload.".format(application_name,
                                                                                              version_name))

                # Application was found, but no Version. Upload new Version.
                else:
                    self._upload_new_version(application_name, application_id, version_name, project_template,
                                             file_name)

            # No Application was found matching application_name. Unable to Upload.
            else:
                application_id = self._create_new_application(application_name)
                self._upload_new_version(application_name, application_id, version_name, project_template, file_name)
                # TODO: Remove after `_create_new_application` actually creates new Application
                sys.exit(ExitStatus.failure)
        except UnboundLocalError as e:
            Logger.app.critical("Exception trying to create SSC project version: {}".format(e))

    def _get_application_id(self, application_name):
        """
        Returns the ID of the specified Application. Project is a deprecated name for Application.
        :return: ID of the Application
        """
        response = self.api.get_projects()
        APIHelper().check_for_response_errors(response)

        for application in response.data['data']:
            if application['name'] == application_name:
                return application['id']
        return None

    def _get_version_id(self, application_name, version_name):
        """
        Returns the ID of the specified Application. Project is a deprecated name for Application
        :return: ID of the Version
        """
        response = self.api.get_all_project_versions()
        APIHelper().check_for_response_errors(response)

        for version in response.data['data']:
            if version['project']['name'] == application_name:
                if version['name'] == version_name:
                    return version['id']
        return False

    # TODO: Create a new Application.
    def _create_new_application(self, application_name):
        """
        Create a new Application through FortifyAPI after confirming it does not already exist.
        Currently waiting on Fortify to fix their REST API to allow creating Applications.
        :return: Application ID of the newly created Application
        """
        Logger.app.error(
            "Fortify Application: {} does not exist. Please use a valid Application and re-upload scan.".format(
                application_name))
        # TODO: Remove when new Application is created
        return -1

    def _upload_new_version(self, application_name, application_id, version_name, project_template, file_name):
        """
        Create, add required attributes to, and commit a new project version
        :return: The new project_version_id if successful. Otherwise, None.
        """
        response = self.api.create_project_version(project_name=application_name,
                                                   project_id=application_id,
                                                   project_template=project_template,
                                                   version_name=version_name,
                                                   description=self._project_version_description())
        APIHelper().check_for_response_errors(response)

        version_id = response.data['data']['id']

        # At Target, only one attribute is required
        response = self.api.add_project_version_attribute(project_version_id=version_id,
                                                          # TODO: REPLACE
                                                          attribute_definition_id=self._get_attribute_definition_id(
                                                              search_expression='name:"CI Number"'),
                                                          value='New WebBreaker Application',
                                                          values=[])
        APIHelper().check_for_response_errors(response)

        response = self.api.commit_project_version(project_version_id=version_id)
        APIHelper().check_for_response_errors(response)

        Logger.app.info(
            "Your scan file {0}.{1}, has been successfully uploaded to {2}!".format(file_name, self.extension,
                                                                                    self.fortify_url))

    def _project_version_description(self):
        # TODO: Convert to config.ini configuration
        if self.runenv == "jenkins":
            return "WebInspect scan from WebBreaker " + os.getenv('JOB_URL', "jenkins server")
        else:
            return "WebBreaker scan from WebBreaker host " + socket.getfqdn()

    def _get_attribute_definition_id(self, search_expression):
        response = self.api.get_attribute_definition(search_expression=search_expression)
        if response.success:
            return response.data['data'][0]['id']
        else:
            return None

    def _setup_fortify_ssc_api(self):
        try:
            api = FortifyApi(self.fortify_url, username=self.username, password=self.password, verify_ssl=False)

            response = api.get_token()
            APIHelper().check_for_response_errors(response)

            return FortifyApi(self.fortify_url, token=response.data['data']['token'], verify_ssl=False)

        # TODO: Remove general exception handling
        except Exception as e:
            if hasattr(e, 'message'):
                Logger.app.critical("Exception while getting Fortify token: {0}".format(e.message))

        return None

    @staticmethod
    def _trim_ext(file):
        try:
            return os.path.splitext(os.path.basename(file))[0]
        except (TypeError, AttributeError):
            return file
