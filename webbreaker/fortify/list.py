#!/usr/bin/env python
# -*- coding: utf-8 -*-

__since__ = "2.1.6"

import sys

from exitstatus import ExitStatus
from webbreaker.fortify.common.helper import FortifyHelper
from webbreaker.fortify.config import FortifyConfig
from webbreaker.fortify.authentication import FortifyAuth
from webbreaker.common.webbreakerlogger import Logger
from webbreaker.fortify.common.loghelper import FortifyLogHelper

fortifyloghelper = FortifyLogHelper()

class FortifyList:
    def __init__(self, username, password, application_name):
        self.config = FortifyConfig()

        self.username, self.password = FortifyAuth().authenticate(username, password)
        self.list(application_name)

    def list(self, application_name):
        """
        List all Versions of an Application if an Application was specified. If it was not, it will list all
        Applications & Versions.
        :param application_name: Application Name to list all Versions of. If it is None, it will list all Applications.
        :return: None
        """
        try:
            self.list_application_versions(application_name)
        except (AttributeError, UnboundLocalError, TypeError) as e:
            Logger.app.critical("Unable to complete command 'fortify list': {}".format(e))
            sys.exit(ExitStatus.failure)

    def list_application_versions(self, application_name):
        """
        List all Applications & Versions from the Fortify URL unless application_name is supplied (Not None).
        :param application_name: If Application name is specified, only list versions for that Application
        """
        fortify_helper = FortifyHelper(fortify_url=self.config.ssc_url,
                                       fortify_username=self.username,
                                       fortify_password=self.password)
        response_data = fortify_helper.get_applications_and_versions()

        print("{0:^8} {1:30} {2:30}".format('ID', 'Application', 'Version'))
        print("{0:8} {1:30} {2:30}".format('-' * 8, '-' * 30, '-' * 30))
        for version in response_data:
            if application_name is None or application_name == version['project']['name']:
                print("{0:8} {1:30} {2:30}".format(version['id'], version['project']['name'], version['name']))

        fortifyloghelper.log_info_list_success()