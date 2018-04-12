# WebBreaker Documentation

## Table of Contents
[Introduction](#introduction)

- [Description: `description`](#description)

[User Guide](#user-guide)

- [Installation `installation`](#installation)
- [Supported Features `supported_features`](#supported-features)
- [Usage `usage`](#usage)
- [Logging `logging`](#logging)
- [Docker `docker`](#docker)
- [Testing `testing`](#testing)
- [Notifications `notifications`](#notifications)

[Configuration](#configuration)

- [WebBreaker `webbreaker_config`](#webbreaker-config)
- [Fortify `fortify_config`](#fortify-config)
- [ThreadFix `threadfix_config`](#threadfix-config)
- [WebInspect `webinspect_config`](#webinspect-config)
- [Email `email_config`](#email-config)

- [WebBreaker Command Usage `webbreaker_cheatsheet`](#webbreaker-cheatsheet)


## Introduction `introduction`

### Description `description`
Build functional security testing, into your software development and release cycles! WebBreaker provides the capabilities to automate and centrally manage Dynamic Application Security Testing (DAST) as part of your DevOps pipeline.

## User Guide `user-guide`

### Installation: `installation`

#### Quick Local Installation 
Install WebBreaker from source.
* ```git clone https://github.com/target/webbreaker```
* ```cd webbreaker```
* ```pip install -r requirements.txt```
* ```python setup.py install```

Install WebBreaker with Linux/MacOS pyinstaller.
* ```git clone https://github.com/target/webbreaker```
* ```cd webbreaker```
* ```python setup.py pyinstaller```

Install WebBreaker with Windows pyinstaller.
* ```git clone https://github.com/target/webbreaker```
* ```cd webbreaker```
* ```Set-ExecutionPolicy Unrestricted```
* ```Powershell.exe -executionpolicy unrestricted -command build.ps1```
* ```python setup.py windows```

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
* Configurable property .ini files to support your [Foritfy](.webbreaker/config.ini) and [WebInspect](.webbreaker/config.ini) deployments.
* Enterprise scalability with configurable Just-In-Time (JIT) scheduling to distribute your WebInspect scans between two (2) or greater sensors.
* ChatOps extensibility and [email notifications](.webbreaker/config.ini) on scan start and completion.
* Local [logging](.webbreaker/log) of WebInspect scan state.

### Usage `usage`
Webbreaker utilizes a structure of upper-level and lower-level commands to enable interaction with multiple 3rd party platforms. The two platforms currently supported are WebInspect and Fortfiy and they can be accessed using their respective upper-level commands. Webbreaker supports multiple functions for each platform which are accessed via lower-level commands. The current command structure is listed below.

- webbreaker
    - webinspect
        - scan
        - servers
        - list
        - download
        - proxy
    - fortify
        - list
        - upload
        - scan
        - download
    - admin
        - credentials
        - clear
    - threadfix
        - list
        - teams
        - applications
        - scans
        - upload
        - create_app

A proper Webbreaker command utilizes the structure 'webbreaker [webinspect|fortify|threadfix|admin] [lower-level command] [OPTIONS]'

### Logging `logging`
WebBreaker local logs may be found under `~/.webbreaker/logs` and can be implemented with Elastic Stack for log aggregation. Recommended compenents include Filebeat agents installed on all WebInspect servers, forwarding to Logstash, and visualized in Kibana. General implementation details are [here](https://qbox.io/blog/welcome-to-the-elk-stack-elasticsearch-logstash-kibana/).  A recommended approach is to tag log events and queries with ```WebInspect``` and ```webbreaker```, but remember 
queries are case sensitive.

### Docker `docker`
Run WebBreaker in Docker from the repository's root directory, the pre-configured virtualenv environments are `venv27` for Python 2.7 or `venv36` for Python 3.6.  Examples are illustrated below.

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

### Testing `testing`
Our automated testing is performed with tox and detox on Python 3.6 and 2.7.

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
WebBreaker provides notifications or email for start-scan and end-scan events. 

The email notifier merges the provided event data into an HTML email message and sends the message. All SMTP-related 
settings are managed under your user's home directory within the `~.webbreaker/config.ini`, and read during the webbreaker execution.

If an error occurs on behalf of the notifiers at any point during the process of creating or sending 
notifications, the event will be logged, without any interruption of WebBreaker execution or the WebInspect scan.

## Configuration

Below is the default config.ini that is set at first time install, once you execute `webbreaker` for the first time.  All subsequent installs and updates will not update your `~/.webbreaker/config.ini` unless it is deleted.  You will need to modify the appropriate sections to your environment specifications.

### Default 
````
[fortify]
verify_ssl = False
ssc_url = https://fortify.example.com/ssc
username =
password =
application_name = WEBINSPECT
business_risk_ranking = High
development_phase = Active
development_strategy = Internal
accessibility = externalpublicnetwork
custom_attribute_name =
custom_attribute_value =

[threadfix]
host = https://threadfix.example.com:8443/threadfix
api_key =

[webinspect]
server_01 = https://webinspect-server-1.example.com:8083
endpoint_01 = %(server_01)s|%(size_large)s
git_repo = https://github.com/webbreaker/webinspect.git
authenticate = false
username =
password =

[webinspect_policy]
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
smtp_host = smtp.example.com
smtp_port = 25
from_address = webbreaker-no-reply@example.com
to_address = webbreaker-activity@example.com
default_to_address =
chatroom =
email_template =
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
````

### [threadFix]
##### host
Threadfix host that will be used.

##### api_key
This api_key to authenticate ThreadFix actions

### [fortify]
Fortify SSC settings can be found under [fortify]

##### application_name
Static Value of the default Fortify SSC Application you wish to use without stating it on the command line.

##### verify_ssl
Option to verify ssl or not while communicating with Fortify. The default option is 'False'.

##### ssc_url
URL of the fortify server to contact.

##### username
Fortify username that will be used for authentication with ssc_url. It is stored using an encrypted value. Use 
`webbreaker admin credentials --fortify` to set your username & password.

##### password
Fortify username that will be used for authentication with ssc_url. It is stored using an encrypted value. Use 
`webbreaker admin credentials --fortify` to set your username & password.

##### business_risk_ranking
Fortify defaults this to `High`. Other valid inputs are `Medium` & `Low`.

##### development_phase
Current development phase of Fortify Version. Default is `Active`.

##### development_strategy
Development staffing strategy used for this Application. Default is `Internal`.

##### accessibility
The level of recommended access required to interact with this Application. Default is `externalpublicnetwork`.

##### project_template
Static value of the Fortify SSC Project Template you wish to set as a default for each Application Version you create.

##### custom_attribute_id
If you would like to set another attribute definition with a custom id number for creation of a new Application Version.

##### custom_attribute_value
If you would like to set another attribute definition with a custom value for creation of a new Application Version.

##### search_expression
If this is set, it will attempt to retrieve the Application Attribute Definition and use that ID in setting Version Attributes.
The format for creating a search_expression is `name:"Search Example"`

##### attribute_definition_id
Instead of using the search expression to retrieve the Application Attribute Definition, you may set it here and the search_expression will be ignored.

##### version_attribute_value
Attribute value that is set when setting Version Attributes. The default is `New WebBreaker Application`

##### version_attribute_values
List of Version attribute values to set while setting Version Attributes.

### [webinspect]

WebInspect scan configuration files for `policies` are versioned and hosted from a GIT repository configured 
in `~/.webbreaker/config.ini`.  Additionally, all WebInspect policies and servers are managed from this 
configuration file.  

All WebInspect distributions are packaged with a `Default.xml` setting file that may be overridden and uploaded 
to the WebInspect deployment with the webbreaker option `--settings`.  The setting xml file contains 
all possible options for your scan, including a WebInspect scan including policy, workflow and/or login 
macro, scan depth, and allowed hosts.

#### server_XX and endpoint_XX
Provides a _Just-In-Time_ (JIT) scheduler provides the ability to load balance a WebInspect cluster for scans.

#### webinspect_size
Sets the number for large and small WebInspect scan servers. This assists with _Just-In-Time_ (JIT) scheduling

#### webinspect_repo
A unique GIT repo is defined by the user and is mutually exclusive from the WebBreaker source.  The 
assumption is each WebBreaker installation will have a unique GIT URL defined.  Upon each execution, 
the repo refreshes *all* settings file(s), assuming that there may be newly created, deletions, or modifications 
of settings files.  All settings files used in execution must reside in this respective repo 
under `~/.webbreaker/etc/webinspect/settings`.

#### username
Basic authentication with `.htaccess` syntax configured on your WebInspect server

If authentication is set to true, all WebInspect requests will use basic auth. A user will be prompted for
credentials which, if valid, will be encrypted and saved. Credentials can also be set via the
`webbreaker admin credentials --webinspect` command.

#### password
Basic authentication with `.htaccess` syntax configured on your WebInspect server

### [webinspect_policy]
Grouping of proprietary WebInspect tests to perform.  Tests or rules are represented in an `xml` element with 
a `.policy` file extension.  Custom tests or Checks are mapped to a unique WebInspect ID.  The mapping for all 
policies shipped with WebInspect are mapped with their respective GUID within this section.

*Note:* All custom polices are automatically uploaded to the targeted WebInspect server and must be referenced 
as a GUID.  

### email
Notifications for start-scan and end-scan events. A simple publisher/subscriber pattern is implemented under 
the "notifiers" folder.

A Reporter object holds a collection of Notifier objects, each of which implements a Notify function responsible 
for creating the desired notification. Currently, two notification types are implemented email and database.

The email notifier merges the provided event data into an HTML email message and sends the message. All 
SMTP-related settings are stored in .emailrc, and read during program startup.

## WebBreaker Command Usage `webbreaker_cheatsheet`
See [WebBreaker Cheatsheet](https://github.com/target/webbreaker/blob/master/docs/cheatsheet.md)
