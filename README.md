[![Build Status](https://travis-ci.org/target/webbreaker.svg?branch=master)](https://travis-ci.org/target/webbreaker/builds)
[![Release](http://img.shields.io/github/release/target/webbreaker.svg)](https://github.com/target/webbreaker/releases/latest)
[![Versions](https://img.shields.io/pypi/pyversions/webinspectapi.svg)](https://img.shields.io/pypi/pyversions/webinspectapi.svg)
[![Open Hub statistics](https://www.openhub.net/p/webbreaker/widgets/project_thin_badge.gif)](https://www.openhub.net/p/webbreaker)
[![Coverage Status](https://coveralls.io/repos/github/target/webbreaker/badge.svg?branch=master)](https://coveralls.io/github/target/webbreaker?branch=master)

## Introduction

WebBreaker is an open source Dynamic Application Security Test Orchestration (DASTO) client, enabling development teams to release secure software with continuous delivery, visibility, and scalability.

Create pipelines with integrating a portfolio of web application security testing products, such as WebInspect, Fortify SSC, and ThreadFix.

## Download
[![Download](https://api.bintray.com/packages/webbreaker/webbreaker-cli/webbreaker/images/download.svg?version=2.0.03)](https://bintray.com/webbreaker/webbreaker-cli/webbreaker/2.0.03/link)

:arrow_down: [Mac OS](https://github.com/target/webbreaker/releases/download/2.0.03/webbreaker.dmg)]
:arrow_down: [CentOS/RedHat/Fedora](https://github.com/target/webbreaker/releases/download/2.0.03/webbreaker-2.0-03.el7.centos.x86_64.rpm)

## Configuration
:white_check_mark: Add your webbreaker executable to your $PATH or %PATH%

:white_check_mark: Configure `$HOME/.webbreaker/config.ini` or `%USERPROFILE%\.webbreaker\config.ini`

:white_check_mark: Each supported product Webinspect, Fortify SSC, and ThreadFix has a section. Modify the ones you need.


```
# Change to an absolute path
[webbreaker_install]
dir = .

# Your Fortify SSC URL without /ssc
[fortify]
ssc_url = https://ssc.example.com:8443

# Your Threadfix URL
[threadfix]
host = https://threadfix.example.com:8443/threadfix
api_key = ZfO0b7dotQZnXSgkMOEuQVoFIeDZwd8OEQE7XXX

# Your Webinspect installation, default port is 8083/tcp. Feel free to add more servers here
[webinspect_endpoints]
server01 = https://webinspect.example.com:8083
```
**NOTES:**
* Turn-on your [WebInspect API Service](https://software.microfocus.com/en-us/software/webinspect).

## Release Notes

New Features, bugs and enhancements for this release are documented in our [WebBreaker Release Notes](docs/release.md)

## Usage

WebBreaker is a command-line interface (CLI) client.  See our complete [_WebBreaker Documentation_](https://target.github.io/webbreaker/) for further configuration, usage, and installation.

The CLI supports upper-level and lower-level commands with respective options to enable interaction with Dynamic Application Security Test (DAST) products.  Currently, the two Products supported are WebInspect and Fortfiy (more to come in the future!!)

Below is a Cheatsheet of supported commands to get you started.  

---


    List all WebInspect servers found in .config - webinspect_endpoints:
    webbreaker webinspect servers

    List all WebInspect scans on webinspect-1.example.com and webinspect-2.example.com:
    webbreaker webinspect list --server webinspect-1.example.com:8083 --server webinspect-2.example.com:8083
    
    List all WebInspect scans on webinspect-1.example.com and webinspect-2.example.com matching "important_site":
    webbreaker webinspect list --server webinspect-1.example.com:8083 --server webinspect-2.example.com:8083 --scan_name important_site

    List all WebInspect scans on all servers:
    webbreaker webinspect list

    List all WebInspect scans on all servers matching "important_site":
    webbreaker webinspect list --scan_name important_site
    
    List with http:
    webbreaker webinspect list --server webinspect-1.example.com:8083 --protocol http

    Download WebInspect scan from server or sensor:
    webbreaker webinspect download --server webinspect-2.example.com:8083 --scan_name important_site_auth
    
    Download WebInspect scan as XML:
    webbreaker webinspect download --server webinspect-2.example.com:8083 --scan_name important_site_auth -x xml

    Download WebInspect scan by ID:
    webbreaker webinspect download --server webinspect-2.example.com:8083 --scan_name important_site_auth --scan_id my_important_scans_id
    
    Download WebInspect scan with http (no SSL):
    webbreaker webinspect download --server webinspect-2.example.com:8083 --scan_name important_site_auth --protocol http
    
    Basic WebInspect scan:
    webbreaker webinspect scan --settings important_site_auth
    
    Advanced WebInspect Scan with Scan overrides:
    webbreaker webinspect scan --settings important_site_auth --allowed_hosts example.com --allowed_hosts m.example.com
    
    Scan with local WebInspect settings:
    webbreaker webinspect scan --settings /Users/Matt/Documents/important_site_auth
    
    Initial Fortify SSC listing with authentication (SSC token is managed for 1-day):
    webbreaker fortify list --fortify_user matt --fortify_password abc123
    
    Interactive Listing of all Fortify SSC application versions:
    webbreaker fortify list
    
    List Fortify SSC versions by application (case sensitive):
    webbreaker fortify list --application WEBINSPECT
    
    Upload to Fortify SSC with command-line authentication:
    webbreaker fortify upload --fortify_user $FORT_USER --fortify_password $FORT_PASS --version important_site_auth
    
    Upload to Fortify SSC with interactive authentication & application version configured with .config file:
    webbreaker fortify upload --version important_site_auth --scan_name auth_scan
    
    Upload to Fortify SSC with application/project & version name:
    webbreaker fortify upload --application my_other_app --version important_site_auth --scan_name auth_scan

    Download lastest .fpr scan from Fortify SSC with application/project & version name:
    webbreaker fortify download --application my_other_app --version important_site_auth

    Download lastest .fpr scan from Fortify SSC with application/project from .config file & version name:
    webbreaker fortify download --version important_site_auth

    Download lastest .fpr scan from Fortify SSC with application/project & version name and command-line authentication:
    webbreaker fortify download --fortify_user $FORT_USER --fortify_password $FORT_PASS --application my_other_app --version important_site_auth

    Retrieve and store Fortify Version url and Jenkins BuildID:
    webbreaker fortify scan --version important_site_auth --build_id my_latest_build

    Retrieve and store Fortify Version url and Jenkins BuildID with Fortify Application override:
    webbreaker fortify scan --application my_other_app --version important_site_auth --build_id my_latest_build

    Retrieve and store Fortify Version url and Jenkins BuildID with command-line authentication:
    webbreaker fortify scan --version important_site_auth --build_id my_latest_build --fortify_user $FORT_USER --fortify_password $FORT_PASS

    List all applications for all teams found in ThreadFix
    webbreaker threadfix list

    List all applications with names containing 'secret' for all teams with names containing 'Marketing'
    webbreaker threadfix list --team Marketing --application MyApp

    List all applications and teams found in ThreadFix
    webbreaker threadfix list

    List all ThreadFix applications for the Marketing team
    webbreaker threadfix list --team Marketing

    Upload the local file 'my_app_scan.xml' as a scan to the application with ID=345
    webbreaker threadfix upload --application MyApp --scan_file my_app_scan.xml

    Upload the local file 'my_app_scan.xml' as a scan to the application with name Marketing_App
    webbreaker threadfix upload --application Marketing_App --scan_file my_app_scan.xml

    Create a new application, with a given name and url, in ThreadFix under the Marketing team
    webbreaker threadfix create --team Marketing --application new_marketing_app --url http://marketing.ourapp.com

    Retrieve and store public emails of contributors to the webbreaker repo:
    webbreaker admin notifier --email --git_url https://github.com/target/webbreaker

    View the current stored information for WebBreaker Agent based on most recent use of 'admin notifier' and 'fortify scan':
    webbreaker admin agent

    Create a WebBreaker Agent to monitor the Fortify Cloudscan specified in 'fortify scan'. On scan completion the agent will notify contributors:
    webbreaker admin agent --start

    Encrypt and store new Fortify credentials. User will be prompted for username and password.
    webbreaker admin credentials --fortify

    Encrypt and store new Fortify credentials passed as environment variables
    webbreaker admin credentials --fortify --username $FORT_USER --password $FORT_PASS

    Clear cuurent stored Fortify credentials.
    webbreaker admin credentials --fortify --clear



## Testing
Our automated testing is performed with tox and detox on Python 3.6 and 2.7. See the [full testing documentation](https://target.github.io/webbreaker/#testing).

## Docker 
Run WebBreaker in Docker from the repo's root directory, the pre-configured virtualenv environments are `venv27` for Python 2.7 or `venv36` for Python 3.6.  Examples are illustrated below.

```
docker build -t test_env:centos . \
&& docker create -it --name test_env test_env:centos  \
&& docker start test_env \
&& docker exec -it test_env bash
```
To remove the environment gracefully, perform the following command:
```
docker stop test_env && docker rm test_env
```

## Console Output

![WebBreaker](images/WebBreakerScreen.jpg)

## Bugs and Feature Requests

Found something that doesn't seem right or have a feature request? [Please open a new issue](https://github.com/target/webbreaker/issues/new/).

## Copyright and License

[![license](https://img.shields.io/github/license/target/webbreaker.svg?style=flat-square)](https://github.com/target/webbreaker/blob/master/LICENSE.txt)

Copyright 2017 Target Brands, Inc.
