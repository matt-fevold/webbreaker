#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os


class WebBreakerHelper(object):
    @classmethod
    def check_run_env(cls):
        jenkins_home = os.getenv('JENKINS_HOME', '')
        if jenkins_home:
            return "jenkins"
        return None

    @classmethod
    def ascii_motd(cls):
        return """
 _       __     __    ____                  __
| |     / /__  / /_  / __ )________  ____ _/ /_____  _____
| | /| / / _ \/ __ \/ __  / ___/ _ \/ __ `/ //_/ _ \/ ___/
| |/ |/ /  __/ /_/ / /_/ / /  /  __/ /_/ / ,< /  __/ /
|__/|__/\___/_.___/_____/_/   \___/\__,_/_/|_|\___/_/
"""

    @classmethod
    def banner(cls, text, ch=' ', length=78):
        spaced_text = ' %s ' % text
        banner = spaced_text.center(length, ch)
        return banner
    
    @classmethod
    def help_description(cls):
        return """
        WebBreaker is a light-weight, scalable, distributed, and automated dynamic security testing framework 
        with a rich command set providing both high-level Product operations and Dynamic Application Security 
        Test Orchestration (DASTO) on Products.
        """

    @classmethod
    def webinspect_desc(cls):
        return """
        WebInspect is Dynamic Application Security Testing (DAST) software for assessing security of Web applications 
        and Web services.
        """

    @classmethod
    def webinspect_scan_desc(cls):
        return """
        Create or launch a WebInspect scan from a fully licensed WebInspect server or host. Scan results are 
        automatically downloaded in both XML and FPR formats.
        """

    @classmethod
    def webinspect_list_desc(cls):
        return """
        List WebInspect scans. Default protocol is https. If no server is specified it will list all 
        scans from config.ini settings. 
        """

    @classmethod
    def webinspect_servers_desc(cls):
        return """
        List all WebInspect servers from config.ini.
        """

    @classmethod
    def webinspect_download_desc(cls):
        return """
        Download or export a WebInspect scan locally. Default protocol is https & default extension is 'fpr'.
        
        """

    @classmethod
    def fortify_desc(cls):
        return """
        Collaborative web application for managing WebInspect and Fortify SCA security bugs
        across the entire secure SDLC-from development to QA and through production.
        """

    @classmethod
    def fortify_download_desc(cls):
        return """
        Download the .fpr scan of an Fortify version using application/project & version name
        """

    @classmethod
    def fortify_list_desc(cls):
        return """
        Interactive Listing of all Fortify SSC application versions
        """

    @classmethod
    def fortify_scan_desc(cls):
        return """
        Retrieve and store Fortify Version url and Jenkins BuildID in agent.json. If application 
        is not provided, WebBreaker will use the application in fortify.ini
        """

    @classmethod
    def fortify_upload_desc(cls):
        return """
        Upload a WebInspect scan matching '--version' with a '.fpr' extension to Fortify 
        Security Center (SSC). 
        """

    @classmethod
    def admin_desc(cls):
        return """
        Administrative commands involving credentials and notifiers.       
        """

    @classmethod
    def admin_notifier_desc(cls):
        return """
        Retrieve and store public emails of contributors to the webbreaker repo.
        """

    @classmethod
    def admin_agent_desc(cls):
        return """
        View the current stored information for WebBreaker Agent based on most recent use of 
        'admin notifier' and 'fortify scan'.
        Create a WebBreaker Agent to monitor the Fortify scan specified in 'fortify scan'. 
        On scan completion the agent will notify contributors found via 'admin notifiers'
        """

    @classmethod
    def admin_credentials_desc(cls):
        return """
        Encrypt and store new Fortify credentials
        """

    @classmethod
    def admin_secret_desc(cls):
        return """
        Generates a new encryption key and clears all stored credentials
        """

    @classmethod
    def threadfix_desc(cls):
        return """
        Interaction with ThreadFix API.
        """

    @classmethod
    def threadfix_application_desc(cls):
        return """
        List all applications for a given ThreadFix team. Either team name OR team_id is required
        """
    @classmethod
    def threadfix_create_desc(cls):
        return """
        Create a new application in ThreadFix. Use OPTIONS to specify application information.
        """
    @classmethod
    def threadfix_list_desc(cls):
        return """
        List all applications across all teams. Use OPTIONS to specify either teams or applications to list.
        """
    @classmethod
    def threadfix_scan_desc(cls):
        return """
        List all scans (ID, Scanner, and Filename) of specified application in ThreadFix
        """
    @classmethod
    def threadfix_team_desc(cls):
        return """
        List all teams (ID and Name) found on ThreadFix
        """
    @classmethod
    def threadfix_upload_desc(cls):
        return """
        Upload a local specified scan file to an application in ThreadFix.
        """

