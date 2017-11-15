# WebBreaker Documentation

## Table of Contents
[Introduction](#introduction)

- [Description: `description`](#description)

[User Guide](#user-guide)

- [Installation `installation`](#installation)
- [Supported Features `supported_features`](#supported-features)
- [Usage `usage`](#usage)
- [Logging `logging`](#logging)
- [Testing `testing`](#testing)
- [Notifications `notifications`](#notifications)

[Configurations](#configurations)

- [Logging `logging_config`](#logging-config)
- [Notifications `email_config`](#notifications-config)
- [Email `email_config`](#email-config)
- [Fortify configuration: `fortify_config`](#fortify-config)
- [WebInspect `webinspect_config`](#webinspect-config)
- [Fortify `fortify_config`](#fortify-config)
- [WebBreaker `webbreaker_config`](#webbreaker-config)
- [ThreadFix `threadfix_config`](#threadfix-config)

[Verbose Cheatsheet: Webinspect `webinspect_cheatsheet`](#verbose-cheatsheet-webinspect)

- [Scan: `webinspect_scan`](#webinspect-scan)
- [Servers: `webinspect_servers`](#webinspect-servers)
- [List: `webinspect_list`](#webinspect-list)
- [Download: `webinspect_download`](#webinspect-download)

[Verbose Cheatsheet: Fortify `fortify_cheatsheet`](#verbose-cheatsheet-fortify)

- [List: `fortify_list`](#fortify-list)
- [Download: `fortify_download`](#fortify_download)
- [Upload: `fortify_upload`](#fortify-upload)
- [Scan: `fortify_scan`](#fortify-scan)

[Verbose Cheatsheet: ThreadFix `threadfix_cheatsheet`](#verbose-cheatsheet-threadfix)

- [Teams: `threadfix_teams`](#threadfix_teams)
- [Applications: `threadfix_applications`](#threadfix_applications)
- [Scans: `threadfix_scans`](#threadfix_scans)
- [Upload: `threadfix_upload`](#threadfix_upload)
- [Create App: `threadfix_create_app`](#threadfix_create_app)

[Verbose Cheatsheet: Admin `admin_cheatsheet`](#verbose-cheatsheet-admin)

- [Notifier: `admin_notifier`](#admin-notifier)
- [agent: `admin_agent`](#admin-agent)
- [Credentials: `admin_credentials`](#admin-credentials)
- [Secret: `admin_secret`](#admin-secret)

## Introduction `introduction`

### Description `description`
Build functional security testing, into your software development and release cycles! WebBreaker provides the capabilities to automate and centrally manage Dynamic Application Security Testing (DAST) as part of your DevOps pipeline.

## User Guide `user-guide`

### Installation: `installation`

#### Quick Local Installation 
Install WebBreaker from github.com.
* ```git clone https://github.com/target/webbreaker```
* ```export PATH=$PATH:$PYTHONPATH```
* ```pip install -r requirements.txt```
* ```python setup.py install```

#### Package Install
WebBreaker releases are packaged on github.com and can be installed locally.
* ```pip install -e git+https://github.com/target/webbreaker.git#egg=webbreaker```

### Supported Features: `supported_features`

* Jenkins global environmental variable inheritance with scan options.
* WebInspect REST API support for v9.30 and above. 
* Export both XML and FPR WebInspect formats to Fortify Software Security Center (SSC) or other compatible vulnerability management web applications for vulnerability analysis/triage.
* Ability to automatically upload scan results to Fortify SSC or other third-party vulnerability management software.
* Centrally administer all configurations required to launch WebInspect scans.
* Remotely query arbitrary policies, settings, webmacros, from any WebInspect deployment.
* Configurable property .ini files to support your [Foritfy](webbreaker/etc/fortify.ini) and [WebInspect](webbreaker/etc/webinspect.ini) deployments.
* Enterprise scalability with configurable Just-In-Time (JIT) scheduling to distribute your WebInspect scans between two (2) or greater sensors.
* ChatOps extensibility and [email notifications](webbreaker/etc/email.ini) on scan start and completion.
* Local [logging](webbreaker/etc/logging.ini) of WebInspect scan state.
* [Superset data visualization dashboard](https://github.com/airbnb/superset) support for scan status and performance.

### Usage `usage`
Webbreaker utilizes a structure of upper-level and lower-level commands to enable interaction with multiple 3rd party platforms. The two platforms currently supported are WebInspect and Fortfiy and they can be accessed using their respective upper-level commands. Webbreaker supports multiple functions for each platform which are accessed via lower-level commands. The current command structure is listed below.

- webbreaker
    - webinspect
        - scan
        - servers
        - list
        - download
    - fortify
        - list
        - upload
        - scan
        - download
    - admin
        - notifier
        - agent
        - credentials
        - secret
    - threadfix
        - teams
        - applications
        - scans
        - upload
        - create_app

A proper Webbreaker command utilizes the structure 'webbreaker [webinspect|fortify|admin] [lower-level command] [OPTIONS]'

### Logging `logging`
WebBreaker may be implemented with Elastic Stack for log aggregation. Recommended compenents include Filebeat agents installed on all WebInspect servers, forwarding to Logstash, and visualized in Kibana. General implementation details are [here](https://qbox.io/blog/welcome-to-the-elk-stack-elasticsearch-logstash-kibana/).  A recommended approach is to tag log events and queries with ```WebInspect``` and ```webbreaker```, but remember queries are case sensitive.

### Testing `testing`
#### Requirements
1. Be in your project root to run tests. 
    * ```pip install -rrequirements.txt```
2. Python2.7 and Python3.6 are currently tested in our tox.ini file
    * If you want to test it against your current version python, you can the other ways to test. Tox is suggested though. 
    
#### Tox
We use detox instead of tox for the speed of concurrent testing. With the speed of testing, comes a lack of coverage output
* ```detox```

Tox will allow you to see the coverage.py results.
* ```tox```

#### Other ways to test
These can test against your version of python without creating seperate virtualenv. For isolation of issues and ease of use it is suggested that you use tox. 
```
python setup.py install
pytest
```
```
python setup.py install
python setup.py test
```

### Notifications
WebBreaker provides notifications for start-scan and end-scan events. A simple publisher/subscriber pattern is implemented under the ```webbreaker/notifiers```.  A Reporter object will hold a collection of Notifiers, each of which implements a Notify function responsible for creating the desired notification. Currently, two notification types are implemented email and database.

The email notifier merges the provided event data into an HTML email message and sends the message. All SMTP-related settings are stored in [webbreaker/etc/email.ini](https://github.com/target/webbreaker/blob/master/webbreaker/etc/email.ini), and read during the webbreaker execution.

If an error occurs on behalf of the notifiers at any point during the process of creating or sending notifications, the event will be logged, without any interruption of WebBreaker execution or the WebInspect scan.

## Configurations

### Logging `logging_config`
WebBreaker may be implemented with Elastic Stack for log aggregation. Recommended compenents include Filebeat agents installed on all WebInspect servers, forwarding to Logstash, and visualized in Kibana. General implementation details are [here](https://qbox.io/blog/welcome-to-the-elk-stack-elasticsearch-logstash-kibana/).  A recommended approach is to tag log events and queries with ```WebInspect``` and ```webbreaker```, but remember queries are case sensitive.

The `webbreaker/etc/logging.ini` implements the standard Python logging facility, logs and events are created under `/tmp`.

#### File
*webbreaker/etc/logging.ini*

#### Example 
[See Python Logging](https://docs.python.org/3/library/logging.html)

### Notifications `notifications_config`
WebBreaker provides notifications for start-scan and end-scan events. A simple publisher/subscriber pattern is implemented under the ```webbreaker/notifiers```.  A Reporter object will hold a collection of Notifiers, each of which implements a Notify function responsible for creating the desired notification. Currently, two notification types are implemented email and database.

The email notifier merges the provided event data into an HTML email message and sends the message. All SMTP-related settings are stored in [webbreaker/etc/email.ini](https://github.com/target/webbreaker/blob/master/webbreaker/etc/email.ini), and read during the webbreaker execution.

If an error occurs on behalf of the notifiers at any point during the process of creating or sending notifications, the event will be logged, without any interruption of WebBreaker execution or the WebInspect scan.

### Email `email_config`
Notifications for start-scan and end-scan events. A simple publisher/subscriber pattern is implemented under the "notifiers" folder.

A Reporter object holds a collection of Notifier objects, each of which implements a Notify function responsible for creating the desired notification. Currently, two notification types are implemented email and database.

The email notifier merges the provided event data into an HTML email message and sends the message. All SMTP-related settings are stored in .emailrc, and read during program startup.

#### File
*webbreaker/etc/email.ini*

#### Example
````
[emailer]
smtp_host=smtp.example.com
smtp_port=25
from_address=webbreaker-no-reply@example.com
to_address=webbreaker-activity@example.com
email_template:<html>
              <head></head>
              <body></body>

[agent_emailer]
smtp_host = smtp.example.com
smtp_port = 25
from_address = webbreaker-no-reply@example.com
default_to_address = security-team@example.com
chatroom = Security Chat Room
email_template:<html>
              <head></head>
              <body></body>
              </html>
````

### WebInspect `webinspect_config`

#### Configuration `webinspect_config`
WebInspect scan configuration files for `settings`, `policies`, and `webmacros` are versioned and hosted from a GIT repository determined in `webbreaker/etc/webinspect.ini`.  Additionally, all WebInspect policies and servers are managed from this configuration file.  The section `[api endpoints]` provides a _Just-In-Time_ (JIT) scheduler or the ability to load balance scans amongst a WebInspect cluster.

##### File
*webbreaker/etc/webinspect.ini*

##### Example
```
[webinspect_policies]
AggressiveSQLInjection=032b1266-294d-42e9-b5f0-2a4239b23941
AllChecks=08cd4862-6334-4b0e-abf5-cb7685d0cde7
ApacheStruts=786eebac-f962-444c-8c59-7bf08a6640fd
Application=8761116c-ad40-438a-934c-677cd6d03afb
Assault=0a614b23-31fa-49a6-a16c-8117932345d8
Blank=adb11ba6-b4b5-45a6-aac7-1f7d4852a2f6
CriticalsAndHighs=7235cf62-ee1a-4045-88f8-898c1735856f
CrossSiteScripting=49cb3995-b3bc-4c44-8aee-2e77c9285038
Development=9378c6fa-63ec-4332-8539-c4670317e0a6
Mobile=be20c7a7-8fdd-4bed-beb7-cd035464bfd0
NoSQLAndNode.js=a2c788cc-a3a9-4007-93cf-e371339b2aa9
OpenSSLHeartbleed=5078b547-8623-499d-bdb4-c668ced7693c
OWASPTop10ApplicationSecurityRisks2013=48cab8a0-669e-438a-9f91-d26bc9a24435
OWASPTop10ApplicationSecurityRisks2007=ece17001-da82-459a-a163-901549c37b6d
OWASPTop10ApplicationSecurityRisks2010=8a7152d5-2637-41e0-8b14-1330828bb3b1
PassiveScan=40bf42fb-86d5-4355-8177-4b679ef87518
Platform=f9ae1fc1-3aba-4559-b243-79e1a98fd456
PrivilegeEscalation=bab6348e-2a23-4a56-9427-2febb44a7ac4
QA=5b4d7223-a30f-43a1-af30-0cf0e5cfd8ed
Quick=e30efb2a-24b0-4a7b-b256-440ab57fe751
Safe=def6a5b3-d785-40bc-b63b-6b441b315bf0
SOAP=a7eb86b8-c3fb-4e88-bc59-5253887ea5b1
SQLInjection=6df62f30-4d47-40ec-b3a7-dad80d33f613
Standard=cb72a7c2-9207-4ee7-94d0-edd14a47c15c
TransportLayerSecurity=0fa627de-3f1c-4640-a7d3-154e96cda93c

[api_endpoints]
large=2
medium=1
server01=https://webinspect-server-1.example.com:8083
server02=https://webinspect-server-2.example.com:8083
server03=https://webinspect-server-3.example.com:8083
server04=https://webinspect-server-4.example.com:8083
server05=https://webinspect-server-5.example.com:8083
server06=https://webinspect-server-6.example.com:8083
server07=https://webinspect-server-7.example.com:8083
server08=https://webinspect-server-8.example.com:8083
server09=https://webinspect-server-9.example.com:8083
server10=https://webinspect-server-10.example.com:8083
e01: %(server01)s|%(large)s
e02: %(server02)s|%(large)s
e03: %(server03)s|%(large)s
e04: %(server04)s|%(large)s
e05: %(server05)s|%(large)s
e06: %(server06)s|%(medium)s
e07: %(server07)s|%(medium)s
e08: %(server08)s|%(medium)s
e09: %(server09)s|%(medium)s
e10: %(server10)s|%(medium)s

[webinspect_size]
large=2
medium=1

[webinspect_default_size]
default=large

[configuration_repo]
git = git@github.com:target/webbreaker.git
dir = webbreaker/etc/webinspect/
```

#### Settings `webinspect_settings`
All WebInspect distributions are packaged with a `Default.xml` file that may be overridden and uploaded to the WebInspect deployment with the webbreaker option `--settings`.  The setting xml file contains all possible options for your scan including, a WebInspect scan including policy, workflow and/or login macro, scan depth, and allowed hosts.

*Note:* The `etc/webinspect.ini` property file contains a section `configuration_repo`, a unique GIT repo is defined by the user and is mutually exclusive from the WebBreaker source.  The assumption is each WebBreaker installation will have a unique GIT URL defined.  Upon each execution, the repo refreshes *all* settings file(s), assuming that there may be newly created, deletions, or modifications of settings files.  All settings files used in execution must reside in this respective repo under `etc/webinspect/settings`.

##### Directory
*webbreaker/etc/webinspect/settings*

#### Policies `webinspect_policies`
Grouping of proprietary WebInspect tests to perform.  Tests or rules are represented in an `xml` element with a `.policy` file extension.  Custom tests or Checks are mapped to a unique WebInspect ID.  The mapping for all policies shipped with WebInspect are mapped with their respective GUID under `etc/webinspect.ini` within the `[webinspect_policies]` section.

*Note:* All custom polices are automatically uploaded to the targeted WebInspect server and must be referenced as a GUID.  

The `etc/webinspect.ini` property file contains a section `configuration_repo`, a unique GIT repo is defined by the user and is mutually exclusive from the WebBreaker source.  The assumption is each WebBreaker installation will have a unique GIT URL defined.  Upon each execution, the repo refreshes *all* settings file(s), assuming that there may be newly created, deletions, or modifications of settings files.  All settings files used in execution must reside in this respective repo under `etc/webinspect/settings`.

##### Directory
*webbreaker/etc/webinspect/policies*

#### Webmacros: `webinspect_webmacros`
Proprietary functional recordings of either a login or workflow of the website to scan, both files are encoded and are not compatable with any 3rd party product.  If a website requires authentication the login webmacro is required otherwise WebInspect will not be able to test any page enforcing authentication.  The workflow macro is a recording of a base case functional use of the website and is optional.  Alernatively, a website can be scanned by providing a list of URLs in-scope to scan.

*Note:* The `etc/webinspect.ini` property file contains a section `configuration_repo`, a unique GIT repo is defined by the user and is mutually exclusive from the WebBreaker source.  The assumption is each WebBreaker installation will have a unique GIT URL defined.  Upon each execution, the repo refreshes *all* settings file(s), assuming that there may be newly created, deletions, or modifications of settings files.  All settings files used in execution must reside in this respective repo under `etc/webinspect/settings`.

##### Directory
*webbreaker/etc/webinspect/webmacros*

### Fortify `fortify_config`
#### Configuration `fortify_config`
Software Security Center (SSC) configuration file `webbreaker/etc/fortify.ini` administers communication with Fortify SSC, and other Application settings.  Both `Project Template` and `Application` are static values declared in `fortify.ini`.  The `--scan_name` value will be used as the SSC Version name, created within the `Application` specified in the `fortify.ini` illustrated below.

##### File
*webbreaker/etc/fortify.ini*

##### Example
```
[fortify]
fortify_url = http://localhost:8080/ssc
project_template = Prioritized High Risk Issue Template
application_name = WEBINSPECT
fortify_username =
fortify_password =
```

### WebBreaker `webbreaker_config`
#### Configuration `webbreaker_config`
Webbreaker configuration file `webbreaker/etc/webbreaker.ini` stores Git API auth token and url of a default WebBreaker Agent.

##### File
*webbreaker/etc/webbreaker.ini*

##### Example
```
[git]
token = this_is_my_super_secret_token
```

### ThreadFix `threadfix_config`

#### File
*webbreaker/etc/threadfix.ini*

#### Example
````
[threadfix]
host = https://our-threadfix.com/threadfix/
api_key = aBcDeFgHiJkLmNoPqRsTuVwXyZ123456789

````

## Verbose Cheatsheet: Webinspect `webinspect_cheatsheet`
### WebInspect Scan `webinspect_scan`
Launch a scan using the settings file important_site_auth.xml (WebBreaker assumes the .xml extension)
```
webbreaker webinspect scan --settings important_site_auth
```

Launch a scan using the settings file important_site_auth.xml (WebBreaker assumes the .xml extension) with the allowed hosts important-site.com and m.important-site.com
**Note: The start_urls, allowed_hosts, and workflow_macros options can all be used multiple times in this format**
```
webbreaker webinspect scan --settings important_site_auth --allowed_hosts important-site.com --allowed_hosts m.important-site.com
```

Launch a scan using a settings file found by absolute path instead of one downloaded from the webinspect.ini repo
```
webbreaker webinspect scan --settings /Users/Matt/Documents/important_site_auth
```
### WebInspect Servers `webinspect_servers`
List all servers found in webbreaker/etc/webinspect.ini
```
webbreaker webinspect servers
```

#### WebInspect List `webinspect_list`
List all scans (scan name, scan id, and scan status) found on the server webinspect-server-1.example.com:8083
```
webbreaker webinspect list --server webinspect-server-1.example.com:8083
```

List all scans (scan name, scan id, and scan status) found on the servers webinspect-server-1.example.com:8083 whose scan name matches the query 'important_site'
```
webbreaker webinspect list --server webinspect-server-1.example.com:8083 --scan_name important_site
```

List all scans (scan name, scan id, and scan status) found on the servers webinspect-server-1.example.com:8083 and webinspect-server-2.example.com:8083
```
webbreaker webinspect list --server webinspect-server-1.example.com:8083 --server webinspect-server-2.example.com:8083
```

List all scans (scan name, scan id, and scan status) found on the servers webinspect-server-1.example.com:8083 and webinspect-server-2.example.com:8083 whose scan name matches the query 'important_site'
```
webbreaker webinspect list --server webinspect-server-1.example.com:8083 --server webinspect-server-2.example.com:8083 --scan_name important_site
```

List all scans (scan name, scan id, and scan status) found on all servers listed in webbreaker/etc/webinspect.ini
```
webbreaker webinspect list
```

List all scans (scan name, scan id, and scan status) containing the query 'important_site' found on all servers listed in webbreaker/etc/webinspect.ini
```
webbreaker webinspect list --scan_name important_site
```

List all scans (scan name, scan id, and scan status) found on the server webinspect-server-1.example.com:8083. Interaction with server will use http instead of https.
```
webbreaker webinspect list --server webinspect-server-1.example.com:8083 --protocol http
```
#### WebInspect Downlaod `webinspect_download`
For these examples, assume the server has scans with names important_site_auth, important_site_api, important_site_internal

Download the results from the important_site_auth scan found on webinspect-server-2.example.com:8083 as an fpr file
```
webbreaker webinspect download --server webinspect-server-2.example.com:8083 --scan_name important_site_auth
```

Because multiple scan names on webinspect-server-2.example.com:8083 match 'important_site', this command will list them in output and no files will be downloaded
```
webbreaker webinspect download --server webinspect-server-2.example.com:8083 --scan_name important_site
```

Download the results of scan 'important_site_auth' from webinspect-server-2.example.com:8083 in xml format
```
webbreaker webinspect download --server webinspect-server-2.example.com:8083 --scan_name important_site_auth -x xml
```

Download WebInspect scan by ID. Scan will be downloaded as important_site_auth.fpr (This is helpful when multiple scans have the same_name):
```
webbreaker webinspect download --server webinspect-2.example.com:8083 --scan_name important_site_auth --scan_id my_important_scans_id
```

Download the results from the important_site_auth scan found on webinspect-server-2.example.com:8083 as an fpr file. All interaction with webinspect-server-2.example.com:8083 will use http instead of https
```
webbreaker webinspect download --server webinspect-server-2.example.com:8083 --scan_name important_site_auth --protocol http
```

## Verbose Cheatsheet: Fortify `fortify_cheatsheet`
#### Fortify List `fortify_list`

List all versions found on Fortify (using the url listed in fortify.ini). Authentication to Fortify will use the username and password I have stored as environment variables.
```
webbreaker fortify list --fortify_user $FORT_USER --fortify_password $FORT_PASS
```

List all versions found on Fortify (using the url listed in fortify.ini). User will be prompted for their username and password to authenticate to Fortify.
**Note: When username/password authentication is successful, Fortify will provide a token that is valid for 24 hours. WebBreaker encryptes this token and stores it in fortify.ini. As long as you have a valid token, you will not be prompted for your username and password.**
```
webbreaker fortify list
```

List all versions found on Fortify (using the url listed in fortify.ini) that belong to the application 'webinspect'
**Note: Fortify applications are also sometimes refered to as projects**
```
webbreaker fortify list --application webinspect
```

#### Fortify Download `fortify_download`
Download lastest .fpr scan from Fortify SSC with application/project & version name
```
webbreaker fortify download --application my_other_app --version important_site_auth
```

Download lastest .fpr scan from Fortify SSC with application/project from fortify.ini & version name
```
webbreaker fortify download --version important_site_auth
```

Download lastest .fpr scan from Fortify SSC with application/project & version name and command-line authentication
```
webbreaker fortify download --fortify_user $FORT_USER --fortify_password $FORT_PASS --application my_other_app --version important_site_auth
```

#### Fortify Upload `fortify_upload`

Upload the file important_site_auth.fpr to the important_site_auth version on Fortify (using the url listed in fortify.ini). User will be prompted for their username and password to authenticate to Fortify.
**Note: When username/password authentication is successful, Fortify will provide a token that is valid for 24 hours. WebBreaker encryptes this token and stores it in fortify.ini. As long as you have a valid token, you will not be prompted for your username and password.**
```
webbreaker fortify upload --version important_site_auth
```

Upload the file important_site_auth.fpr to the important_site_auth version on Fortify (using the url listed in fortify.ini). Authentication to Fortify will use the username and password I have stored as environment variables.
```
webbreaker fortify upload --fortify_user $FORT_USER --fortify_password $FORT_PASS --version important_site_auth
```

Upload the file important_site_auth.fpr to the important_site_auth version under the application my_other_app on Fortify. If --application is not provided, WebBreaker will use the application name found in fortify.ini
```
webbreaker fortify upload --application my_other_app --version important_site_auth
```

Upload the file auth_scan.fpr to the important_site_auth version on Fortify
```
webbreaker fortify upload --version important_site_auth --scan_name auth_scan
```

#### Fortify Scan `fortify_scan`

Retrieve and store Fortify Version url and Jenkins BuildID in agent.json. If application is not provided, WebBreaker will use the application in fortify.ini. User will be prompted for their username and password to authenticate to Fortify
```
webbreaker fortify scan --version important_site_auth --build_id my_latest_build
```

Retrieve and store Fortify Version url and Jenkins BuildID in agent.json with Fortify Application override. User will be prompted for their username and password to authenticate to Fortify
```
webbreaker fortify scan --application my_other_app --version important_site_auth --build_id my_latest_build
```

Retrieve and store Fortify Version url and Jenkins BuildID with command-line authentication. Authentication to Fortify will use the username and password I have stored as environment variables
```
webbreaker fortify scan --version important_site_auth --build_id my_latest_build --fortify_user $FORT_USER --fortify_password $FORT_PASS
```

## Verbose Cheatsheet: ThreadFix `threadfix_cheatsheet`
#### ThreadFix Teams `threadfix_teams`
List all teams (ID and Name) found in ThreadFix
```
webbreaker threadfix teams
```

#### ThreadFix Applications `threadfix_applications`
List all applications (ID and Name) found in ThreadFix that belong to the team with ID=123
```
webbreaker threadfix applications --team_id 123
```

#### ThreadFix Scans `threadfix_scans`
List all scans (ID Scanner, and Filename) found in ThreadFix that belong to the application with ID=345
```
webbreaker threadfix scans --app_id 345
```

#### ThreadFix Upload `threadfix_upload`
Upload the local file 'my_app_scan.xml' as a scan to the application with ID=345
```
webbreaker threadfix upload --app_id 345 --scan_file my_app_scan.xml
```

#### ThreadFix Create App `threadfix_create_app`
Create a new application, with a given name and url, in ThreadFix under the team with ID=123
```
webbreaker threadfix create_app --team_id 123 --name new_marketing_app --url http://marketing.ourapp.com
```

## Verbose Cheatsheet: Admin `admin_cheatsheet`
#### Admin Notifier `admin_notifier`

Retrieve and store public emails of contributors to the webbreaker repo. Communication with the Git API requires a token stored in webbreaker.ini
```
webbreaker admin notifier --email --git_url https://github.com/target/webbreaker
```

#### Admin Agent `admin_agent`

View the current stored information for WebBreaker Agent based on most recent use of 'admin notifier' and 'fortify scan'
```
webbreaker admin agent
```

Create a WebBreaker Agent to monitor the Fortify Cloudscan specified in 'fortify scan'. On scan completion the agent will notify contributors found via 'admin notifiers':
```
webbreaker admin agent --start
```

#### Admin Credentials `admin_credentials`

Encrypt and store new Fortify credentials. User will be prompted for username and password. Credentials are validated before being stored.
```
webbreaker admin credentials --fortify
```

Encrypt and store new Fortify credentials passed as environment variables. Credentials are validated before being stored.
```
webbreaker admin credentials --fortify --username $FORT --password $FORT_PASS
```

Clear cuurent stored Fortify credentials.
```
webbreaker admin credentials --fortify --clear
```

#### Admin Secret `admin_secret`
A new encryption key is created and all stored credentials are cleared. Through regular use you should not need to use this command. However, if WebBreaker is having troubles with encrypting credentials, this command will help it reset.
```
webbreaker admin secret
```

A new encryption key is created and all stored credentials are cleared. You will not be prompted to confirm this command.
```
webbreaker admin secret [-f / --force]
```