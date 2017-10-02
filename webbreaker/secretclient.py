#!/usr/bin/env python
# -*- coding: utf-8 -*-

try:
    import ConfigParser as configparser
except ImportError: #Python3
    import configparser
from subprocess import CalledProcessError
import os
import sys
import re
from webbreaker.webbreakerlogger import Logger
from cryptography.fernet import Fernet





class SecretClient(object):
    def __init__(self):
        self.fernet_key = self.__read_fernet_secret__()
        self.webbreaker_ini = os.path.abspath(os.path.join('webbreaker', 'etc', 'webbreaker.ini'))
        self.fortify_ini = os.path.abspath(os.path.join('webbreaker', 'etc', 'fortify.ini'))
        self.webinspect_ini = os.path.abspath(os.path.join('webbreaker', 'etc', 'webinspect.ini'))
        try: # Python 2
            self.config = configparser.SafeConfigParser()
        except NameError: # Python 3
            self.config = configparser.ConfigParser()


    def get(self, ini, section, key):
        config_file = self.__get_ini_file__(ini)
        self.config.read(config_file)
        try:
            encryp_value = self.config.get(section, key)
        except configparser.NoSectionError:
            return None
        except (configparser.NoOptionError, CalledProcessError) as noe:
            Logger.console.error("{} has incorrect or missing values {}".format(config_file, noe))
        except configparser.Error as e:
            Logger.app.error("Error reading {} {}".format(config_file, e))

        if not encryp_value:
            return None
        if encryp_value[:2] == "e$":
            decryp_value = self.__decrypt__(encryp_value)
            return decryp_value

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
            Logger.app.error("{} has incorrect or missing values, see log file {}".format(config_file, Logger.app_logfile))
            sys.exit(1)
        except configparser.Error as e:
            Logger.console.error("Error reading {}, see log file: {}".format(config_file, Logger.app_logfile))
            Logger.app.error("Error reading {} {}".format(config_file, e))
            sys.exit(1)
        return True


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
            except ValueError as e:
                Logger.console.error(
                    "Error decrypting the Fortify token.  Exiting now, see log {}!".format(Logger.app_logfile))
                Logger.app.debug(e)
                sys.exit(1)
        else:
            Logger.console.error("Error decrypting.  Unsupported encryption version")
            sys.exit(1)

        return decryp_value



    def __read_fernet_secret__(self):
        try:
            with open(".webbreaker", 'r') as secret_file:
                fernet_key = secret_file.readline().strip()
            Logger.app.debug("Fernet key found. Attempting decryption of Fortify token")
            return fernet_key
        except IOError:
            Logger.console.error("Error retrieving Fernet key, file does not exist. Please run 'python "
                                 "setup.py secret' to reset")
            sys.exit(1)

    def __get_ini_file__(self, ini):
        if ini == 'webbreaker':
            return self.webbreaker_ini
        if ini == 'fortify':
            return self.fortify_ini
        if ini == 'webinspect':
            return self.webinspect_ini