# LOWER-LEVEL COMMANDS
#     webbraker-list
#
#
#     webbreaker-scan
#
#
#     webbreaker-download
#     .
#
#     fortify-upload
#
#
# WEBINSPECT SCAN OPTIONS:
#     --settings\tWebInspect scan configuration file, if no setting file\b
#     is specified the Default file shipped with WebInspect will be used.\n
#
#     --scan_name\tUsed for the command 'webinspect scan' as both a scan\b
#     instance variable and file name.  Default value is WEBINSPECT-<random-5-alpha-numerics>,\b
#      or Jenkins global environment variables may be declared, such as $BUILD_TAG.\n
#
#     --scan_policy\tOverrides the existing scan policy from the value in the\b
#     setting file from `--settings`, see `.config` for built-in values.  \b
#     Any custom policy must include only the GUID.  Do NOT include the `.policy` extension.\n
#
#     --login_macro\tOverrides the login macro declared in the original setting file from\b
#     `--settings` and uploads it to the WebInspect server.\n
#
#     --workflow_macros\tWorkflow macros are located under webbreaker/etc/webinspect/webmacros,\b
#     all webmacro files end with a .webmacro extension, do NOT include the `webmacro` extension.\n
#
#     --scan_mode\tAcceptable values are `crawl`, `scan`, or `all`.\n
#
#     --scan_scope\tAcceptable values are `all`, `strict`, `children`, and `ancestors`.\n
#
#     --scan_start\tAcceptable values are `url` or `macro`.\n
#
#     --start_urls\tEnter a single url or multiples.  For example --start_urls\b
#     http://test.example.com --start_urls http://test2.example.com\n
#
#     --allowed_hosts\tHosts to scan, either a single host or a list of hosts separated by \b
#     spaces. If not provided, all values from `--start_urls` will be used.\n
#
#     --size\t WebInspect scan servers are managed with the `.config` file, however a\b
#      medium or large size WebInspect server defined in the config can be explicitly declared with\b
#     `--size medium` or `--size large`.\n
#
# WEBINSPECT LIST OPTIONS:
#     --server\tQuery a list of past and current scans from a specific WebInspect server or host.\n
#     --scan_name\tLimit query results to only those matching a given scan name
#     --protocol\tSpecify which protocol should be used to contact the WebInspect server. Valid protocols\b
#     are 'https' and 'http'. If not provided, this option will default to 'https'\n
#
# WEBINSPECT DOWNLOAD OPTIONS:
#     --scan_name\tSpecify the desired scan name to be downloaded from a specific WebInspect server or host.\n
#     --server\tRequired option for downloading a specific WebInspect scan.  Server must be appended to all\b
#     WebInspect download Actions.\n
#     --protocol\tSpecify which protocol should be used to contact the WebInspect server. Valid protocols\b
#     are 'https' and 'http'. If not provided, this option will default to 'https'\n
#
# FORTIFY LIST OPTIONS:
#     --application\tProvides a listing of Fortify SSC Version(s) within a specific Application or Project.\n
#     --fortify_user\tIf provided WebBreaker authenticates to Fortify using these credentials. If not provided\n
#     --fortify_password\tWebBreaker attempts to use a secret from .config. If no secret is found our\b
#     the secret is no longer valid, you will be prompted for these credentials.\n
#
# FORTIFY UPLOAD OPTIONS:
#     --fortify_user \tIf provided WebBreaker authenticates to Fortify using these credentials. If not provided\n
#     --fortify_password\tWebBreaker attempts to use a secret for .config. If no secret is found our the secret is\b
#     no longer valid, you will be prompted for these credentials.\n
#     --application\tIf provided WebBreaker will look for version under this application name instead of the one\b
#     provided in .config\n
#     --version\tUsed for the command 'fortify upload' this option specifies the application version name and\b
#     is used to both locate the file to be uploaded and the correct fortify application version\b
#     to upload the file to.\n
#     --scan_name\tIf the scan file you wish to upload has a different name then --version, this option can\b
#     override which file WebBreaker uploads. Note: WebBreaker still assume the .fpr extension so\b
#     it should not be included here\n
# """
