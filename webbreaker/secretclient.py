#!/usr/bin/env python
# -*- coding: utf-8 -*-

try:
    import ConfigParser as configparser
except ImportError:  # Python3
    import configparser
from subprocess import CalledProcessError
import os
import sys
import re
from webbreaker.webbreakerlogger import Logger
from cryptography.fernet import Fernet
from os.path import expanduser


class SecretClient(object):
    def __init__(self):
        self.fernet_key = self.__read_fernet_secret__()
        self.webbreaker_ini = os.path.abspath(os.path.join('webbreaker', 'etc', 'webbreaker.ini'))
        self.fortify_ini = os.path.abspath(os.path.join('webbreaker', 'etc', 'fortify.ini'))
        self.webinspect_ini = os.path.abspath(os.path.join('webbreaker', 'etc', 'webinspect.ini'))
        try:  # Python 2
            self.config = configparser.SafeConfigParser()
        except NameError:  # Python 3
            self.config = configparser.ConfigParser()

    def get(self, ini, section, key):
        config_file = self.__get_ini_file__(ini)
        self.config.read(config_file)
        try:
            encryp_value = self.config.get(section, key)
        except configparser.NoSectionError as e:
            Logger.app.error("Error: {}".format(e))

        except (configparser.NoOptionError, CalledProcessError) as noe:
            Logger.console.error("{} has incorrect or missing values {}".format(config_file, noe))
        except configparser.Error as e:
            Logger.app.error("Error reading {} {}".format(config_file, e))

        try:
            if not encryp_value:
                return None
            if encryp_value[:2] == "e$":
                decryp_value = self.__decrypt__(encryp_value)
                return decryp_value
        except UnboundLocalError as e:
            Logger.console.info("Incorrect user name or password!")

        return encryp_value

    def set(self, ini, section, key, value):
        encryp_value = self.__encrypt__(value)
        config_file = self.__get_ini_file__(ini)
        try:
            self.config.read(config_file)
            self.config.set(section, key, "e$Fernet$" + encryp_value.decode())
            with open(config_file, 'w') as new_config:
                self.config.write(new_config)

        except (configparser.NoOptionError, CalledProcessError) as noe:
            Logger.app.error(
                "{} has incorrect or missing values, see log file {}".format(config_file, Logger.app_logfile))
            sys.exit(1)
        except configparser.Error as e:
            Logger.console.error("Error reading {}, see log file: {}".format(config_file, Logger.app_logfile))
            Logger.app.error("Error reading {} {}".format(config_file, e))
            sys.exit(1)
        return True

    def clear_credentials(self, ini, section, username_key, password_key):
        config_file = self.__get_ini_file__(ini)
        try:
            self.config.read(config_file)
            self.config.set(section, username_key, '')
            self.config.set(section, password_key, '')
            with open(config_file, 'w') as new_config:
                self.config.write(new_config)

        except (configparser.NoOptionError, CalledProcessError) as noe:
            Logger.app.error(
                "{} has incorrect or missing values, see log file {}".format(config_file, Logger.app_logfile))
            sys.exit(1)
        except configparser.Error as e:
            Logger.console.error("Error reading {}, see log file: {}".format(config_file, Logger.app_logfile))
            Logger.app.error("Error reading {} {}".format(config_file, e))
            sys.exit(1)
        return True

    def verify_secret(self):
        if self.secret_exists():
            return True
        else:
            self.write_secret()

    def secret_exists(self):
        # TODO: Refactor to config option in webbreaker.ini
        home = expanduser("~")
        secret_path = os.path.join(home, '.webbreaker')
        return os.path.isfile(secret_path)

    def wipe_all_credentials(self):
        # TODO if any other values are encrypted, make sure to add them here
        self.clear_credentials('fortify', 'fortify', 'fortify_username', 'fortify_password')

    def write_secret(self, overwrite=False):
        # TODO: Refactor to config option in webbreaker.ini
        home = expanduser("~")
        secret_path = os.path.join(home, '.webbreaker')
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
        # TODO: Refactor to config option in webbreaker.ini
        home = expanduser("~")
        secret_path = os.path.join(home, '.webbreaker')
        try:
            with open(secret_path, 'r') as secret_file:
                fernet_key = secret_file.readline().strip()
            return fernet_key
        except IOError:
            Logger.console.error("Error retrieving Fernet key.")
            sys.exit(1)

    def __get_ini_file__(self, ini):
        if ini == 'webbreaker':
            return self.webbreaker_ini
        if ini == 'fortify':
            return self.fortify_ini
        if ini == 'webinspect':
            return self.webinspect_ini
