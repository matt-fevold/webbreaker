[![Build Status](https://travis-ci.org/target/webbreaker.svg?branch=master)](https://travis-ci.org/target/webbreaker/builds)
[![Release](http://img.shields.io/github/release/target/webbreaker.svg)](https://github.com/target/webbreaker/releases/latest)
[![Versions](https://img.shields.io/pypi/pyversions/webinspectapi.svg)](https://img.shields.io/pypi/pyversions/webinspectapi.svg)
[![Open Hub statistics](https://www.openhub.net/p/webbreaker/widgets/project_thin_badge.gif)](https://www.openhub.net/p/webbreaker)
[![Coverage Status](https://coveralls.io/repos/github/target/webbreaker/badge.svg?branch=master)](https://coveralls.io/github/target/webbreaker?branch=master)

## Introduction

WebBreaker is an open source Dynamic Application Security Test Orchestration (DASTO) client, enabling development teams to release secure software with continuous delivery, visibility, and scalability.

Create pipelines with integrating a portfolio of web application security testing products, such as WebInspect, Fortify SSC, and ThreadFix.

## Download & Install
[![Download](https://api.bintray.com/packages/webbreaker/webbreaker-cli/webbreaker/images/download.svg?version=2.0.09)](https://bintray.com/webbreaker/webbreaker-cli/webbreaker/2.0.09/link)

:arrow_down: [Mac OS](https://github.com/target/webbreaker/releases), Mac installation is available on tap @ [homebrew](https://brew.sh) - COMING SOON

`brew install webbreaker`

:arrow_down: [CentOS/RedHat/Fedora](https://github.com/target/webbreaker/releases), Linux installation is available @ [artifactory](https://bintray.com/webbreaker/webbreaker-cli/webbreaker/)

`yum install webbreaker`

:arrow_down: [Windows 7](https://github.com/target/webbreaker/releases), Windows installation is available @ [Chocolatey](https://chocolatey.org) - COMING SOON

`choco install webbreaker`

## Configuration
:white_check_mark: Add your webbreaker executable to your $PATH or %PATH%

:white_check_mark: Configure `$HOME/.webbreaker/config.ini` or `%USERPROFILE%\.webbreaker\config.ini`

:white_check_mark: Each supported product Webinspect, Fortify SSC, and ThreadFix has a section. Modify the ones you need.

```
# Your Fortify SSC URL without /ssc
[fortify]
ssc_url = https://ssc.example.com

# Your Threadfix URL
[threadfix]
host = https://threadfix.example.com:8443/threadfix
api_key = ZfO0b7dotQZnXSgkMOEuQVoFIeDZwd8OEQE7XXX

# Your Webinspect installation, default port is 8083/tcp. Feel free to add more servers here
[webinspect]
server_01 = https://webinspect.example.com:8083
endpoint_01 = %(server_01)s|%(size_large)s
```
**NOTES:**
* If you are using WebInspect turn-on your [WebInspect API Service](https://software.microfocus.com/en-us/software/webinspect).  Go to your Swagger doc for validation https://webinspecct.example.com:8083/webinspect/api

## Release Notes

New Features, bugs and enhancements for this release are documented in our [WebBreaker Release Notes](docs/release.md)

## Usage

WebBreaker is a command-line interface (CLI) client.  See our complete [_WebBreaker Documentation_](https://target.github.io/webbreaker/) for further configuration, usage, and installation.

The CLI supports upper-level and lower-level commands with respective options to enable interaction with Dynamic Application Security Test (DAST) products.  Current supported products are WebInspect, Fortfiy, and ThreadFix (more to come in the future!!). 

Illustrated below is a fully automated WebBreaker workflow of a WebInspect Scan.  Please see the [WebBreaker Cheatsheet](docs/cheatsheet.md) for further examples.

1. Starting WebInspect Proxy
`webbreaker webinspect proxy --start --port=9001 --proxy_name=$WEBINSPECT_SCAN_NAME`

1. Stopping WebInspect Proxy
`webbreaker webinspect proxy --stop --proxy_name=$WEBINSPECT_SCAN_NAME`

1. WebInspect Scanning from Proxy Results
`webbreaker webinspect scan --settings=$WEBINSPECT_SCAN_NAME.xml --scan_name=$WEBINSPECT_SCAN_NAME`

1. Uploading Scan Results to Threadfix
`webbreaker threadfix upload --application DAST-Test --scan_file $WEBINSPECT_SCAN_NAME.xml`

1. Uploading Scan Results to Fortify SSC
`webbreaker fortify upload --fortify_user $FORTIFY_SSC_USER --fortify_password $FORTIFY_SSC_PASSWORD --version $WEBINSPECT_SCAN_NAME --scan_name $WEBINSPECT_SCAN_NAME`

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

## Bugs and Feature Requests

Found something that doesn't seem right or have a feature request? [Please open a new issue](https://github.com/target/webbreaker/issues/new/).

## Copyright and License

[![license](https://img.shields.io/github/license/target/webbreaker.svg?style=flat-square)](https://github.com/target/webbreaker/blob/master/LICENSE.txt)

Copyright 2017 Target Brands, Inc.
