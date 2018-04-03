#!/usr/bin/env python
# -*- coding: utf-8 -*-

__since__ = "2.1.6"

from webbreaker.fortify.common.fortify_helper import FortifyClient
from webbreaker.fortify.fortify_config import FortifyConfig
from webbreaker.fortify.authentication import FortifyAuth
from webbreaker.common.webbreakerlogger import Logger


class FortifyUpload:
    def __init__(self, username, password, application, version, scan_name):
        self.version = version
        self.config = FortifyConfig()

        if application is None:
            application = self.config.application_name
        if not scan_name:
            scan_name = version

        self.username, self.password = FortifyAuth().authenticate(username, password)
        self.upload(application, version, self.config.project_template, scan_name)

    def upload(self, application, version, application_template, scan_name):
        """
        Uploads a file to Fortify SSC. The scan_name matches the name of the file to upload with a '.fpr' extension
        :param application: Application to upload Version to
        :param version: Name of the Version to upload
        :param application_template: Template to use for Version upload
        :param scan_name: Name of the scan to upload. Also the name of the file without the '.fpr' extension. Usually
        the same as the version_name
        :return: None
        """
        try:
            fortify_client = FortifyClient(fortify_url=self.config.ssc_url,
                                           fortify_username=self.username,
                                           fortify_password=self.password)
            fortify_client.upload_scan(application, version, application_template, scan_name)
        except (IOError, ValueError) as e:
            Logger.console.critical("Unable to complete command 'fortify upload'\n Error: {}".format(e))
        except UnboundLocalError:
            Logger.app.error("There are duplicate Fortify SSC Project Version names.  Please choose another one.")
