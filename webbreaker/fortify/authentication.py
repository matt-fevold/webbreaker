#!/usr/bin/env python
# -*- coding: utf-8 -*-

from webbreaker.common.webbreakerlogger import Logger
from webbreaker.common.authorization import auth_prompt
from webbreaker.common.secretclient import SecretClient


# TODO: Convert to general `webbreaker/common/authenticate`
class FortifyAuth:
    def __init__(self):
        secret_client = SecretClient()
        self.username = secret_client.get('fortify', 'username')
        self.password = secret_client.get('fortify', 'password')

    def authenticate(self, username, password):

        # creds passed from cli
        if username and password:
            Logger.app.info("Importing Fortify credentials")
            return username, password
        else:
            # check config for creds
            Logger.app.info("No Fortify username or password provided. Checking config.ini for credentials")

            if self._has_auth_creds():
                Logger.app.info("Fortify username and password successfully found in config.ini")
                return self.username, self.password

            else:
                # ask user for creds
                Logger.app.info("Fortify credentials not found in config.ini")
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
