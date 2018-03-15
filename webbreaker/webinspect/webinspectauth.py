
#!/usr/bin/env python
# -*- coding: utf-8 -*-

from subprocess import CalledProcessError
from webbreaker.common.webbreakerlogger import Logger
from webbreaker.common.webbreakerhelper import WebBreakerHelper
from webbreaker.common.confighelper import Config

from webbreaker.common.secretclient import SecretClient

from webbreaker.common.logexceptionhelper import LogExceptionHelper
from click import prompt

try:
    import ConfigParser as configparser

    config = configparser.SafeConfigParser()
except ImportError:  # Python3
    import configparser

    config = configparser.ConfigParser()

runenv = WebBreakerHelper.check_run_env()
logexceptionhelper = LogExceptionHelper()


def auth_prompt(service_name):
    username = prompt('{} user'.format(service_name))
    password = prompt('{} password'.format(service_name), hide_input=True)
    return username, password


class WebInspectAuth(object):
    def __init__(self):
        Logger.app.debug("Starting webinspect auth config initialization")

        self.require_authenticate = self._check_if_authenticate_required_()

        if self.require_authenticate:
            Logger.app.debug("Authenitcation is required by the config file")
        else:
            Logger.app.debug("Authenitcation is not required by the config file (or it couldn't read the config)")

        self.username, self.password = self._get_config_authentication_()

        Logger.app.debug("Completed webinspect auth config initialization")

    def _check_if_authenticate_required_(self):
        config_file = Config().config
        try:
            config.read(config_file)
            return config.get("webinspect", "authenticate").lower() == 'true'

        except (configparser.NoOptionError, CalledProcessError) as noe:
            Logger.app.error("{} has incorrect or missing values {}".format(config_file, noe))
        except configparser.Error as e:
            Logger.app.error("Error reading {} {}".format(config_file, e))

    def _get_config_authentication_(self):
        secret_client = SecretClient()

        username = secret_client.get('webinspect', 'username')
        password = secret_client.get('webinspect', 'password')
        return username, password

    def clear_credentials(self):
        secret_client = SecretClient()
        secret_client.clear_credentials('webinspect', 'username', 'password')

    def write_credentials(self, username, password):
        secret_client = SecretClient()
        secret_client.set('webinspect', 'username', username)
        secret_client.set('webinspect', 'password', password)

    def has_auth_creds(self):
        if self.username and self.password:
            return True
        else:
            return False

    def authenticate(self, username, password):
        '''
        authenticate
        :param username: user supplied username
        :param password: user supplied password
        :return: a tuple of username, password
        '''
        Logger.app.debug("Start finding credentials to use")
        if self.require_authenticate:
            Logger.app.debug("Credentials are required")
            # user passed in credentials
            if username is not None and password is not None:
                Logger.app.debug("User has supplied credentials in the cli")
            # there was a username/password in the config file.
            elif self.has_auth_creds():
                Logger.app.debug("Credentials found in config")
                username = self.username
                password = self.password
            # prompt the user for their credentials
            else:
                Logger.app.debug("No credentials found - prompting user")
                username, password = auth_prompt("webinspect")
        # no auth!?!
        else:
            Logger.app.debug("Credentials are not required")
            username = None
            password = None

        Logger.app.debug("Completed finding credentials")
        return username, password
