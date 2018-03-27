#!/usr/bin/env python
# -*- coding: utf-8 -*-

__since__ = "2.1.6"
# TODO Test

from webbreaker.fortify.fortifyclient import FortifyClient
from webbreaker.fortify.fortifyconfig import FortifyConfig
from webbreaker.fortify.authentication import FortifyAuth
from webbreaker.common.webbreakerlogger import Logger


class FortifyUpload:
    def __init__(self, username, password, application, version, scan_name):
        self.config = FortifyConfig()
        self.upload(username, password, application, version, scan_name)

    def upload(self, username, password, application, version, scan_name):

        fortify_auth = FortifyAuth()
        username, password = fortify_auth.authenticate(username, password)

        # Fortify only accepts fpr scan files
        extension = 'fpr'
        if application:
            self.config.application_name = application
        if not scan_name:
            scan_name = version
        try:
            fortify_client = FortifyClient(fortify_url=self.config.ssc_url,
                                           project_template=self.config.project_template,
                                           application_name=self.config.application_name,
                                           fortify_username=username,
                                           fortify_password=password, scan_name=version, extension=extension)

            reauth = fortify_client.upload_scan(file_name=scan_name)

            if reauth == -2:
                # The given application doesn't exist
                Logger.console.critical(
                    "Fortify Application {} does not exist. Unable to upload scan.".format(application))

        except (IOError, ValueError) as e:
            Logger.console.critical("Unable to complete command 'fortify upload'\n Error: {}".format(e))
        except (UnboundLocalError):
            Logger.app.error("There are duplicate Fortify SSC Project Version names.  Please choose another one.")
