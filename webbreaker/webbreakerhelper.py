#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from webbreaker.webbreakerlogger import Logger

class WebBreakerHelper(object):
    @classmethod
    def check_run_env(cls):
        jenkins_home = os.getenv('JENKINS_HOME', '')
        if jenkins_home:
            return "jenkins"
        return None


    @classmethod
    def help_description(cls):
        return """
SYNOPSIS:
webbreaker [webinspect|fortify] [list|scan|download|upload] [OPTIONS]

DESCRIPTION:
WebBreaker is a light-weight, scalable, distributed, and automated dynamic security testing framework with a rich
command set providing both high-level Product operations and Dynamic Application Security Test Orchestration (DASTO) on Products.

COMMANDS:
Webbreaker is separated into Upper ("Products") and Lower level ("Actions") commands with their respective options.

UPPER-LEVEL COMMANDS:
    webbreaker-fortify
    Administer WebInspect scan results with Fortify Software Security Center (SSC).  Available `Actions` are
    add, list, and upload.

    webbreaker-webinspect
    Select WebInspect as your commercial scanner or Dynamic Application Security Test (DAST) product.  Available  `Actions` are
    scan, list and download.

LOWER-LEVEL COMMANDS
    webbraker-list
    List current and past WebInspect scans.

    webbreaker-scan
    Create or launch a WebInspect scan from a fully licensed WebInspect server or host. Scan results are automatically
    downloaded in both XML and FPR formats.

    webbreaker-download
    Download or export a WebInspect scan locally.

    fortify-upload
    Upload a WebInspect scan to Fortify Software Security Center (SSC).

WEBINSPECT SCAN OPTIONS:
    --settings\tWebInspect scan configuration file, if no setting file\b
    is specified the Default file shipped with WebInspect will be used.\n

    --scan_name\tUsed for the command 'webinspect scan' as both a scan\b
    instance variable and file name.  Default value is WEBINSPECT-<random-5-alpha-numerics>,\b
     or Jenkins global environment variables may be declared, such as $BUILD_TAG.\n

    --scan_policy\tOverrides the existing scan policy from the value in the\b
    setting file from `--settings`, see `.config` for built-in values.  \b
    Any custom policy must include only the GUID.  Do NOT include the `.policy` extension.\n

    --login_macro\tOverrides the login macro declared in the original setting file from\b
    `--settings` and uploads it to the WebInspect server.\n

    --workflow_macros\tWorkflow macros are located under webbreaker/etc/webinspect/webmacros,\b
    all webmacro files end with a .webmacro extension, do NOT include the `webmacro` extension.\n

    --scan_mode\tAcceptable values are `crawl`, `scan`, or `all`.\n

    --scan_scope\tAcceptable values are `all`, `strict`, `children`, and `ancestors`.\n

    --scan_start\tAcceptable values are `url` or `macro`.\n

    --start_urls\tEnter a single url or multiples.  For example --start_urls\b
    http://test.example.com --start_urls http://test2.example.com\n

    --allowed_hosts\tHosts to scan, either a single host or a list of hosts separated by \b
    spaces. If not provided, all values from `--start_urls` will be used.\n

    --size\t WebInspect scan servers are managed with the `.config` file, however a\b
     medium or large size WebInspect server defined in the config can be explicitly declared with\b
    `--size medium` or `--size large`.\n

WEBINSPECT LIST OPTIONS:
    --server\tQuery a list of past and current scans from a specific WebInspect server or host.\n
    --scan_name\tLimit query results to only those matching a given scan name
    --protocol\tSpecify which protocol should be used to contact the WebInspect server. Valid protocols\b
    are 'https' and 'http'. If not provided, this option will default to 'https'\n

WEBINSPECT DOWNLOAD OPTIONS:
    --scan_name\tSpecify the desired scan name to be downloaded from a specific WebInspect server or host.\n
    --server\tRequired option for downloading a specific WebInspect scan.  Server must be appended to all\b
    WebInspect download Actions.\n
    --protocol\tSpecify which protocol should be used to contact the WebInspect server. Valid protocols\b
    are 'https' and 'http'. If not provided, this option will default to 'https'\n

FORTIFY LIST OPTIONS:
    --application\tProvides a listing of Fortify SSC Version(s) within a specific Application or Project.\n
    --fortify_user\tIf provided WebBreaker authenticates to Fortify using these credentials. If not provided\n
    --fortify_password\tWebBreaker attempts to use a secret from .config. If no secret is found our\b
    the secret is no longer valid, you will be prompted for these credentials.\n

FORTIFY UPLOAD OPTIONS:
    --fortify_user \tIf provided WebBreaker authenticates to Fortify using these credentials. If not provided\n
    --fortify_password\tWebBreaker attempts to use a secret for .config. If no secret is found our the secret is\b
    no longer valid, you will be prompted for these credentials.\n
    --application\tIf provided WebBreaker will look for version under this application name instead of the one\b
    provided in .config\n
    --version\tUsed for the command 'fortify upload' this option specifies the application version name and\b
    is used to both locate the file to be uploaded and the correct fortify application version\b
    to upload the file to.\n
    --scan_name\tIf the scan file you wish to upload has a different name then --version, this option can\b
    override which file WebBreaker uploads. Note: WebBreaker still assume the .fpr extension so\b
    it should not be included here\n
"""

