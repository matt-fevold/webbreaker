#!/usr/bin/env python
# -*- coding: utf-8 -*-

from webbreaker.common.authorization import auth_prompt
from webbreaker.common.secretclient import SecretClient
from webbreaker.fortify.common.loghelper import FortifyLogHelper

fortifyloghelper = FortifyLogHelper()


# TODO: Convert to general `webbreaker/common/authenticate`
class FortifyAuth:
    def __init__(self):
        secret_client = SecretClient()
        self.username = secret_client.get('fortify', 'username')
        self.password = secret_client.get('fortify', 'password')

    def authenticate(self, username, password):

        # creds passed from cli
        if username and password:
            fortifyloghelper.log_info_import_credentials()
            return username, password
        else:
            # check config for creds
            fortifyloghelper.log_info_check_config()
            if self._has_auth_creds():
                fortifyloghelper.log_info_credentials_found_in_config()
                return self.username, self.password

            else:
                # ask user for creds
                fortifyloghelper.log_info_credential_not_found()
                username, password = auth_prompt("Fortify")

                self.write_credentials(username, password)
                return username, password

    @staticmethod
    def write_credentials(username, password):
        secret_client = SecretClient()
        secret_client.set('fortify', 'username', username)
        secret_client.set('fortify', 'password', password)

    @staticmethod
    def clear_credentials():
        secret_client = SecretClient()
        secret_client.clear_credentials('fortify', 'username', 'password')

    def _has_auth_creds(self):
        if self.username and self.password:
            return True
        return False
