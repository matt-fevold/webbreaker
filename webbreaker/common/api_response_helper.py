#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

from webbreaker.common.webbreakerlogger import Logger
from exitstatus import ExitStatus


class APIHelper:
    def __init__(self):
        pass

    def check_for_response_errors(self, response):
        """
        Check the response for any possible error messages, raise an error and exit if found.
        :param response:
        :return:
        """
        self._check_for_authorization_error(response)
        self._check_for_response_fail(response)

    @staticmethod
    def _check_for_authorization_error(response):
        # Check for 401 response and break if it occurs.
        if response.response_code == 401:
            Logger.app.critical("An Authorization Error Occurred.")
            sys.exit(ExitStatus.failure)

    @staticmethod
    def _check_for_response_fail(response):
        if response.success:
            pass
        else:
            Logger.app.error("The call to the API was not successful: {}".format(response.message))
            sys.exit(ExitStatus.failure)
