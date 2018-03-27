#!/usr/bin/env python
# -*- coding: utf-8 -*-

__since__ = "2.1.6"
# TODO Test

from webbreaker.fortify.common.fortify_helper import FortifyClient
from webbreaker.fortify.fortify_config import FortifyConfig
from webbreaker.fortify.authentication import FortifyAuth
from webbreaker.common.webbreakerlogger import Logger


class FortifyDownload:
    def __init__(self, username, password, application, version):
        self.config = FortifyConfig()
        self.download(username, password, application, version)

    def download(self, username, password, application, version):
        if application:
            self.config.application_name = application
        try:

            fortify_auth = FortifyAuth()
            username, password = fortify_auth.authenticate(username, password)

            fortify_client = FortifyClient(fortify_url=self.config.ssc_url,
                                           project_template=self.config.project_template,
                                           application_name=self.config.application_name,
                                           fortify_username=username,
                                           fortify_password=password)

            version_id = fortify_client.find_version_id(version)
            if version_id:
                filename = fortify_client.download_scan(version_id)
                if filename:
                    Logger.app.info("Scan file for version {} successfully written to {}".format(version_id, filename))
                else:
                    Logger.app.error("Scan download for version {} has failed".format(version_id))
            else:
                Logger.app.error("No version matching {} found under {} in Fortify".format(version, application))
        except (AttributeError, UnboundLocalError) as e:
            Logger.app.critical("Unable to complete command 'fortify download': {}".format(e))
