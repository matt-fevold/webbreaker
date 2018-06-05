#!/usr/bin/env python
# -*- coding: utf-8 -*-

from webbreaker.common.webbreakerlogger import Logger


# Okay - this will not look nice future person reading this. This needs to be fixed again after we
#   get our testing in a nicer spot - currently some tests check for logging output (not anything we've refactored
#   recently (~2.1.5)) but those will change as more work is done. TODO


class LogExceptionHelper(object):

    def __init__(self):
        pass

    #__main__
    def log_error_git_command(self, args):
        Logger.app.error("Please install the git client or add it to your PATH variable ->"
                         " https://git-scm.com/download.  See log {}!!!".format(args))

    def log_info_credentials_store_success(self):
        Logger.app.info("Credentials stored successfully")

    def log_info_webinspect_credential_clear_success(self):
        Logger.app.info("Successfully cleared WebInspect credentials from config.ini")

    def log_error_invalid_ssl_credentials(self):
        Logger.app.error("Invalid SSL credentials")
