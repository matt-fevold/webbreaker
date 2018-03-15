#!/usr/bin/env python
# -*- coding: utf-8 -*-
from subprocess import CalledProcessError
import os
import sys
import re
from webbreaker.common.webbreakerlogger import Logger
from webbreaker.common.confighelper import Config
from cryptography.fernet import Fernet

try:
    import ConfigParser as configparser

    config = configparser.SafeConfigParser()
except ImportError:  # Python3
    import configparser

    config = configparser.ConfigParser()


class SecretClient(object):
    def __init__(self):
        self.fernet_key = self.__read_fernet_secret__()
        self.config_file = Config().config

    def get(self, section, key):
        config.read(self.config_file)
        try:
            encryp_value = config.get(section, key)
        except (config.NoSectionError) as e:
            Logger.app.error("Error: {}".format(e))
        except (config.NoOptionError, CalledProcessError) as noe:
            Logger.console.error("{} has incorrect or missing values {}".format(self.config_file, noe))

        try:
            if not encryp_value:
                return None
            if encryp_value[:2] == "e$":
                decryp_value = self.__decrypt__(encryp_value)
                return decryp_value
        except UnboundLocalError:
            Logger.console.info("Incorrect user name or password!")

        return encryp_value

    def set(self, section, key, value):
        encryp_value = self.__encrypt__(value)
        try:
            config.read(self.config_file)
            config.set(section, key, "e$Fernet$" + encryp_value.decode())
            with open(self.config_file, 'w') as new_config:
                config.write(new_config)

        except (config.NoOptionError, CalledProcessError) as noe:
            Logger.app.error(
                "{} has incorrect or missing values, see log file {}".format(self.config_file, Logger.app_logfile))
            sys.exit(1)
        except config.Error as e:
            Logger.console.error("Error reading {}, see log file: {}".format(self.config_file, Logger.app_logfile))
            Logger.app.error("Error reading {} {}".format(self.config_file, e))
            sys.exit(1)
        return True

    def clear_credentials(self, section, username_key, password_key):
        try:
            config.read(self.config_file)
            config.set(section, username_key, '')
            config.set(section, password_key, '')
            with open(self.config_file, 'w') as new_config:
                config.write(new_config)

        except (config.NoOptionError, CalledProcessError) as noe:
            Logger.app.error(
                "{} has incorrect or missing values, see log file {}".format(self.config_file, Logger.app_logfile))
            sys.exit(1)
        except config.Error as e:
            Logger.console.error("Error reading {}, see log file: {}".format(self.config_file, Logger.app_logfile))
            Logger.app.error("Error reading {} {}".format(self.config_file, e))
            sys.exit(1)
        return True

    def verify_secret(self):
        if self.secret_exists():
            return True
        else:
            self.write_secret()

    # TODO: Change to check inside file, not just if file is there
    def secret_exists(self):
        return os.path.isfile(Config().secret)

    def wipe_all_credentials(self):
        # TODO if any other values are encrypted, make sure to add them here
        self.clear_credentials('fortify', 'username', 'password')
        self.clear_credentials('webinspect', 'username', 'password')

    def write_secret(self, overwrite=False):
        secret_path = Config().secret
        if self.secret_exists() and overwrite:
            os.chmod(secret_path, 0o200)
        key = Fernet.generate_key()
        with open(secret_path, 'w') as secret_file:
            secret_file.write(key.decode())
        os.chmod(secret_path, 0o400)
        print("New secret has been set.")

    def __encrypt__(self, value):
        try:
            cipher = Fernet(self.fernet_key)
            encryp_value = cipher.encrypt(value.encode())
            return encryp_value
        except ValueError as e:
            Logger.console.error("Error encrypting...exiting without completeing command."
                                 "Please see log {}".format(Logger.app_logfile))
            Logger.app.error(e)
            sys.exit(1)

    def __decrypt__(self, encryp_value):
        encryption_version = re.search('e\$(.*)\$.*', encryp_value).group(1)
        if encryption_version == 'Fernet':
            encryp_value = encryp_value.split(encryption_version + "$", 1)[1]
            try:
                cipher = Fernet(self.fernet_key)
                decryp_value = cipher.decrypt(encryp_value.encode()).decode()
            except Exception as e:
                Logger.app.error(
                    "Error decrypting the Fortify secret.  Exiting now, see log {}".format(Logger.app_logfile))
                Logger.app.error("Error: {}".format(e))
                Logger.app.error("If error persists, run 'webbreaker admin secret'")
                sys.exit(1)
        else:
            Logger.app.error("Error decrypting.  Unsupported encryption version")
            sys.exit(1)
        return decryp_value

    def __read_fernet_secret__(self):
        self.verify_secret()
        try:
            with open(Config().secret, 'r') as secret_file:
                fernet_key = secret_file.readline().strip()
            return fernet_key
        except IOError:
            Logger.console.error("Error retrieving Fernet key.")
            sys.exit(1)
