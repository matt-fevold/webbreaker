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
        self.download(username, password, application, version_name)

    def download(self, username, password, application, version_name):
        if application:
            self.config.application_name = application
        try:
            username, password = FortifyAuth().authenticate(username, password)

            fortify_client = FortifyClient(fortify_url=self.config.ssc_url,
                                           project_template=self.config.project_template,
                                           application_name=self.config.application_name,
                                           fortify_username=username,
                                           fortify_password=password)
            fortify_client.download_scan(version_name)
        except (AttributeError, UnboundLocalError) as e:
            Logger.app.critical("Unable to complete command 'fortify download': {}".format(e))
        except IOError as e:
            Logger.app.error("Couldn't open or write to file {}.".format(e))

