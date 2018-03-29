#!/usr/bin/env python
# -*- coding: utf-8 -*-

__since__ = "2.1.6"
# TODO Test

from webbreaker.fortify.common.fortify_helper import FortifyClient
from webbreaker.fortify.fortify_config import FortifyConfig
from webbreaker.fortify.authentication import FortifyAuth
from webbreaker.common.webbreakerlogger import Logger


class FortifyDownload:
    def __init__(self, username, password, application, version_name):
        self.config = FortifyConfig()

        if application:
            self.config.application_name = application

        self.username, self.password = FortifyAuth().authenticate(username, password)
        self.download(version_name)

    def download(self, version_name):
        try:
            fortify_client = FortifyClient(fortify_url=self.config.ssc_url,
                                           project_template=self.config.project_template,
                                           application_name=self.config.application_name,
                                           fortify_username=self.username,
                                           fortify_password=self.password)
            fortify_client.download_scan(version_name)
        except (AttributeError, UnboundLocalError) as e:
            Logger.app.critical("Unable to complete command 'fortify download': {}".format(e))
        except IOError as e:
            Logger.app.error("Couldn't open or write to file {}.".format(e))

