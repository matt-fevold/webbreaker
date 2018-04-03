#!/usr/bin/env python
# -*- coding: utf-8 -*-

__since__ = "2.1.6"

from webbreaker.fortify.common.fortify_helper import FortifyClient
from webbreaker.fortify.fortify_config import FortifyConfig
from webbreaker.fortify.authentication import FortifyAuth
from webbreaker.common.webbreakerlogger import Logger


class FortifyDownload:
    def __init__(self, username, password, application, version_name):
        self.config = FortifyConfig()

        if application is None:
            application = self.config.application_name

        self.username, self.password = FortifyAuth().authenticate(username, password)
        self.download(application, version_name)

    def download(self, application_name, version_name):
        """
        Downloads a specific Version from an Application.
        :param application_name: Application to search for Version in
        :param version_name: Version to download
        :return: None
        """
        try:
            fortify_client = FortifyClient(fortify_url=self.config.ssc_url,
                                           fortify_username=self.username,
                                           fortify_password=self.password)
            fortify_client.download_scan(application_name, version_name)
        except (AttributeError, UnboundLocalError) as e:
            Logger.app.critical("Unable to complete command 'fortify download': {}".format(e))
        except IOError as e:
            Logger.app.error("Couldn't open or write to file {}.".format(e))

