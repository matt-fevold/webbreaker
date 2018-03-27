#!/usr/bin/env python
# -*- coding: utf-8 -*-

from webbreaker.fortify.fortifyconfig import FortifyConfig
from webbreaker.common.webbreakerlogger import Logger
from webbreaker.common.authorization import auth_prompt
from webbreaker.common.secretclient import SecretClient


class FortifyAuth:
    def __init__(self):
        secret_client = SecretClient()
        self.username = secret_client.get('fortify', 'username')
        self.password = secret_client.get('fortify', 'password')

    def authenticate(self, username, password):

        config = FortifyConfig()

        if username and password:
            Logger.app.info("Importing Fortify credentials")
            return username, password
        else:
            Logger.app.info("No Fortify username or password provided. Checking config.ini for credentials")

            if self.has_auth_creds():
                Logger.app.info("Fortify username and password successfully found in config.ini")
                return self.username, self.password

            else:
                Logger.app.info("Fortify credentials not found in config.ini")
                username, password = auth_prompt("Fortify")

                return username, password

    @staticmethod
    def write_credentials(username, password):
        secret_client = SecretClient()
        secret_client.set('fortify', 'username', username)
        secret_client.set('fortify', 'password', password)

    def clear_redentials(self):
        secret_client = SecretClient()
        secret_client.clear_credentials('fortify', 'username', 'password')

    def has_auth_creds(self):
        if self.username and self.password:
            return True
        else:
            return False
