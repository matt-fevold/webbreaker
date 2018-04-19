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


class FortifyDownload:
    def __init__(self, username, password, application_name, version_name):
        self.config = FortifyConfig()

        if application_name is None:
            application_name = self.config.application_name

        self.username, self.password = FortifyAuth().authenticate(username, password)
        self.download(application_name, version_name)

    def download(self, application_name, version_name):
        """
        Downloads a specific Version from an Application.
        :param application_name: Application to search for Version in
        :param version_name: Version to download
        :return: None
        """

        try:
            self.download_scan(application_name, version_name)
        except (AttributeError, UnboundLocalError) as e:
            Logger.app.critical("Unable to complete command 'fortify download': {}".format(e))
            sys.exit(ExitStatus.failure)
        except IOError as e:
            fortifyloghelper.log_error_can_not_open_or_write_to_file(e)
            sys.exit(ExitStatus.failure)

    def download_scan(self, application_name, version_name):
        """
        Downloads a scan with matching Application name & Version name.
        :param application_name: Required. Application to search for the Version under.
        :param version_name: The Version to download.
        """
        fortify_helper = FortifyHelper(fortify_url=self.config.ssc_url,
                                       fortify_username=self.username,
                                       fortify_password=self.password)
        version_id = fortify_helper.get_version_id(application_name, version_name)

        if version_id:
            file_content, file_name = fortify_helper.download_version(version_id)
            with open(file_name, 'wb') as f:
                f.write(file_content)
                fortifyloghelper.log_info_version_successful_written_to_file(version_id, file_name)
        else:
            fortifyloghelper.log_error_no_version_match_under_application_name(version_name, application_name)
            sys.exit(ExitStatus.failure)

