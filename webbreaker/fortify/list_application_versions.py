#!/usr/bin/env python
# -*- coding: utf-8 -*-

__since__ = "2.1.6"

# TODO Test
import sys

from exitstatus import ExitStatus
from webbreaker.fortify.common.fortify_helper import FortifyClient
from webbreaker.fortify.fortify_config import FortifyConfig
from webbreaker.fortify.authentication import FortifyAuth
from webbreaker.common.webbreakerlogger import Logger


class FortifyListApplicationVersions:
    def __init__(self, username, password, application):
        self.config = FortifyConfig()
        self.list(username, password, application)

    def list(self, username, password, application):
        try:

            username, password = FortifyAuth().authenticate(username, password)

            fortify_client = FortifyClient(fortify_url=self.config.ssc_url,
                                           fortify_username=username,
                                           fortify_password=password)
            fortify_client.list_application_versions(application)
        except (AttributeError, UnboundLocalError, TypeError) as e:
            Logger.app.critical("Unable to complete command 'fortify list': {}".format(e))
            sys.exit(ExitStatus.failure)
