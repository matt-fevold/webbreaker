#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import socket

from fortifyapi.fortify import FortifyApi
from webbreaker.common.api_response_helper import APIHelper
from webbreaker.fortify.config import FortifyConfig
from webbreaker.common.webbreakerhelper import WebBreakerHelper


class FortifyHelper(object):
    def __init__(self, fortify_url, fortify_username, fortify_password):
        # Static
        self.extension = 'fpr'

        # Required Globals
        self.fortify_url = fortify_url
        self.username = fortify_username
        self.password = fortify_password

        self.config = FortifyConfig()
        self.runenv = WebBreakerHelper.check_run_env()
        self.api = self._setup_fortify_ssc_api()

    def create_application_version(self, application_name, version_name, application_template, description,
                                    application_id=None):
        """
        Creates a new Version under the specified Application ID.
        :param application_name: Name of the Application to put the Version under.
        :param application_id: ID of the Application. If None, creates a new Application with the application_name.
        :param version_name: Name of the Version to create.
        :param application_template: Brought in from the config.ini during the FortifyUpload Class __init__
        :param description: Description for Application Version
        :return: Version ID of the newly created Version.
        """

        response = self.api.create_application_version(application_name=application_name,
                                                       application_id=application_id,
                                                       application_template=application_template,
                                                       version_name=version_name,
                                                       description=description)
        APIHelper().check_for_response_errors(response)
        return response.data['data']['id']

    def download_version(self, version_id):
        """
        Downloads the Version specified, checks for errors, then returns the data & file name (Version name)
        :param version_id: Version ID to download
        :return: Response data that will be written to the file & the file_name of where to download it.
        """
        response, file_name = self.api.download_artifact_scan(version_id)
        APIHelper().check_for_response_errors(response)
        return response.data, file_name

    def finalize_application_version_creation(self, version_id, custom_value):

        custom_attribute = self._get_custom_attribute(custom_value)

        response = \
            self.api.bulk_create_new_application_version_request(version_id=version_id,
                                                                 development_phase=self.config.development_phase,
                                                                 development_strategy=self.config.development_strategy,
                                                                 accessibility=self.config.accessibility,
                                                                 business_risk_ranking=self.config.business_risk_ranking,
                                                                 custom_attribute=custom_attribute
                                                                 )
        APIHelper().check_for_response_errors(response)

    def _get_custom_attribute(self, custom_value=None):
        custom_attribute_id = self._get_attribute_definition_id(search_expression=self.config.custom_attribute_name)

        if custom_value:
            return custom_attribute_id, custom_value
        else:
            return custom_attribute_id, self.config.custom_attribute_value

    def get_application_id(self, application_name):
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

    def get_applications_and_versions(self):
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
        return ''

    def get_version_id(self, application_name, version_name):
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

    def project_version_description(self):
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
        api = FortifyApi(host=self.fortify_url,
                         username=self.username,
                         password=self.password,
                         verify_ssl=self.config.verify_ssl)

        response_token = api.get_token()
        APIHelper().check_for_response_errors(response_token)

        return FortifyApi(self.fortify_url, token=response_token.data['data']['token'],
                          verify_ssl=self.config.verify_ssl)

    def upload_application_version_file(self, version_id, file_name):
        response = self.api.upload_artifact_scan(file_path=('{0}.{1}'.format(file_name, self.extension)),
                                                 project_version_id=version_id)
        APIHelper().check_for_response_errors(response)

    @staticmethod
    def trim_ext(file):
        try:
            return os.path.splitext(os.path.basename(file))[0]
        except (TypeError, AttributeError):
            return file
