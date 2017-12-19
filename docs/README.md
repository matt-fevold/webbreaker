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

- [WebBreaker `webbreaker_config`](#webbreaker-config)
- [Fortify `fortify_config`](#fortify-config)
- [ThreadFix `threadfix_config`](#threadfix-config)
- [WebInspect `webinspect_config`](#webinspect-config)
- [Email `email_config`](#email-config)

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

- [List: `threadfix_list`](#threadfix_list)
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
        - list
        - teams
        - applications
        - scans
        - upload
        - create_app

A proper Webbreaker command utilizes the structure 'webbreaker [webinspect|fortify|admin] [lower-level command] [OPTIONS]'

### Logging `logging`
WebBreaker may be implemented with Elastic Stack for log aggregation. Recommended compenents include 
Filebeat agents installed on all WebInspect servers, forwarding to Logstash, and visualized in Kibana. General 
implementation details are [here](https://qbox.io/blog/welcome-to-the-elk-stack-elasticsearch-logstash-kibana/).  
A recommended approach is to tag log events and queries with ```WebInspect``` and ```webbreaker```, but remember 
queries are case sensitive.

### Testing `testing`
#### Requirements
1. Be in your project root to run tests. 
    * ```pip install -rrequirements.txt```
2. Python2.7 and Python3.6 are currently tested in our tox.ini file
    * If you want to test it against your current version python, you can the other ways to test. Tox is 
    suggested though. 
    
#### Tox
We use detox instead of tox for the speed of concurrent testing. With the speed of testing, comes a lack of 
coverage output
* ```detox```

Tox will allow you to see the coverage.py results.
* ```tox```

#### Other ways to test
These can test against your version of python without creating seperate virtualenv. For isolation of issues 
and ease of use it is suggested that you use tox. 
```
python setup.py install
pytest
```
```
python setup.py install
python setup.py test
```

### Notifications
WebBreaker provides notifications for start-scan and end-scan events. A simple publisher/subscriber 
pattern is implemented under the ```webbreaker/notifiers```.  A Reporter object will hold a collection
of Notifiers, each of which implements a Notify function responsible for creating the desired notification. 
Currently, two notification types are implemented email and database.

The email notifier merges the provided event data into an HTML email message and sends the message. All SMTP-related 
settings are stored in [webbreaker/etc/email.ini](https://github.com/target/webbreaker/blob/master/webbreaker/etc/email.ini)
, and read during the webbreaker execution.

If an error occurs on behalf of the notifiers at any point during the process of creating or sending 
notifications, the event will be logged, without any interruption of WebBreaker execution or the WebInspect scan.

## Configurations

This is a compelte example of what will be generated under ~/.webbreaker/config.ini on the first WebBreaker run

To import your own config file just put 'config.ini' into ~/.webbreaker/config.ini
### Example 
````
[fortify]
ssc_url = https://fortify.example.com
project_template = Prioritized High Risk Issue Template
application_name = WEBINSPECT
username = 
password = 

[threadfix]
host = https://threadfix.example.com:8443/threadfix
api_key = this_is_my_super_secret_api_key

[git]
token = this_is_my_super_secret_token

[webinspect_endpoints]
large = 2
medium = 1
server01 = https://webinspect-server.example.com:8083
e01 = %(server01)s|%(large)s

[webinspect_size]
large = 2
medium = 1

[webinspect_default_size]
default = large

[webinspect_repo]
git = git@github.com:automationdomination/webinspect.git

[webinspect_policies]
aggressivesqlinjection = 032b1266-294d-42e9-b5f0-2a4239b23941
allchecks = 08cd4862-6334-4b0e-abf5-cb7685d0cde7
apachestruts = 786eebac-f962-444c-8c59-7bf08a6640fd
application = 8761116c-ad40-438a-934c-677cd6d03afb
assault = 0a614b23-31fa-49a6-a16c-8117932345d8
blank = adb11ba6-b4b5-45a6-aac7-1f7d4852a2f6
criticalsandhighs = 7235cf62-ee1a-4045-88f8-898c1735856f
crosssitescripting = 49cb3995-b3bc-4c44-8aee-2e77c9285038
development = 9378c6fa-63ec-4332-8539-c4670317e0a6
mobile = be20c7a7-8fdd-4bed-beb7-cd035464bfd0
nosqlandnode.js = a2c788cc-a3a9-4007-93cf-e371339b2aa9
opensslheartbleed = 5078b547-8623-499d-bdb4-c668ced7693c
owasptop10applicationsecurityrisks2013 = 48cab8a0-669e-438a-9f91-d26bc9a24435
owasptop10applicationsecurityrisks2007 = ece17001-da82-459a-a163-901549c37b6d
owasptop10applicationsecurityrisks2010 = 8a7152d5-2637-41e0-8b14-1330828bb3b1
passivescan = 40bf42fb-86d5-4355-8177-4b679ef87518
platform = f9ae1fc1-3aba-4559-b243-79e1a98fd456
privilegeescalation = bab6348e-2a23-4a56-9427-2febb44a7ac4
qa = 5b4d7223-a30f-43a1-af30-0cf0e5cfd8ed
quick = e30efb2a-24b0-4a7b-b256-440ab57fe751
safe = def6a5b3-d785-40bc-b63b-6b441b315bf0
soap = a7eb86b8-c3fb-4e88-bc59-5253887ea5b1
sqlinjection = 6df62f30-4d47-40ec-b3a7-dad80d33f613
standard = cb72a7c2-9207-4ee7-94d0-edd14a47c15c
transportlayersecurity = 0fa627de-3f1c-4640-a7d3-154e96cda93c

[emailer]
# smnp email host, port and email addresses required for email functionality.
smtp_host=smtp.example.com
smtp_port=25
from_address=webbreaker-no-reply@example.com
to_address=webbreaker-no-reply@example.com
default_to_address =
chatroom =
email_template =
        <html>
        <head></head>
        <body>
        <p>Hello,<br /><br />
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
        or <a href="mailto:webbreaker-no-reply@target.com">email us</a>.
        </p>
        <p>
        Want to manage your subscription to these emails? Use <a href="http://wiki.example.com/tgtwiki/index.php/GroupID">GroupID</a>, and
        add/remove yourself from WebBreaker Activity.
        </p>
        </body>
        </html>
````

### WebBreaker `webbreaker_config`
Global settings for webbreaker.

####[webbreaker_install]
Directory where webbreaker is installed. The default is set to `.` to signify the current directory of webbreaker. 

*Note:* This will be moved to [webbreaker] `install`

####[git]
Stores Git API auth token and url of a default WebBreaker Agent.

*Note:* This will be moved to under [webbreaker]

### ThreadFix `threadfix_config`
#### Configuration `threadfix_config`
##### host
Threadfix host that will be used.

##### api_key
This api_key to authenticate ThreadFix actions

### Fortify `fortify_config`
#### Configuration `fortify_config`
Fortify SSC settings can be found under [fortify]

##### ssc_url
URL of the fortify server to contact

##### project_template
Static value

##### application_name
Static Value

##### fortify_username
Fortify username that will be used for authentication with ssc_url. It is stored using an encrypted value. Use 
`webbreaker admin credentials --fortify` to set your username & password.
##### fortify_password
Fortify username that will be used for authentication with ssc_url. It is stored using an encrypted value. Use 
`webbreaker admin credentials --fortify` to set your username & password.

### WebInspect `webinspect_config`

#### Configuration `webinspect_config`
WebInspect scan configuration files for `policies` are versioned and hosted from a GIT repository determined 
in `webbreaker/etc/webinspect.ini`.  Additionally, all WebInspect policies and servers are managed from this 
configuration file.  The section 

All WebInspect distributions are packaged with a `Default.xml` file that may be overridden and uploaded 
to the WebInspect deployment with the webbreaker option `--settings`.  The setting xml file contains 
all possible options for your scan including, a WebInspect scan including policy, workflow and/or login 
macro, scan depth, and allowed hosts.


####[webinspect_endpoints]
Provides a _Just-In-Time_ (JIT) scheduler or the ability to load balance scans amongst a WebInspect cluster.

Will be moving 'large' & 'medium' under [webinspect_size] in the future.

####[webinspect_size]
Sets the number for large and small WebInspect scan servers. This helps with _Just-In-Time_ (JIT) scheduling

####[webinspect_default_size]
Will be moved under [webinspect_size] in the future. 

####[webinspect_repo]
A unique GIT repo is defined by the user and is mutually exclusive from the WebBreaker source.  The 
assumption is each WebBreaker installation will have a unique GIT URL defined.  Upon each execution, 
the repo refreshes *all* settings file(s), assuming that there may be newly created, deletions, or modifications 
of settings files.  All settings files used in execution must reside in this respective repo 
under `etc/webinspect/settings`.

*Note:* dir will be deprecated

####[webinspect_policies]
Grouping of proprietary WebInspect tests to perform.  Tests or rules are represented in an `xml` element with 
a `.policy` file extension.  Custom tests or Checks are mapped to a unique WebInspect ID.  The mapping for all 
policies shipped with WebInspect are mapped with their respective GUID within the `[webinspect_policies]` section.

*Note:* All custom polices are automatically uploaded to the targeted WebInspect server and must be referenced 
as a GUID.  


### Email `email_config`
Notifications for start-scan and end-scan events. A simple publisher/subscriber pattern is implemented under 
the "notifiers" folder.

A Reporter object holds a collection of Notifier objects, each of which implements a Notify function responsible 
for creating the desired notification. Currently, two notification types are implemented email and database.

The email notifier merges the provided event data into an HTML email message and sends the message. All 
SMTP-related settings are stored in .emailrc, and read during program startup.

## Verbose Cheatsheet: Webinspect `webinspect_cheatsheet`
### WebInspect Scan `webinspect_scan`
##### Options

##### Commands
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
#### WebInspect Scan Options
##### Options

##### Commands

Specify name of scan --scan_name ${BUILD_TAG}
```--scan_name```

Specify name of settings file, without the .xml extension. WebBreaker will  by default try to locate this file in in the repo found in .config. If your file is not in the repo, you may instead pass an absolute path to the file
```--settings```

Size of scanner required. Valid values if provided are 'medium' or 'large'
```--size```

Overrides the setting scan mode value.  Acceptable values are crawl, scan, or all.
```--scan_mode```

Overrides the scope value.  Acceptable values are all, strict, children, and ancestors.
```--scan_scope```

Overrides existing or adds a recorded login sequence to authenticate to the targeted application
```--login_macro```

Assign either custom or built-in WebInspect policies, for example AggressiveSQLInjection, AllChecks, ApacheStruts, Application, Assault, CriticalsAndHighs, CrossSiteScripting, Development, Mobile, NoSQLAndNode.js OpenSSLHeartbleed, OWASPTop10ApplicationSecurityRisks2013, OWASPTop10ApplicationSecurityRisks2007 OWASPTop10ApplicationSecurityRisks2010, PassiveScan, Platform, PrivilegeEscalation, QA, Quick, Safe, SOAP, SQLInjection, Standard and TransportLayerSecurity
```--scan_policy```

Type of scan to be performed list-driven or workflow-driven scan. Acceptable values are `url` or `macro`
```--scan_start```

Enter a single url or multiple each with it's own --start_urls. For example --start_urls http://test.example.com --start_urls http://test2.example.com
```--start_urls```

--upload_settings, upload setting file to the webinspect host, settings are hosted under webbreaker/etc/webinspect/settings, all settings files end with an .xml extension, the xml extension is not needed and shouldn't be included.
```--upload_settings```

--upload_policy xss, upload policy file to the webinspect scanner policies are hosted under webbreaker/etc/webinspect/policies, all policy files end with a .policy extension, the policy extension is not needed and shouldn't be included.
```--upload_policy```

--upload_webmacro to the webinspect scanner macros are hosted under webbreaker/etc/webinspect/webmacros, all webmacro files end with the .webmacro extension, the extension should NOT be included.
```--upload_webmacros```

--fortify_user authenticates the Fortify SSC user for uploading WebInspect `.fpr` formatted scan
```--fortify_user```

Include the hosts to scan without the protocol or scheme http:// or https://, either a single host or multiple hosts each with it's own --allowed_hosts. If --allowed_hosts is not provided, all hosts explicitly stated within the option, --start_urls will be used.  Keep in mind, if this option is used you must re-enter your host as provided in --start_urls
```--allowed_hosts```

--workflow_macros are located under webbreaker/etc/webinspect/webmacros. Overrides the login macro. Acceptable values are login .webmacros files available on the WebInspect scanner to be used.
```--workflow_macros```


### WebInspect Servers `webinspect_servers`
##### Options

##### Commands
List all servers found in webbreaker/etc/webinspect.ini
```
webbreaker webinspect servers
```

#### WebInspect List `webinspect_list`
##### Options

##### Commands
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
##### Options

##### Commands
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
##### Options

##### Commands

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
##### Options

##### Commands
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
##### Options

##### Commands
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
##### Options

##### Commands
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
#### ThreadFix List `threadfix_list`
##### Options

##### Commands
List all applications (ID, Team Name, Application Name) across all teams found in ThreadFix
```
webbreaker threadfix list
```

List all applications (ID, Team Name, Application Name) with names containing 'secret' across all teams with names containing 'Marketing'. Queries are not case sensitive.
```
webbreaker threadfix list --team Marketing --application secret
```

#### ThreadFix Teams `threadfix_teams`
##### Options

##### Commands
List all teams (ID and Name) found in ThreadFix
```
webbreaker threadfix teams
```

#### ThreadFix Applications `threadfix_applications`
##### Options

##### Commands
List all applications (ID and Name) found in ThreadFix that belong to the team with ID=123
```
webbreaker threadfix applications --team_id 123
```

List all applications (ID and Name) found in ThreadFix that belong to the Marketing team
```
webbreaker threadfix applications --team_name Marketing
```

#### ThreadFix Scans `threadfix_scans`
##### Options

##### Commands
List all scans (ID Scanner, and Filename) found in ThreadFix that belong to the application with ID=345
```
webbreaker threadfix scans --app_id 345
```

#### ThreadFix Upload `threadfix_upload`
##### Options

##### Commands
Upload the local file 'my_app_scan.xml' as a scan to the application with ID=345
```
webbreaker threadfix upload --app_id 345 --scan_file my_app_scan.xml
```

Upload the local file 'my_app_scan.xml' as a scan to the application with name Marketing_App
```
webbreaker threadfix upload --app_name Marketing_App --scan_file my_app_scan.xml
```

#### ThreadFix Create App `threadfix_create_app`
##### Options
`  --start  Flag that instructs WebBreaker to create an agent`

`  --help   Show this message and exit.`
##### Commands
Create a new application, with a given name and url, in ThreadFix under the team with ID=123
```
webbreaker threadfix create_app --team_id 123 --name new_marketing_app --url http://marketing.ourapp.com
```

Create a new application, with a given name and url, in ThreadFix under the Marketing team
```
webbreaker threadfix create_app --team_name Marketing --name new_marketing_app --url http://marketing.ourapp.com
```

## Verbose Cheatsheet: Admin `admin_cheatsheet`
#### Admin Notifier `admin_notifier`
##### Options
`  --email         Flag to specify email notifications`
  
`  --git_url TEXT  Specify Git URL  [required]`
  
`  --help          Show this message and exit.`
##### Commands
Retrieve and store public emails of contributors to the webbreaker repo. Communication with the Git API requires a token stored in webbreaker.ini
```
webbreaker admin notifier --email --git_url https://github.com/target/webbreaker
```

#### Admin Agent `admin_agent`
##### Options

##### Commands
View the current stored information for WebBreaker Agent based on most recent use of 'admin notifier' and 'fortify scan'
```
webbreaker admin agent
```

Create a WebBreaker Agent to monitor the Fortify Cloudscan specified in 'fortify scan'. On scan completion the agent will notify contributors found via 'admin notifiers':
```
webbreaker admin agent --start
```

#### Admin Credentials `admin_credentials`
##### Options
`  --fortify        Flag used to designate options as Fortify credentials`

`  --webinspect     Flag used to designate options as WebInspect credentials`

`  --clear          Flag to clear credentials of Fortify OR WebInspect`

`  --username TEXT  Specify username`

`  --password TEXT  Specify username`

`  --help           Show this message and exit.`
##### Commands
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
##### Options
`-f, --force  Flag prevents confirmation prompt`

##### Commands

A new encryption key is created and all stored credentials are cleared. Through regular use you should not need to use this command. However, if WebBreaker is having troubles with encrypting credentials, this command will help it reset.
```
webbreaker admin secret
```

A new encryption key is created and all stored credentials are cleared. You will not be prompted to confirm this command.
```
webbreaker admin secret [-f / --force]
```
