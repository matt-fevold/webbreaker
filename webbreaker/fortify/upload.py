#!/usr/bin/env python
# -*- coding: utf-8 -*-

__since__ = "2.1.6"
# TODO Test

from webbreaker.fortify.common.fortify_helper import FortifyClient
from webbreaker.fortify.fortify_config import FortifyConfig
from webbreaker.fortify.authentication import FortifyAuth
from webbreaker.common.webbreakerlogger import Logger


class FortifyUpload:
    def __init__(self, username, password, application, version, scan_name):
        self.version = version
        self.extension = "fpr"
        self.config = FortifyConfig()

        if application:
            self.config.application_name = application
        if not scan_name:
            scan_name = version

        self.username, self.password = FortifyAuth().authenticate(username, password)
        self.upload(scan_name)

    def upload(self, scan_name):
        try:
            fortify_client = FortifyClient(fortify_url=self.config.ssc_url,
                                           project_template=self.config.project_template,
                                           application_name=self.config.application_name,
                                           fortify_username=self.username,
                                           fortify_password=self.password,
                                           scan_name=self.version,
                                           extension=self.extension)
            fortify_client.upload_scan(scan_name)
        except (IOError, ValueError) as e:
            Logger.console.critical("Unable to complete command 'fortify upload'\n Error: {}".format(e))
        except UnboundLocalError:
            Logger.app.error("There are duplicate Fortify SSC Project Version names.  Please choose another one.")
