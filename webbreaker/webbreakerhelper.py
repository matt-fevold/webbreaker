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
\33[92m
 _       __     __    ____                  __
| |     / /__  / /_  / __ )________  ____ _/ /_____  _____
| | /| / / _ \/ __ \/ __  / ___/ _ \/ __ `/ //_/ _ \/ ___/
| |/ |/ /  __/ /_/ / /_/ / /  /  __/ /_/ / ,< /  __/ /
|__/|__/\___/_.___/_____/_/   \___/\__,_/_/|_|\___/_/
\033[0m
"""

    @classmethod
    def banner(cls, text, ch=' ', length=78):
        spaced_text = ' %s ' % text
        banner = spaced_text.center(length, ch)
        return banner

    @classmethod
    def webinspect_proxy_desc(cls):
        return """

        """
    @classmethod
    def webbreaker_desc(cls):
        return """
        WebBreaker is an open source Dynamic Application Security Test Orchestration (DASTO) client, enabling development teams
        to release secure software with continuous delivery, visibility, and scalability..
        """

    @classmethod
    def webinspect_desc(cls):
        return """
        WebInspect is commercial software for Dynamic Application Security Testing (DAST) of Web applications
        and services.
        """

    @classmethod
    def webinspect_scan_desc(cls):
        return """
        Launch a WebInspect scan from the WebInspect RESTFul API with scan results downloaded locally in both XML
        and FPR formats.  For example:\n
        \033[91m
        webbreaker webinspect scan --settings important_wi_site
        \033[0m
        """

    @classmethod
    def webinspect_list_desc(cls):
        return """
        List WebInspect scans configured in the config.ini or from an explicit server option. All communication implies
        https unless http is specified.
        \033[91m
        webbreaker webinspect list
        \033[0m
        """

    @classmethod
    def webinspect_servers_desc(cls):
        return """
        List all configured WebInspect servers from the config.ini.  For Example:\n
        \033[91m
        webbreaker webinspect servers
        \033[0m
        """

    @classmethod
    def webinspect_download_desc(cls):
        return """
        Download or export a WebInspect scan file to the local file system from a WebInspect server or sensor.
        For example:\n
        \033[91m
        webbreaker webinspect download --server https://webinspect.example.com:8083 --scan_name important_wi_scan
        \033[0m
        """

    @classmethod
    def webinspect_proxy_start_desc(cls):
        return """
        Start a WebInspect proxy for creating a settings file and/or a workflow webmacro to scan a site.  For example:\n
        \033[91m
        webbreaker webinspect proxy --start --port=9001 --proxy_name=example_site
        \033[0m
        """

    @classmethod
    def webinspect_proxy_stop_desc(cls):
        return """
        Stop the WebInspect proxy and automatically pull the webmacro and setting file locally.  For example:\n
        \033[91m
        webbreaker webinspect proxy --stop --proxy_name=example_site
        \033[0m
        """

    @classmethod
    def fortify_desc(cls):
        return """
        Fortify's  Software Security Center (SSC) is a centralized management repository for both WebInspect and
        Fortify Sourceanalyzer (SCA) scan results.
        """

    @classmethod
    def fortify_download_desc(cls):
        return """
        Download a Fortify Sourceanalyzer (SCA) or WebInspect scan from a specified Project/Application Version.  All
        scan results are included in a .fpr file.  For example\n
        \033[91m
        webbreaker fortify download --application WEBINSPECT --version important_site
        \033[0m
        WARNING :: Do not specify fortify username and password using options unless you are willing to have
        your credentials in your terminal history. An interactive prompt is recommended to store command line credentials!
        """

    @classmethod
    def fortify_list_desc(cls):
        return """
        Interactive Listing of all Fortify SSC Project/Application Versions. For example:\n
        \033[91m
        webbreaker fortify list
        \033[0m
        WARNING :: Do not specify fortify username and & password using options unless you are willing to have
        your credentials in your terminal history. An interactive prompt is recommended to store command line credentials!
        """

    @classmethod
    def fortify_scan_desc(cls):
        return """
        Retrieve Fortify SSC Application Version URL and Jenkins $BUILD_ID in agent.json. If application
        is not provided, the default SSC Application/Project is declared in the config.ini under application_name.

        WARNING :: Do not specify fortify username and & password using options unless you are willing to have
        your credentials in your terminal history. An interactive prompt is recommended to store command line credentials!
        """

    @classmethod
    def fortify_upload_desc(cls):
        return """
        Upload a WebInspect .fpr scan to an explicit Fortify SSC Application/Project Version with '--version'
        For example:\n
        \033[91m
        webbreaker fortify upload --application WEBINSPECT --version important_site --scan_name example_com-abc
        \033[0m
        WARNING :: Do not specify fortify username and & password using options unless you are willing to have
        your credentials in your terminal history. An interactive prompt is recommended to store command line credentials!
        """

    @classmethod
    def admin_desc(cls):
        return """
        WebBreaker administrative commands for managing Fortify SSC, ThreadFix, and WebInspect credentials.
        """

    @classmethod
    def admin_notifier_desc(cls):
        return """
        Retrieve and store emails from a specified Github repo.  An OAuth Github token is typically required for this action
        under the config.ini
        """

    @classmethod
    def admin_agent_desc(cls):
        return """
        Poll the Fortify SSC Cloudscan API endpoint from a Fortify Sourceanalyzer Build ID and email the Github repo's
        contributors upon scan completion.
        """

    @classmethod
    def admin_credentials_desc(cls):
        return """
        Interactive prompt to encrypt and store Fortify SSC credentials.  For example:\n
        \033[91m
        webbreaker admin credentials --fortify
        \033[0m
        WARNING :: Do not specify username and & password using options unless you are willing to have
        your credentials in your terminal history. An interactive prompt is recommended to store command line credentials!
        """

    @classmethod
    def admin_secret_desc(cls):
        return """
        Creates an AES 128-bit encrypted symetric key and clears all stored credentials
        """

    @classmethod
    def threadfix_desc(cls):
        return """
        ThreadFix is the industry leading vulnerability resolution platform that provides
        a window into the state of application security programs for organizations that build software.
        """

    @classmethod
    def threadfix_application_desc(cls):
        return """
        List all applications for a given ThreadFix team. Either team name OR team_id is required. For example:\n
        \033[91m
        webbreaker threadfix list --team Marketing
        \033[0m
        """
    
    @classmethod
    def threadfix_create_desc(cls):
        return """
        Create a new application in ThreadFix. Use OPTIONS to specify application information.  For example:\n
        \033[91m
        webbreaker threadfix create --team MARKETING --application new_marketing_app --url http://marketing.example.com
        \033[0m
        """

    @classmethod
    def threadfix_list_desc(cls):
        return """
        List all applications across all teams. Use OPTIONS to specify either teams or applications to list.  For example:\n
        \033[91m
        webbreaker threadfix list
        \033[0m
        """

    @classmethod
    def threadfix_scan_desc(cls):
        return """
        List all application scans per ID, Scanner, and Filename in ThreadFix.  For example:\n
        \033[91m
        webbreaker threadfix list --team Marketing --application MyApp
        \033[0m
        """

    @classmethod
    def threadfix_team_desc(cls):
        return """
        List all team names with associated ThreadFix IDs.  For example:\n
        \033[91m
        webbreaker threadfix list --team Marketing
        \033[0m
        """

    @classmethod
    def threadfix_upload_desc(cls):
        return """
        Upload a scan from to a Team's Application in ThreadFix.  For example:\n
        \033[91m
        webbreaker threadfix upload --application new_marketing_app --scan_file webinspect_scan.xml
        \033[0m
        """

    @classmethod
    def email_template_config(cls):
        return """
<html>
<head></head>
<body>
<p>Hello,<br/><br/>
    The following scan has logged new activity:
<ul>
    <li>Attack traffic source: {0}</li>
    <li>Attack traffic target(s):</li>
    <ul>
        {4}
    </ul>
    <li>Scan name: {1}</li>
    <li>Scan ID: {2}</li>
    <li><b>Action: {3}</b></li>
</ul>
</p>
<p>
    Questions? Concerns? Please contact us in our Hipchat room, &quot;WebBreaker Activity&quot;,
    or <a href="mailto:webbreaker-team@example.com">email us</a>.
</p>

<p>
    Want to manage your subscription to these emails? Use <a
        href="http://wiki.example.com/index.php/GroupID">GroupID</a>, and
    add/remove yourself from webbreaker-activity.
</p>
</body>
</html>
        """
