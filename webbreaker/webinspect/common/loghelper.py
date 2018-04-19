from webbreaker.common.webbreakerlogger import Logger


class WebInspectLogHelper(object):

    def __init__(self):
        pass

    def log_error_webinspect_download(self, e):
        Logger.app.error("Please refer to the --help on the option value you provided.".format(e))

    def log_error_uploading(self, args, e):
        Logger.app.error("Error uploading {} {}".format(args, e))

    def log_no_webinspect_server_found(self, e):
        Logger.app.error("No WebInspect server was found: {}!".format(e))

    def log_configuration_incorrect(self, args):
        Logger.app.error(
            "Your configuration or settings are incorrect see log: ERROR: {}!!!".format(args))

    def log_error_in_options(self, e):
        Logger.app.error("There was an error in the options provided!: ".format(e))

    def log_no_settings_file(self, e):
        Logger.app.error("The setting file does not exist: {}".format(e))

    def log_error_scan_policy(self, e):
        Logger.app.error("There was an error with the policy provided from --scan_policy option! ".format(e))

    def log_error_settings(self, args, e):
        Logger.app.error("The {0} is unable to be assigned! {1}".format(args, e))

    def log_scan_error(self, scan_name, e):
        Logger.app.error("The {0} is unable to be created! {1}".format(scan_name, e))

    def log_config_file_unavailable(self, e):
        Logger.app.error("Either your SSL or Config files are not available: {}".format(e))

    def log_webinspect_config_issue(self, e):
        Logger.app.error("Uh oh something is wrong with your WebInspect configurations!!\nError: {}".format(e))

    def log_git_access_error(self, args, e):
        Logger.app.critical("{} does not have permission to access the git repo: {}".format(args, e))

    def log_error_incorrect_webinspect_configs(self, args):
        Logger.app.error("Incorrect webinspect config values: {}".format(args))