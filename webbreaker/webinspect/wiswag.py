#!/usr/bin/env python
# -*- coding: utf-8 -*-

from time import sleep
import random
import string
import sys

from exitstatus import ExitStatus
from webbreaker.common.confighelper import Config
from webinspectapi.webinspect import WebInspectApi
from webbreaker.webinspect.authentication import WebInspectAuth
from webbreaker.common.webbreakerlogger import Logger
from webbreaker.common.api_response_helper import APIHelper
from webbreaker.webinspect.webinspect_config import WebInspectConfig
from webbreaker.webinspect.jit_scheduler import WebInspectJitScheduler, NoServersAvailableError


class WebInspectWiswag:
    def __init__(self, url, wiswag_name, username=None, password=None, server=None):
        auth_config = WebInspectAuth()
        self.wiswag_name = wiswag_name
        self.host = server
        self.username, self.password = auth_config.authenticate(username, password)

        if self.host is None:
            self.host = self.get_endpoint()

        self.api = WebInspectApi(self.host, verify_ssl=False, username=self.username, password=self.password)
        self.wiswag(url)

    def wiswag(self, url):
        if self.wiswag_name is None:
            self._generate_random_wiswag_name()

        self.api.create_wiswag(url, self.wiswag_name)

        # go through the settings list 3 times (~15 secs before timeout)
        for i in range(3):
            response = self.api.list_settings()
            APIHelper().check_for_response_errors(response)
            if response.data is not None:
                for settingListName in response.data:
                    if settingListName == self.wiswag_name:
                        Logger.app.info("Found wiswag_name: {}".format(self.wiswag_name))
                        self._download_wiswag(self.wiswag_name)
                        sys.exit(ExitStatus.success)
            else:
                Logger.app.info("Fail to find wiswag_name {}. Retrying".format(self.wiswag_name))
                sleep(5)
        Logger.app.error("Timeout error: Can not find wiswag_name {}".format(self.wiswag_name))

    def _download_wiswag(self, wiswag_name):
        response = self.api.download_settings(wiswag_name)
        extension = 'xml'

        try:
            with open('{0}.{1}'.format(wiswag_name, extension), 'wb') as f:
                f.write(response.data)
        except UnboundLocalError as e:
            Logger.app.error('Error saving file locally {}'.format(e))
            sys.exit(ExitStatus.failure)

    def _generate_random_wiswag_name(self):
        self.wiswag_name = "wiswag" + "-" + "".join(
            random.choice(string.ascii_uppercase + string.digits) for _ in range(5))

    def get_endpoint(self):
        jit_scheduler = WebInspectJitScheduler(username=self.username,
                                               password=self.password)
        Logger.app.info("Querying WebInspect scan engines for availability.")

        endpoint = jit_scheduler.get_endpoint()
        return endpoint










