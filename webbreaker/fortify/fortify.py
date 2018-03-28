#!/usr/bin/env python
# -*- coding: utf-8 -*-

from webbreaker.fortify.fortifyclient import FortifyClient
from webbreaker.fortify.fortifyconfig import FortifyConfig
from exitstatus import ExitStatus
import sys
from webbreaker.common.webbreakerlogger import Logger
from webbreaker.common.auth import auth_prompt
from webbreaker.common.logexceptionhelper import LogInfoHelper
from webbreaker.common.logexceptionhelper import LogExceptionHelper

logexceptionhelper = LogExceptionHelper()
loginfohelper = LogInfoHelper()


class Fortify:
    def __init__(self):
        self.config = None

    def _set_config_(self):
        self.config = FortifyConfig()

    def list(self, fortify_user, fortify_password, application):
        self.config = FortifyConfig()
        try:
            if fortify_user and fortify_password:
                loginfohelper.LogInfoFortifyImportCredentials()

                # Logger.app.info("Importing Fortify credentials")
                fortify_client = FortifyClient(fortify_url=self.config.ssc_url,
                                               fortify_username=fortify_user,
                                               fortify_password=fortify_password)
                self.config.write_username(fortify_user)
                self.config.write_password(fortify_password)
                loginfohelper.LogInfoFortifyCredentialStored()
            else:
                loginfohelper.LogInfoFortifyCheckConfig()

                if self.config.has_auth_creds():
                    fortify_client = FortifyClient(fortify_url=self.config.ssc_url,
                                                   fortify_username=self.config.username,
                                                   fortify_password=self.config.password)
                    loginfohelper.LogInfoFortifyCredentialsFound()
                else:
                    loginfohelper.LogInfoFortifyCredentialNotFound()
                    fortify_user, fortify_password = auth_prompt("Fortify")
                    fortify_client = FortifyClient(fortify_url=self.config.ssc_url,
                                                   fortify_username=fortify_user,
                                                   fortify_password=fortify_password)
                    self.config.write_username(fortify_user)
                    self.config.write_password(fortify_password)
                    loginfohelper.LogInfoFortifyCredentialStored()
            if application:
                fortify_client.list_application_versions(application)
            else:
                fortify_client.list_versions()
            loginfohelper.LogInfoFortifyListSuccess()
        except ValueError:
            logexceptionhelper.LogErrorFortifyAPIToken()

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
                loginfohelper.LogInfoFortifyImportCredentials()
                fortify_client = FortifyClient(fortify_url=fortify_config.ssc_url,
                                               project_template=fortify_config.project_template,
                                               application_name=fortify_config.application_name,
                                               fortify_username=fortify_user,
                                               fortify_password=fortify_password)
                fortify_config.write_username(fortify_user)
                fortify_config.write_password(fortify_password)
                loginfohelper.LogInfoFortifyCredentialStored()
            else:
                loginfohelper.LogInfoFortifyCheckConfig()
                if fortify_config.has_auth_creds():
                    fortify_client = FortifyClient(fortify_url=fortify_config.ssc_url,
                                                   project_template=fortify_config.project_template,
                                                   application_name=fortify_config.application_name,
                                                   fortify_username=fortify_config.username,
                                                   fortify_password=fortify_config.password)
                    loginfohelper.LogInfoFortifyCredentialsFound()
                else:
                    loginfohelper.LogInfoFortifyCredentialNotFound()
                    fortify_user, fortify_password = auth_prompt("Fortify")
                    fortify_client = FortifyClient(fortify_url=fortify_config.ssc_url,
                                                   project_template=fortify_config.project_template,
                                                   application_name=fortify_config.application_name,
                                                   fortify_username=fortify_user,
                                                   fortify_password=fortify_password)
                    fortify_config.write_username(fortify_user)
                    fortify_config.write_password(fortify_password)
                    loginfohelper.LogInfoFortifyCredentialStored()
            version_id = fortify_client.find_version_id(version)
            if version_id:
                filename = fortify_client.download_scan(version_id)
                if filename:
                    loginfohelper.LogInfoScanFileWrittenSuccess(version_id, filename)
                else:
                    logexceptionhelper.LogErrorScanDownloadVersionFail(version_id)
            else:
                logexceptionhelper.LogErrorNoVersionMatchFound(version, application)
        except ValueError:
            logexceptionhelper.LogErrorFortifyAPIToken()
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
                    # TODO check logging stuff
                    fortify_client = FortifyClient(fortify_url=self.config.ssc_url,
                                                   project_template=self.config.project_template,
                                                   application_name=self.config.application_name, scan_name=version,
                                                   extension=x, fortify_username=self.config.username,
                                                   fortify_password=self.config.password)
                else:
                    loginfohelper.LogInfoFortifyCredentialNotFound()
                    fortify_user, fortify_password = auth_prompt("Fortify")
                    fortify_client = FortifyClient(fortify_url=self.config.ssc_url,
                                                   project_template=self.config.project_template,
                                                   application_name=self.config.application_name,
                                                   fortify_username=fortify_user,
                                                   fortify_password=fortify_password, scan_name=version,
                                                   extension=x)
                    self.config.write_username(fortify_user)
                    self.config.write_password(fortify_password)
                    loginfohelper.LogInfoFortifyCredentialStored()
            else:
                fortify_client = FortifyClient(fortify_url=self.config.ssc_url,
                                               project_template=self.config.project_template,
                                               application_name=self.config.application_name,
                                               fortify_username=fortify_user,
                                               fortify_password=fortify_password, scan_name=version, extension=x)
                self.config.write_username(fortify_user)
                self.config.write_password(fortify_password)
                loginfohelper.LogInfoFortifyCredentialStored()

            reauth = fortify_client.upload_scan(file_name=scan_name)

            if reauth == -2:
                # The given application doesn't exist
                Logger.console.critical(
                    "Fortify Application {} does not exist. Unable to upload scan.".format(application))

        except (IOError, ValueError) as e:
            Logger.console.critical("Unable to complete command 'fortify upload'\n Error: {}".format(e))
        except (UnboundLocalError):
            logexceptionhelper.LogErrorDuplicateFortifySSC()

