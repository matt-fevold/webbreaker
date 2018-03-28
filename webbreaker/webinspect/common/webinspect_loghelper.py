from webbreaker.common.webbreakerlogger import Logger


class WebInspect_LogExceptionHelper(object):

    def __init__(self):
        pass

    def LogErrorWebInspectDownload(self, e):
        Logger.app.error("Please refer to the --help on the option value you provided.".format(e))

    def LogErrorUploading(self, args, e):
        Logger.app.error("Error uploading {} {}".format(args, e))

    def LogNoWebInspectServerFound(self, e):
        Logger.app.error("No WebInspect server was found: {}!".format(e))

    def LogConfigurationIncorrect(self, args):
        Logger.app.error(
            "Your configuration or settings are incorrect see log: ERROR: {}!!!".format(args))

    def LogErrorInOptions(self, e):
        Logger.app.error("There was an error in the options provided!: ".format(e))

    def LogNoSettingsFile(self, e):
        Logger.app.error("The setting file does not exist: {}".format(e))

    def LogScanPolicyError(self, e):
        Logger.app.error("There was an error with the policy provided from --scan_policy option! ".format(e))

    def LogSettingsError(self, args, e):
        Logger.app.error("The {0} is unable to be assigned! {1}".format(args, e))

    def LogScanError(self, scan_name, e):
        Logger.app.error("The {0} is unable to be created! {1}".format(scan_name, e))

    def LogConfigFileUnavailable(self, e):
        Logger.app.error("Either your SSL or Config files are not available: {}".format(e))

    def LogWebInspectConfigIssue(self, e):
        Logger.app.error("Uh oh something is wrong with your WebInspect configurations!!\nError: {}".format(e))

    def LogGitAccessError(self, args, e):
        Logger.app.critical("{} does not have permission to access the git repo: {}".format(args, e))