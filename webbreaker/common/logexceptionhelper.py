#!/usr/bin/env python
# -*- coding: utf-8 -*-

from webbreaker.common.webbreakerlogger import Logger


# Okay - this will not look nice future person reading this. This needs to be fixed again after we
#   get our testing in a nicer spot - currently some tests check for logging output (not anything we've refactored
#   recently (~2.1.5)) but those will change as more work is done. TODO

class LogExceptionHelper(object):

    def __init__(self):
        pass

    #__main__
    def LogErrorGitCommand(self, args):
        Logger.app.error("Please install the git client or add it to your PATH variable ->"
                         " https://git-scm.com/download.  See log {}!!!".format(args))

    #ThreadFix
    def LogErrorNoTeam(self):
        Logger.app.error("No teams were found")

    def LogErrorNoTeamWithName(self, args):
        Logger.app.error("Unable to find team with name {}".format(args))

    def LogErrorSpecifyTeam(self):
        Logger.app.error("Please specify either a team or team_id")

    def LogErrorNoApplicationWithTeamId(self, args):
        Logger.app.error("No applications were found for team_id {}".format(args))

    def LogErrorNoTeamWithApplication(self, args):
        Logger.app.error("Unable to find team with application {}".format(args))

    def LogErrorApplicationNotCreated(self):
        Logger.app.error("Application was not created, either the application exists, invalid token, or Threadfix"
                         " is unavailable!! ")

    def LogErrorThreadfixResponse(self, args):
        Logger.app.error("{}\n".format(args) + "Threadfix exited")

    def LogErrorReading(self, args, e):
        Logger.app.error("Error reading {} {}".format(args, e))

    def LogErrorRetrievingApplication(self, args):
        Logger.app.error("Error retrieving application for team {}".format(args))

    def LogErrorRequestDownlaod(self, args):
        Logger.app.error("Error requesting download: {}".format(args))

    def LogErrorNoScansFoundWithAppId(self, args):
        Logger.app.error("No scans were found for app_id {}".format(args))

    def LogErrorSpecifyApplication(self, args):
        Logger.app.error("Please specify either an application or app_id! {}".format(args))

    def LogErrorThreadfixRetrieveFail(self):
        Logger.app.error("Failed to retrieve applications from ThreadFix")

    def LogErrorNoApplicationWithMatchingName(self, args):
        Logger.app.error("No application was found matching name {}".format(args))

    def LogErrorMultipleApplicationFound(self, args):
        Logger.app.error("Multiple applications were found matching name {}. "
                         "Please specify the desired ID from below.".format(args))

    def LogErrorScanFailToUpload(self):
        Logger.app.error("Scan file failed to upload!")

    def LogErrorAPITokenAssociatedWithLocalAccount(self):
        Logger.app.error("Possible cause could be your API token must be associated with a local account!!")

    #Fortify
    def LogErrorFortifyAPIToken(self):
        Logger.app.error("Unable to obtain a Fortify API token. Invalid Credentials")

    def LogErrorUnableToCreateProjectVersion(self):
        Logger.app.error("Unable to create new project version, see logs for details")

    def LogErrorScanDownloadVersionFail(self, args):
        Logger.app.error("Scan download for version {} has failed".format(args))

    def LogErrorNoVersionMatchFound(self, args, application):
        Logger.app.error("No version matching {} found under {} in Fortify".format(args, application))

    def LogErrorDuplicateFortifySSC(self):
        Logger.app.error("There are duplicate Fortify SSC Project Version names. Please choose another one.")

    def LogErrorFortifyCredentialsNotStored(self):
        Logger.app.error("Unable to validate Fortify credentials. Credentials were not stored")


class LogInfoHelper(object):

    def __init__(self):
        pass

    #__main__
    def LogInfoCredentialsStoreSuccess(self):
        Logger.app.info("Credentials stored successfully")

    def LogInfoWebInspectCredentialClearSuccess(self):
        Logger.app.info("Successfully cleared WebInspect credentials from config.ini")

    def LogInfoApplicationCreatedWithId(self, args):
        Logger.app.info("Application was successfully created with id {}".format(args))

    #Threadfix
    def LogInfoThreadfixScansListedSuccess(self):
        Logger.app.info("Successfully listed Threadfix scans")

    def LogInfoFindApplicationWithMatchingName(self, args):
        Logger.app.info("Attempting to find application matching name {}".format(args))

    def LogInfoUploadResp(self, args):
        Logger.app.info("{}".format(args))

    def LogInfoThreadfixListSuccess(self):
        Logger.app.info("ThreadFix List successfully completed")

    def LogInfoNoApplicationFound(self, args):
        Logger.app.info("No applications were found" + args)

    def LogInfoThreadfixApplicationListSuccess(self):
        Logger.app.info("Successfully listed threadfix applications")

    def LogInfoThreadfixTeamsListedSuccess(self):
        Logger.app.info("Successfully listed threadfix teams")


    #Fortify
    def LogInfoFortifyCredentialsClearSuccess(self):
        Logger.app.info("Successfully cleared fortify credentials from config.ini")

    def LogInfoFortifyCredentialStored(self):
        Logger.app.info("Fortify credentials stored")

    def LogInfoFortifyImportCredentials(self):
        Logger.app.info("Importing Fortify credentials")

    def LogInfoFortifyCheckConfig(self):
        Logger.app.info("No Fortify username or password provided. Checking config.ini for credentials")

    def LogInfoFortifyCredentialsFound(self):
        Logger.app.info("Fortify username and password successfully found in config.ini")

    def LogInfoFortifyCredentialNotFound(self):
        Logger.app.info("Fortify credentials not found in config.ini")

    def LogInfoFortifyListSuccess(self):
        Logger.app.info("Fortify list has successfully completed")

    def LogInfoScanFileWrittenSuccess(self, args, filename):
        Logger.app.info("Scan file for version {} successfully written to {}".format(args, filename))

