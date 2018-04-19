#!/usr/bin/env python
# -*- coding: utf-8 -*-

__since__ = "2.1.6"

import sys

from exitstatus import ExitStatus
from webbreaker.fortify.common.helper import FortifyHelper
from webbreaker.fortify.config import FortifyConfig
from webbreaker.fortify.authentication import FortifyAuth
from webbreaker.common.webbreakerlogger import Logger
from webbreaker.fortify.common.loghelper import FortifyLogHelper

fortifyloghelper = FortifyLogHelper()


class FortifyUpload:
    def __init__(self, username, password, application_name, version_name, scan_name, custom_value):
        self.config = FortifyConfig()

        if application_name is None:
            application_name = self.config.application_name
        if not scan_name:
            scan_name = version_name

        self.username, self.password = FortifyAuth().authenticate(username, password)
        self.upload(application_name, version_name, self.config.project_template, scan_name, custom_value)

    def upload(self, application_name, version_name, application_template, scan_name, custom_value):
        """
        Uploads a file to Fortify SSC. The scan_name matches the name of the file to upload with a '.fpr' extension
        :param application_name: Application to upload Version to
        :param version_name: Name of the Version to upload
        :param application_template: Template to use for Version upload
        :param scan_name: Name of the scan to upload. Also the name of the file without the '.fpr' extension. Usually
        the same as the version_name
        :param custom_value: Custom value to be used while uploading new attributes to Application Version.
        """
        try:
            self.upload_scan(application_name, version_name, application_template, scan_name, custom_value)
        except (IOError, ValueError) as e:
            Logger.app.critical("Unable to complete command 'fortify upload'\n Error: {}".format(e))
            sys.exit(ExitStatus.failure)
        except UnboundLocalError:
            fortifyloghelper.log_error_duplicate_ssc_project_versioin()
            sys.exit(ExitStatus.failure)

    def upload_scan(self, application_name, version_name, project_template, file_name, custom_value):
        """
        If the Application & Version already exists, log and exit with error.
        Create a new Version and create Application if doesn't exist.
        Finalize Application Version
        Upload file to Application Version.
        :param application_name: Name of the Application for Upload.
        :param version_name: Name of the Version for Upload
        :param project_template: Project Template GUID from config.ini
        :param file_name: Scan name to upload. It will be appended with '.fpr' to create the filename
        """
        fortify_helper = FortifyHelper(fortify_url=self.config.ssc_url,
                                       fortify_username=self.username,
                                       fortify_password=self.password)

        file_name = fortify_helper.trim_ext(file_name)
        description = fortify_helper.project_version_description()
        application_id = fortify_helper.get_application_id(application_name)

        if application_id:
            version_id = fortify_helper.get_version_id(application_name, version_name)
            if version_id:
                fortifyloghelper.log_info_found_existing_application_version(application_name,version_name)
            else:
                version_id = fortify_helper.create_application_version(application_name=application_name,
                                                                       application_id=application_id,
                                                                       version_name=version_name,
                                                                       application_template=project_template,
                                                                       description=description)
                fortify_helper.finalize_application_version_creation(version_id, custom_value)
        else:
            version_id = fortify_helper.create_application_version(application_name=application_name,
                                                                   application_id=application_id,
                                                                   version_name=version_name,
                                                                   application_template=project_template,
                                                                   description=description)
            fortify_helper.finalize_application_version_creation(version_id, custom_value)

            fortify_helper.upload_application_version_file(version_id=version_id, file_name=file_name)
        fortifyloghelper.log_info_file_uploaded_success(file_name, fortify_helper.extension, fortify_helper.fortify_url)