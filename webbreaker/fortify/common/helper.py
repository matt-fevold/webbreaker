#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import socket
import sys

from fortifyapi.fortify import FortifyApi
from exitstatus import ExitStatus
from webbreaker.common.api_response_helper import APIHelper
from webbreaker.fortify.config import FortifyConfig
from webbreaker.common.webbreakerhelper import WebBreakerHelper
from webbreaker.common.webbreakerlogger import Logger


class FortifyHelper(object):
    def __init__(self, fortify_url, fortify_username, fortify_password):
        # Static
        self.extension = 'fpr'

        # Required Globals
        self.fortify_url = fortify_url
        self.username = fortify_username
        self.password = fortify_password

        self.runenv = WebBreakerHelper.check_run_env()
        self.api = self._setup_fortify_ssc_api()
        self.config = FortifyConfig()

    def download_scan(self, application_name, version_name):
        """
        Downloads a scan with matching Application name & Version name.
        :param application_name: Required. Application to search for the Version under.
        :param version_name: The Version to download.
        """
        version_id = self._get_version_id(application_name, version_name)

        if version_id:
            file_content, file_name = self._download_version(version_id)
            with open(file_name, 'wb') as f:
                f.write(file_content)
            Logger.app.info("Scan file for version {} successfully written to {}".format(version_id, file_name))
        else:
            Logger.app.error(
                "No version matching {} found under {} in Fortify".format(version_name, application_name))
            sys.exit(ExitStatus.failure)

    def list_application_versions(self, application_name):
        """
        List all Applications & Versions from the Fortify URL unless application_name is supplied (Not None).
        :param application_name: If Application name is specified, only list versions for that Application
        """
        response_data = self._get_applications_and_versions()

        print("{0:^8} {1:30} {2:30}".format('ID', 'Application', 'Version'))
        print("{0:8} {1:30} {2:30}".format('-' * 8, '-' * 30, '-' * 30))
        for version in response_data:
            if application_name is None or application_name == version['project']['name']:
                print("{0:8} {1:30} {2:30}".format(version['id'], version['project']['name'], version['name']))

        Logger.app.info("Fortify list has successfully completed")

    def upload_scan(self, application_name, version_name, project_template, file_name):
        """
        If the Application & Version already exists, log and exit with error.
        Else upload (create) a new Version. If Application doesn't exist, create it.
        Then upload file to Application Version.
        :param application_name: Name of the Application for Upload.
        :param version_name: Name of the Version for Upload
        :param project_template: Project Template GUID from config.ini
        :param file_name: Scan name to upload. It will be appended with '.fpr' to create the filename
        """
        file_name = self._trim_ext(file_name)
        version_description = self._project_version_description()
        application_id = self._get_application_id(application_name)

        if application_id is not None:
            if self._get_version_id(application_name, version_name):
                Logger.app.error(
                    "Found existing Application Version '{} : {}'. Unable to upload.".format(application_name,
                                                                                             version_name))
                sys.exit(ExitStatus.failure)
            # Application exists but not Version
            else:
                version_id = self._create_version(application_name=application_name,
                                                  application_id=application_id,
                                                  version_name=version_name,
                                                  application_template=project_template,
                                                  version_description=version_description)
        # Application & Version do not exist
        else:
            version_id = self._create_application_and_version(application_name=application_name,
                                                              version_name=version_name,
                                                              application_template=project_template,
                                                              version_description=version_description)
        # Upload File to Application Version
        self._upload_application_version_file(version_id=version_id,
                                              file_name=file_name)
        Logger.app.info(
            "Your scan file {0}.{1}, has been successfully uploaded to {2}!".format(file_name, self.extension,
                                                                                    self.fortify_url))

    def _commit_version(self, version_id):
        """
        Commit a Version to Fortify. Necessary step when creating new Versions OR uploading new attributes.
        :param version_id: Version ID to commit.
        """
        response = self.api.commit_project_version(project_version_id=version_id)
        APIHelper().check_for_response_errors(response)

    def _create_application_and_version(self, application_name, version_name,
                                        application_template, version_description):
        """
        Creates a new Application Version.
        :param application_name: Name of the Application to put the Version under.
        :param version_name: Name of the Version to create.
        :param application_template: Brought in from the config.ini during the FortifyUpload Class __init__
        :param version_description: Version description for Application Version
        :return: Version ID of the newly created Version.
        """

        # Initial call to create a new Project Version
        response = self.api.create_new_project_version(application_name=application_name,
                                                       application_template=application_template,
                                                       version_name=version_name,
                                                       description=version_description)
        APIHelper().check_for_response_errors(response)
        version_id = response.data['data']['id']

        # Second call to create a new Project Version
        response = \
            self.api.bulk_create_new_application_request(version_id=version_id,
                                                         development_phase=self.config.development_phase,
                                                         development_strategy=self.config.development_strategy,
                                                         accessibility=self.config.accessibility,
                                                         business_risk_ranking=self.config.business_risk_ranking,
                                                         custom_attribute=self.config.custom_attribute
                                                         )
        APIHelper().check_for_response_errors(response)
        return version_id

    def _create_version(self, application_name, application_id,
                        version_name, application_template, version_description):
        """
        Creates a new Version under the specified Application ID.
        :param application_name: Name of the Application to put the Version under.
        :param application_id: ID of the Application. If None, creates a new Application with the application_name.
        :param version_name: Name of the Version to create.
        :param application_template: Brought in from the config.ini during the FortifyUpload Class __init__
        :param version_description: Version description for Application Version
        :return: Version ID of the newly created Version.
        """

        response = self.api.create_project_version(project_name=application_name,
                                                   project_id=application_id,
                                                   project_template=application_template,
                                                   version_name=version_name,
                                                   description=version_description)
        APIHelper().check_for_response_errors(response)
        version_id = response.data['data']['id']

        self._upload_version_attributes(version_id)
        self._commit_version(version_id)

        return version_id

    def _download_version(self, version_id):
        """
        Downloads the Version specified, checks for errors, then returns the data & file name (Version name)
        :param version_id: Version ID to download
        :return: Response data that will be written to the file & the file_name of where to download it.
        """
        response, file_name = self.api.download_artifact_scan(version_id)
        APIHelper().check_for_response_errors(response)
        return response.data, file_name

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

    def _get_applications_and_versions(self):
        """
        Gets every application & Version for listing. It returns the response data after checking for errors.
        :return: Response data that will be used to list Applications & Versions
        """
        response = self.api.get_all_project_versions()
        APIHelper().check_for_response_errors(response)
        return response.data['data']

    def _get_attribute_definition_id(self, search_expression):
        response = self.api.get_attribute_definition(search_expression=search_expression)
        if response.success:
            if response.data['data'] is not []:
                return response.data['data'][0]['id']
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
        return None

    def _project_version_description(self):
        if self.runenv == "jenkins":
            return "WebInspect scan from WebBreaker " + os.getenv('JOB_URL', "jenkins server")
        else:
            return "WebBreaker scan from WebBreaker host " + socket.getfqdn()

    def _setup_fortify_ssc_api(self):
        """
        Sets up the FortifyAPI client. Uses the username & password set in init to retrieve a token. Then use that token
        to initialize the API client.
        :return: API client class that can interact with Fortify SSC API.
        """
        try:
            response = FortifyApi(host=self.fortify_url,
                                  username=self.username,
                                  password=self.password,
                                  verify_ssl=False) \
                .get_token()
            APIHelper().check_for_response_errors(response)

            return FortifyApi(self.fortify_url, token=response.data['data']['token'], verify_ssl=False)

        # TODO: Remove general exception handling
        except Exception as e:
            if hasattr(e, 'message'):
                Logger.app.critical("Exception while getting Fortify token: {0}".format(e.message))

        return None

    def _upload_application_version_file(self, version_id, file_name):
        response = self.api.upload_artifact_scan(file_path=('{0}.{1}'.format(file_name, self.extension)),
                                                 project_version_id=version_id)
        APIHelper().check_for_response_errors(response)

    def _upload_version_attributes(self, version_id):
        """
        Uploads attributes to the specified version_id. Will grab all attributes to upload from config.ini
        :param version_id: Version to upload attributes to.
        """
        search_expression = self.config.search_expression
        attribute_definition_id = self.config.attribute_definition_id

        version_attribute_value = self.config.version_attribute_value
        version_attribute_values = self.config.version_attribute_values

        if search_expression is not '':
            attribute_definition_id = self._get_attribute_definition_id(search_expression=search_expression)
        if version_attribute_values is '':
            version_attribute_values = []

        response = self.api.add_project_version_attribute(project_version_id=version_id,
                                                          attribute_definition_id=attribute_definition_id,
                                                          value=version_attribute_value,
                                                          values=version_attribute_values)

        APIHelper().check_for_response_errors(response)

    @staticmethod
    def _trim_ext(file):
        try:
            return os.path.splitext(os.path.basename(file))[0]
        except (TypeError, AttributeError):
            return file