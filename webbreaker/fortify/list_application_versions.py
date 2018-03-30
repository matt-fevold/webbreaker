#!/usr/bin/env python
# -*- coding: utf-8 -*-

__since__ = "2.1.6"

import sys

from exitstatus import ExitStatus
from webbreaker.fortify.common.fortify_helper import FortifyClient
from webbreaker.fortify.fortify_config import FortifyConfig
from webbreaker.fortify.authentication import FortifyAuth
from webbreaker.common.webbreakerlogger import Logger


class FortifyListApplicationVersions:
    def __init__(self, username, password, application):
        self.config = FortifyConfig()

        self.username, self.password = FortifyAuth().authenticate(username, password)
        self.list(application)

    def list(self, application):
        """
        List all Versions of an Application if an Application was specified. If it was not, it will list all
        Applications & Versions.
        :param application: Application Name to list all Versions of. If it is None, it will list all Applications.
        :return: None
        """
        try:
            fortify_client = FortifyClient(fortify_url=self.config.ssc_url,
                                           fortify_username=self.username,
                                           fortify_password=self.password)
            fortify_client.list_application_versions(application)
        except (AttributeError, UnboundLocalError, TypeError) as e:
            Logger.app.critical("Unable to complete command 'fortify list': {}".format(e))
            sys.exit(ExitStatus.failure)
