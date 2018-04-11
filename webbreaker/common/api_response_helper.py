#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

from webbreaker.common.webbreakerlogger import Logger
from exitstatus import ExitStatus


class APIHelper:
    def __init__(self):
        pass

    def check_for_response_errors(self, response, error_message=None):
        """
        Check the response for any possible error messages, raise an error and exit if found.
        :param response:
        :param error_message: to be passed in when needed for better error messages
        :return:
        """
        self._check_for_authorization_error(response)
        self._check_for_response_fail(response, error_message)

    @staticmethod
    def _check_for_authorization_error(response):
        # Check for 401 response and break if it occurs.
        if response.response_code == 401:
            Logger.app.critical("An Authorization Error Occurred.")
            sys.exit(ExitStatus.failure)

    @staticmethod
    def _check_for_response_fail(response, error_message):
        """

        :param response:
        :param error_message: to be passed in when it is used for better logging
        :return:
        """
        if response.success:
            pass
        else:
            Logger.app.error("The call to the API was not successful: {}".format(response.message))
            if error_message is not None:
                Logger.app.error(error_message)

            sys.exit(ExitStatus.failure)
