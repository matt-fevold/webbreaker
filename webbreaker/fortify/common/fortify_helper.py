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
    def __init__(self, fortify_url, project_template=None, application_name=None, fortify_username=None,
                 fortify_password=None, scan_name=None, extension=None):
        self.ssc_server = fortify_url
        self.project_template = project_template
        self.application_name = application_name
        self.user = fortify_username
        self.password = fortify_password
        self.fortify_version = scan_name
        self.extension = extension
        self.runenv = WebBreakerHelper.check_run_env()
        self.token = self._get_token()
        self.api = FortifyApi(self.ssc_server, token=self.token, verify_ssl=False)

        if not self.token:
            raise ValueError("Unable to obtain a Fortify API token.")

    def upload_scan(self, file_name):
        # if reauth == -2:
        #     # The given application doesn't exist
        #     Logger.console.critical(
        #         "Fortify Application {} does not exist. Unable to upload scan.".format(application))
        try:
            file_name = self._trim_ext(file_name)

            project_version_id = self._get_project_version()
            # If our project doesn't exist, exit upload_scan
            if project_version_id == -1:
                return -1
            project_id = self._get_project_id(self.application_name)

            if not project_id:
                project_version_id = self._create_new_project_version()
            if not project_version_id:
                project_version_id = self._create_new_project_version()
            if project_version_id:
                response = self.api.upload_artifact_scan(file_path=('{0}.{1}'.format(file_name, self.extension)),
                                                         project_version_id=project_version_id)

            APIHelper().check_for_response_errors(response)

            Logger.console.info("Your scan file {0}.{1}, has been successfully uploaded to {2}!".format(file_name,
                                                                                                        self.extension,
                                                                                                        self.ssc_server))

        except UnboundLocalError as e:
            Logger.app.critical("Exception trying to create SSC project version: {}".format(e))

        return response

    def list_application_versions(self, application=None):
        response = self.api.get_all_project_versions()
        APIHelper().check_for_response_errors(response)

        print("{0:^8} {1:30} {2:30}".format('ID', 'Application', 'Version'))
        print("{0:8} {1:30} {2:30}".format('-' * 8, '-' * 30, '-' * 30))
        for version in response.data['data']:
            if application is None or version['project']['name'] == application:
                print("{0:8} {1:30} {2:30}".format(version['id'], version['project']['name'], version['name']))
        Logger.app.info("Fortify list has successfully completed")

    def download_scan(self, version_name):
        version_id = self._find_version_id(version_name)

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
            Logger.app.error("No version matching {} found under {} in Fortify".format(version_name, self.application_name))
            sys.exit(ExitStatus.failure)

    def _find_version_id(self, version_name):
        response = self.api.get_all_project_versions()

        if response.success:
            for version in response.data['data']:
                if version['project']['name'] == self.application_name:
                    if version['name'] == version_name:
                        return version['id']

        return False

    def _get_token(self):
        try:
            api = FortifyApi(self.ssc_server, username=self.user, password=self.password, verify_ssl=False)
            response = api.get_token()

            APIHelper().check_for_response_fail_(response)

            token = response.data['data']['token']
            return token

        # TODO: Remove general exception handling
        except Exception as e:
            if hasattr(e, 'message'):
                Logger.app.critical("Exception while getting Fortify token: {0}".format(e.message))

        return None

    def _get_project_id(self, project_name):

        response = self.api.get_projects()

        # Not replacing with APIHelper() due to some special logic going on with the return.
        if response.success:
            for project in response.data['data']:
                if project['name'] == project_name:
                    return project['id']
        return None

    def _project_version_description(self):
        if self.runenv == "jenkins":
            return "WebInspect scan from WebBreaker " + os.getenv('JOB_URL', "jenkins server")
        else:
            return "WebBreaker scan from WebBreaker host " + socket.getfqdn()

    def _create_new_project_version(self):
        """
        Create, add required attributes to, and commit a new project version
        :return: The new project_version_id if successful. Otherwise, None.
        """
        try:
            response = self.api.create_project_version(project_name=self.application_name,
                                                       project_id=self._get_project_id(self.application_name),
                                                       project_template=self.project_template,
                                                       version_name=self.fortify_version,
                                                       description=self._project_version_description())

            if not response.success:
                raise ValueError("Failed to create a new project version")

            project_version_id = response.data['data']['id']

            # At Target, only one attribute is required
            response = self.api.add_project_version_attribute(project_version_id=project_version_id,
                                                              attribute_definition_id=self._get_attribute_definition_id(
                                                                  search_expression='name:"CI Number"'),
                                                              value='New WebBreaker Application',
                                                              values=[])
            if not response.success:
                raise ValueError("Failed to create required project version attribute")

            response = self.api.commit_project_version(project_version_id=project_version_id)

            if not response.success:
                raise ValueError("Failed to commit new project version")
            return project_version_id

        except Exception as e:
            Logger.app.critical("Exception trying to create project version. {0}".format(e.message))

        return None

    def _create_new_project_version(self):
        try:
            # It's kinda dumb for this api call to require both project name and id?
            response = self.api.create_new_project_version(project_name=self.application_name,
                                                           project_template=self.project_template,
                                                           version_name=self.fortify_version,
                                                           description=self._project_version_description())

            if not response.success:
                raise ValueError("Failed to create a new project version")

            project_version_id = response.data['data']['id']
            project_id = response.data['data']['project']['id']

            """
            At Target, only one attribute is required
            TODO: Treatment of all required attributes development_strategy, accessibility, custom_attribute, etc. 
            may accept null values (unconfirmed?), additional conditions need to be placed here to successfully complete this response.
            For example default SSC installations require attributeDefinitionId 1, 5, 6, and 7, however other deployments may have a single
            custom_attribute as is implemented below.  See also 
            https://github.com/target/fortifyapi/blob/134477ef708e63d8c7b555741f5c69610abad920/fortifyapi/fortify.py#L105
            search_expression='name:"CI Number"'
            """
            response = self.api.add_project_version_attribute(project_version_id=project_version_id,
                                                              attribute_definition_id=self._get_attribute_definition_id(
                                                                  search_expression='name:"CI Number"'),
                                                              value='New WebBreaker Application',
                                                              values=[])
            if not response.success:
                raise ValueError("Failed to create required project version attribute")

            response = self.api.commit_project_version(project_version_id=project_version_id)
            if not response.success:
                raise ValueError("Failed to commit new project version")
                # Logger.app.debug("Created new project version id {0}".format(project_version_id))
        except (AttributeError, UnboundLocalError) as e:
            Logger.app.critical("Exception creating project version. {0}".format(e))

        return project_version_id

    def _get_attribute_definition_id(self, search_expression):
        response = self.api.get_attribute_definition(search_expression=search_expression)
        if response.success:
            return response.data['data'][0]['id']
        else:
            return None

    def _get_project_version(self):
        """
        If a project version already exists, return it's project_version_id
        If a project version does NOT exist, create it and return it's project_version_id
        If none of the above succeeds, log the reason(s) and return None
        :return:
        """
        try:
            response = self.api.get_all_project_versions()  # api should support a search expression here. alas...

            if response.success:

                for project_version in response.data['data']:
                    if project_version['project']['name'] == self.application_name:
                        if project_version['name'] == self.fortify_version:
                            # we have a matching project version
                            Logger.app.debug("Found existing project version {0}".format(project_version['id']))
                            return project_version['id']

                # Didn't find a matching project version, verify that our project exists
                for project_version in response.data['data']:
                    if project_version['project']['name'] == self.application_name:
                        # Our project exists, so create a new version
                        return self._create_new_project_version()

                # Let upload_scan know that our project doesn't exist
                return -2
            elif "401" in response.message:
                # Avoid printing error for invalid token. Return -1 to reauth
                return -1
            else:
                Logger.app.critical("Failed to get project version. {0}".format(response.message))
        except Exception as e:
            Logger.app.critical("Exception trying to get project version. {0}".format(e.message))

        return None

    @staticmethod
    def _trim_ext(file):
        try:
            return os.path.splitext(os.path.basename(file))[0]
        except (TypeError, AttributeError):
            return file
