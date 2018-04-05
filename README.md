[![Build Status](https://travis-ci.org/target/webbreaker.svg?branch=master)](https://travis-ci.org/target/webbreaker/builds)
[![Release](http://img.shields.io/github/release/target/webbreaker.svg)](https://github.com/target/webbreaker/releases/latest)
[![Versions](https://img.shields.io/pypi/pyversions/webinspectapi.svg)](https://img.shields.io/pypi/pyversions/webinspectapi.svg)
[![Open Hub statistics](https://www.openhub.net/p/webbreaker/widgets/project_thin_badge.gif)](https://www.openhub.net/p/webbreaker)

## Introduction

WebBreaker is an open source Dynamic Application Security Test Orchestration (DASTO) client, enabling development teams to create pipelines for security testing and automation of functional security tests, with WebInspect, Fortify SSC, and ThreadFix.

The commands are organized by product followed by actions you want to take on the product accompanied with options.  For example `webbreaker webinspect scan --settings=zerobank`

## Download & Install
 [ ![Download](https://api.bintray.com/packages/webbreaker/webbreaker-cli/webbreaker/images/download.svg) ](https://bintray.com/webbreaker/webbreaker-cli/webbreaker/_latestVersion)

:arrow_down: [Mac OS](https://github.com/target/webbreaker/releases), Mac installation is available on tap @ [homebrew](https://brew.sh) - COMING SOON

`brew install webbreaker`

:arrow_down: [CentOS/RedHat/Fedora](https://github.com/target/webbreaker/releases), Linux installation is available @ [artifactory](https://bintray.com/webbreaker/webbreaker-cli/webbreaker/)

`yum install webbreaker`

:arrow_down: [Windows 7](https://github.com/target/webbreaker/releases), Windows installation is available @ [Chocolatey](https://chocolatey.org) - COMING SOON

`choco install webbreaker`

:arrow_down: [Build and install](https://github.com/target/webbreaker.git) from source and follow the steps below.

1. ```git clone https://github.com/target/webbreaker```
1. ```export PATH=$PATH:$PYTHONPATH```
1. ```cd webbreaker;pip install -r requirements.txt```
1. ```python setup.py build```
1. ```python setup.py install```


## Configuration
:white_check_mark: Add your webbreaker executable to your $PATH or %PATH%

:white_check_mark: First time installs, run the `webbreaker` command in your terminal to create the default configurations `$HOME/.webbreaker/config.ini`

:white_check_mark: Configure the `$HOME/.webbreaker/config.ini` or `%USERPROFILE%\.webbreaker\config.ini`

:white_check_mark: Each supported product Webinspect, Fortify SSC, WebInspect and ThreadFix has a section. Modify the ones you need.

```
# Your Fortify SSC URL exclude /ssc and run `webbreaker admin credentials --fortify` 
[fortify]
ssc_url = https://ssc.example.com
username = 
password = 

# Your ThreadFix URL and ThreadFix API Key
[threadfix]
host = https://threadfix.example.com:8443/threadfix
api_key = ZfO0b7dotQZnXSgkMOEuQVoFIeDZwd8OEQE7XXX

# API authentication set to `true` and run `webbreaker admin credentials --webinspect`
[webinspect]
authenticate = false
username = 
password = 

# Webinspect default port is 8083/tcp. Feel free to add more servers here
server_01 = https://webinspect-1.example.com:8083
server_02 = https://webinspect-2.example.com:8083
endpoint_01 = %(server_01)s|%(size_large)s
endpoint_02 = %(server_01)s|%(size_medium)s
```
**NOTES:**
* If you are using WebInspect turn-on your [WebInspect API Service](https://software.microfocus.com/en-us/software/webinspect).  

## Release Notes

New Features, bugs and enhancements for this release are documented in our [WebBreaker Release Notes](docs/release.md)

## Usage

WebBreaker is a command-line interface (CLI) client.  See our complete [_WebBreaker Documentation_](https://target.github.io/webbreaker/) for further configuration, usage, and installation.

Illustrated below is an example of a typical WebBreaker WebInspect scanning workflow from creation to triage.  Please see the [WebBreaker Cheatsheet](docs/cheatsheet.md) for further examples.

1. Starting WebInspect Proxy  
`webbreaker webinspect proxy --start --port=9001 --proxy_name=WEBINSPECT_SCAN_NAME`

1. Stopping WebInspect Proxy  
`webbreaker webinspect proxy --stop --proxy_name=WEBINSPECT_SCAN_NAME`

1. WebInspect Scanning from Proxy Results  
`webbreaker webinspect scan --settings=$WEBINSPECT_SCAN_NAME.xml --scan_name=WEBINSPECT_SCAN_NAME`

1. Uploading Scan Results to Threadfix  
`webbreaker threadfix upload --application WEBINSPECT --scan_file WEBINSPECT_SCAN_NAME.xml`

1. Uploading Scan Results to Fortify SSC  
`webbreaker fortify upload --fortify_user $FORTIFY_SSC_USER --fortify_password $FORTIFY_SSC_PASSWORD --version $WEBINSPECT_SCAN_NAME --scan_name $WEBINSPECT_SCAN_NAME`

## Bugs and Feature Requests

Found something that doesn't seem right or have a feature request? [Please open a new issue](https://github.com/target/webbreaker/issues/new/).

## Copyright and License

[![license](https://img.shields.io/github/license/target/webbreaker.svg?style=flat-square)](https://github.com/target/webbreaker/blob/master/LICENSE.txt)

Copyright 2018 Target Brands, Inc.

