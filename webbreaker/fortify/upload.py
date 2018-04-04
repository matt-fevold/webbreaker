#!/usr/bin/env python
# -*- coding: utf-8 -*-

__since__ = "2.1.6"

import sys

from exitstatus import ExitStatus
from webbreaker.fortify.common.helper import FortifyHelper
from webbreaker.fortify.config import FortifyConfig
from webbreaker.fortify.authentication import FortifyAuth
from webbreaker.common.webbreakerlogger import Logger


class FortifyUpload:
    def __init__(self, username, password, application_name, version_name, scan_name):
        self.config = FortifyConfig()

        if application_name is None:
            application_name = self.config.application_name
        if not scan_name:
            scan_name = version_name

        self.username, self.password = FortifyAuth().authenticate(username, password)
        self.upload(application_name, version_name, self.config.project_template, scan_name)

    def upload(self, application_name, version_name, application_template, scan_name):
        """
        Uploads a file to Fortify SSC. The scan_name matches the name of the file to upload with a '.fpr' extension
        :param application_name: Application to upload Version to
        :param version_name: Name of the Version to upload
        :param application_template: Template to use for Version upload
        :param scan_name: Name of the scan to upload. Also the name of the file without the '.fpr' extension. Usually
        the same as the version_name
        :return: None
        """
        try:
            fortify_helper = FortifyHelper(fortify_url=self.config.ssc_url,
                                           fortify_username=self.username,
                                           fortify_password=self.password)
            fortify_helper.upload_scan(application_name, version_name, application_template, scan_name)
        except (IOError, ValueError) as e:
            Logger.app.critical("Unable to complete command 'fortify upload'\n Error: {}".format(e))
            sys.exit(ExitStatus.failure)
        except UnboundLocalError:
            Logger.app.error("There are duplicate Fortify SSC Project Version names.  Please choose another one.")
            sys.exit(ExitStatus.failure)
