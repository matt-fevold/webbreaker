#!/usr/bin/env python
# -*- coding: utf-8 -*-

__since__ = "2.1.6"
# TODO Test

from webbreaker.fortify.fortifyclient import FortifyClient
from webbreaker.fortify.fortifyconfig import FortifyConfig
from webbreaker.fortify.authentication import FortifyAuth
from exitstatus import ExitStatus
import sys
from webbreaker.common.webbreakerlogger import Logger
from webbreaker.common.authorization import auth_prompt


class FortifyListApplicationVersions:
    def __init__(self, username, password, application):
        self.config = FortifyConfig
        self.list(username, password, application)

    def list(self, username, password, application):

        fortify_auth = FortifyAuth()
        username, password = fortify_auth.authenticate(username, password)

        fortify_client = FortifyClient(fortify_url=self.config.ssc_url,
                                       fortify_username=username,
                                       fortify_password=password)

        if application:
            fortify_client.list_application_versions(application)
        else:
            fortify_client.list_versions()
        Logger.app.info("Fortify list has successfully completed")

        try:
            if application:
                fortify_client.list_application_versions(application)
            else:
                fortify_client.list_versions()
            Logger.app.info("Fortify list has successfully completed")

        except (AttributeError, UnboundLocalError, TypeError) as e:
            Logger.app.critical("Unable to complete command 'fortify list': {}".format(e))
            sys.exit(ExitStatus.failure)

