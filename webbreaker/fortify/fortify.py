#!/usr/bin/env python
# -*- coding: utf-8 -*-

from webbreaker.fortify.fortifyclient import FortifyClient
from webbreaker.fortify.fortifyconfig import FortifyConfig
from exitstatus import ExitStatus
import sys
from webbreaker.common.webbreakerlogger import Logger
from webbreaker.common.authorization import auth_prompt


class Fortify:
    def __init__(self):
        self.config = None

    def _set_config_(self):
        self.config = FortifyConfig()

    def list(self, fortify_user, fortify_password, application):
        self.config = FortifyConfig()
        try:
            if fortify_user and fortify_password:
                Logger.app.info("Importing Fortify credentials")
                fortify_client = FortifyClient(fortify_url=self.config.ssc_url,
                                               fortify_username=fortify_user,
                                               fortify_password=fortify_password)
                self.config.write_username(fortify_user)
                self.config.write_password(fortify_password)
                Logger.app.info("Fortify credentials stored")
            else:
                Logger.app.info("No Fortify username or password provided. Checking config.ini for credentials")
                if self.config.has_auth_creds():
                    fortify_client = FortifyClient(fortify_url=self.config.ssc_url,
                                                   fortify_username=self.config.username,
                                                   fortify_password=self.config.password)
                    Logger.app.info("Fortify username and password successfully found in config.ini")
                else:
                    Logger.app.info("Fortify credentials not found in config.ini")
                    fortify_user, fortify_password = auth_prompt("Fortify")
                    fortify_client = FortifyClient(fortify_url=self.config.ssc_url,
                                                   fortify_username=fortify_user,
                                                   fortify_password=fortify_password)
                    self.config.write_username(fortify_user)
                    self.config.write_password(fortify_password)
                    Logger.app.info("Fortify credentials stored")
            if application:
                fortify_client.list_application_versions(application)
            else:
                fortify_client.list_versions()
            Logger.app.info("Fortify list has successfully completed")
        except ValueError:
            Logger.app.error("Unable to obtain a Fortify API token. Invalid Credentials")
            sys.exit(ExitStatus.failure)
        except (AttributeError, UnboundLocalError, TypeError) as e:
            Logger.app.critical("Unable to complete command 'fortify list': {}".format(e))
            sys.exit(ExitStatus.failure)

    def download(self, fortify_user, fortify_password, application, version):
        fortify_config = FortifyConfig()
        if application:
            fortify_config.application_name = application
        try:
            if fortify_user and fortify_password:
                Logger.app.info("Importing Fortify credentials")
                fortify_client = FortifyClient(fortify_url=fortify_config.ssc_url,
                                               project_template=fortify_config.project_template,
                                               application_name=fortify_config.application_name,
                                               fortify_username=fortify_user,
                                               fortify_password=fortify_password)
                fortify_config.write_username(fortify_user)
                fortify_config.write_password(fortify_password)
                Logger.app.info("Fortify credentials stored")
            else:
                Logger.app.info("No Fortify username or password provided. Checking config.ini for credentials")
                if fortify_config.has_auth_creds():
                    fortify_client = FortifyClient(fortify_url=fortify_config.ssc_url,
                                                   project_template=fortify_config.project_template,
                                                   application_name=fortify_config.application_name,
                                                   fortify_username=fortify_config.username,
                                                   fortify_password=fortify_config.password)
                    Logger.app.info("Fortify username and password successfully found in config.ini")
                else:
                    Logger.app.info("Fortify credentials not found in config.ini")
                    fortify_user, fortify_password = auth_prompt("Fortify")
                    fortify_client = FortifyClient(fortify_url=fortify_config.ssc_url,
                                                   project_template=fortify_config.project_template,
                                                   application_name=fortify_config.application_name,
                                                   fortify_username=fortify_user,
                                                   fortify_password=fortify_password)
                    fortify_config.write_username(fortify_user)
                    fortify_config.write_password(fortify_password)
                    Logger.app.info("Fortify credentials stored")
            version_id = fortify_client.find_version_id(version)
            if version_id:
                filename = fortify_client.download_scan(version_id)
                if filename:
                    Logger.app.info("Scan file for version {} successfully written to {}".format(version_id, filename))
                else:
                    Logger.app.error("Scan download for version {} has failed".format(version_id))
            else:
                Logger.app.error("No version matching {} found under {} in Fortify".format(version, application))
        except ValueError:
            Logger.app.error("Unable to obtain a Fortify API token. Invalid Credentials")
        except (AttributeError, UnboundLocalError) as e:
            Logger.app.critical("Unable to complete command 'fortify download': {}".format(e))

    def upload(self, fortify_user, fortify_password, application, version, scan_name):
        self._set_config_()

        # Fortify only accepts fpr scan files
        x = 'fpr'
        if application:
            self.config.application_name = application
        if not scan_name:
            scan_name = version
        try:
            if not fortify_user or not fortify_password:
                Logger.console.info("No Fortify username or password provided. Validating config.ini for secret")
                if self.config.has_auth_creds():
                    Logger.console.info("Fortify credentials found in config.ini")
                    fortify_client = FortifyClient(fortify_url=self.config.ssc_url,
                                                   project_template=self.config.project_template,
                                                   application_name=self.config.application_name, scan_name=version,
                                                   extension=x, fortify_username=self.config.username,
                                                   fortify_password=self.config.password)
                else:
                    Logger.console.info("Fortify credentials not found in config.ini")
                    fortify_user, fortify_password = auth_prompt("Fortify")
                    fortify_client = FortifyClient(fortify_url=self.config.ssc_url,
                                                   project_template=self.config.project_template,
                                                   application_name=self.config.application_name,
                                                   fortify_username=fortify_user,
                                                   fortify_password=fortify_password, scan_name=version,
                                                   extension=x)
                    self.config.write_username(fortify_user)
                    self.config.write_password(fortify_password)
                    Logger.console.info("Fortify credentials stored")
            else:
                fortify_client = FortifyClient(fortify_url=self.config.ssc_url,
                                               project_template=self.config.project_template,
                                               application_name=self.config.application_name,
                                               fortify_username=fortify_user,
                                               fortify_password=fortify_password, scan_name=version, extension=x)
                self.config.write_username(fortify_user)
                self.config.write_password(fortify_password)
                Logger.console.info("Fortify credentials stored")

            reauth = fortify_client.upload_scan(file_name=scan_name)

            if reauth == -2:
                # The given application doesn't exist
                Logger.console.critical(
                    "Fortify Application {} does not exist. Unable to upload scan.".format(application))

        except (IOError, ValueError) as e:
            Logger.console.critical("Unable to complete command 'fortify upload'\n Error: {}".format(e))
        except (UnboundLocalError):
            Logger.app.error("There are duplicate Fortify SSC Project Version names.  Please choose another one.")

