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

    def log_error_fetch_webinspect_configs(self):
        Logger.app.error("Fetching webinspect config")

    def log_error_not_running_scan(self):
        Logger.app.error("This scan has entered a non-running state, Exiting now!")

    def log_error_scan_overrides_parsing_error(self, e):
        Logger.app.error("Something went wrong processing the scan overrides: {}".format(e))

    def log_info_using_webinspect_server(self, server):
        Logger.app.info("Using webinspect server: -->{}<-- for query".format(server))

    def log_info_scan_start(self, endpoint, scan_id):
        Logger.app.info('WebInspect scan launched on {0} your scan id: {1}\n'.format(endpoint, scan_id))

    def log_error_scan_start_failed(self, e):
        Logger.app.error("Creating the WebInspect scan failed! {}".format(e))

    def log_info_successful_scan_export(self, scan_name, extension):
        Logger.app.info('Scan results file is available: {0}.{1}\n'.format(scan_name, extension))

    def log_error_failed_scan_export(self, e):
        Logger.app.error('Error saving file locally! {}'.format(e))

    def log_error_get_scan_status(self, e):
        Logger.app.error("There was an error getting scan status: {}".format(e))

    def log_error_list_scans(self, e):
        Logger.app.error("There was an error listing WebInspect scans! {}".format(e))

    def log_error_policy_deletion(self, e):
        Logger.app.error("Verify if the deletion of existing policy failed: {}".format(e))

