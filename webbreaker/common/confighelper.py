#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from webbreaker.common.webbreakerhelper import WebBreakerHelper

try:
    import ConfigParser as configparser
    config = configparser.SafeConfigParser(allow_no_value=True)
except ImportError:  # Python3
    import configparser
    config = configparser.ConfigParser(allow_no_value=True)


class Config(object):
    def __init__(self):
        self.home = os.path.expanduser('~')
        self.install = None
        self.config = None
        self.etc = None
        self.git = None
        self.log = None
        self.agent_json = None
        self.secret = None
        self.cert = None

        self.set_vars()
        self.set_config()

    def set_vars(self):
        self.install = self.set_path(install=self.home, dir_path='.webbreaker')
        self.config = self.set_path(file_name='config.ini')
        self.etc = self.set_path(dir_path='etc')
        self.git = self.set_path(dir_path='etc/webinspect')
        self.log = self.set_path(dir_path='log')
        self.agent_json = self.set_path(dir_path=self.etc, file_name='agent.json')
        self.cert = self.set_path(file_name='wiproxycert.crt')

        self.secret = os.path.join(self.install, '.webbreaker')

    def set_path(self, install=None, dir_path=None, file_name=None):
        if not install:
            install = self.install
        if dir_path and file_name:
            dir_path = os.path.join(install, dir_path)
            full_path = os.path.join(dir_path, file_name)
            if not os.path.exists(dir_path):
                os.makedirs(dir_path)
            try:
                f = open(full_path, 'a+')
                f.close()
            except IOError:
                print("Unable to open {}".format(full_path))
                return 1
            return full_path

        elif not dir_path and file_name:
            dir_path = install
            full_path = os.path.join(dir_path, file_name)
            if not os.path.exists(dir_path):
                os.makedirs(dir_path)
            try:
                f = open(full_path, 'a+')
                f.close()
            except IOError:
                print("Unable to open {}".format(full_path))
                return 1
            return full_path

        elif dir_path and not file_name:
            dir_path = os.path.join(install, dir_path)
            if not os.path.exists(dir_path):
                os.makedirs(dir_path)
            return dir_path
        return 1

    def conf_get(self, section, option, value=None):
        try:
            config.read(self.config)
            return config.get(section, option)

        except configparser.NoSectionError:
            config.add_section(section)
            config.set(section, option, value)
            with open(self.config, 'w') as configfile:
                config.write(configfile)
            return value

        except configparser.NoOptionError:
            config.set(section, option, value)
            with open(self.config, 'w') as configfile:
                config.write(configfile)
            return value

    def set_config(self):
        # Complete SSC URL with the the context of your deployment.
        # TODO: Change ssc_url -> fortify_url or vice versa. Just standardize
        # Default Fortify SSC Application
        self.conf_get('fortify', 'application_name', 'WEBINSPECT')

        # Default verify_ssl value
        self.conf_get('fortify', 'verify_ssl', 'False')
        self.conf_get('fortify', 'ssc_url', 'https://fortify.example.com/ssc')

        # Fortify SSC authentication execute, webbreaker admin credentials --fortify
        self.conf_get('fortify', 'username', '')
        self.conf_get('fortify', 'password', '')

        # Default & a custom Fortify SSC Application Version attribute values and
        # Application (Project) Template associated to the Application Version
        self.conf_get('fortify', 'project_template', 'Prioritized High Risk Issue Template')
        self.conf_get('fortify', 'business_risk_ranking', 'High')
        self.conf_get('fortify', 'development_phase', 'Active')
        self.conf_get('fortify', 'development_strategy', 'Internal')
        self.conf_get('fortify', 'accessibility', 'externalpublicnetwork')
        self.conf_get('fortify', 'custom_attribute_name', '')
        self.conf_get('fortify', 'custom_attribute_value', '')

        # ThreadFix URL and ThreadFix API Key')
        self.conf_get('threadfix', 'host', 'https://threadfix.example.com:8443/threadfix')
        self.conf_get('threadfix', 'api_key', 'ZfO0b7dotQZnXSgkMOEuQVoFIeDZwd8OEQE7XXX')

        # WebInspect load balancing, size of server is bound to CPU & memory available
        self.conf_get('webinspect', 'size_large', '2')
        self.conf_get('webinspect', 'size_medium', '1')
        self.conf_get('webinspect', 'default_size', 'size_large')

        # WebInspect server(s) RESTFul API endpoints
        self.conf_get('webinspect', 'server_01', 'https://webinspect-server-1.example.com:8083')
        self.conf_get('webinspect', 'endpoint_01', '%(server_01)s|%(size_large)s')
        self.conf_get('webinspect', 'git_repo', 'https://github.com/webbreaker/webinspect.git')

        # API authentication set to true execute, webbreaker admin credentials --webinspect
        self.conf_get('webinspect', 'authenticate', 'false')
        self.conf_get('webinspect', 'username', '')
        self.conf_get('webinspect', 'password', '')
        self.conf_get('webinspect', 'verify_ssl', 'False')

        # Built-in WebInspect policies, other policies may be appended
        self.conf_get('webinspect_policy', 'aggressivesqlinjection', '032b1266-294d-42e9-b5f0-2a4239b23941')
        self.conf_get('webinspect_policy', 'allchecks', '08cd4862-6334-4b0e-abf5-cb7685d0cde7')
        self.conf_get('webinspect_policy', 'apachestruts', '786eebac-f962-444c-8c59-7bf08a6640fd')
        self.conf_get('webinspect_policy', 'application', '8761116c-ad40-438a-934c-677cd6d03afb')
        self.conf_get('webinspect_policy', 'assault', '0a614b23-31fa-49a6-a16c-8117932345d8')
        self.conf_get('webinspect_policy', 'blank', 'adb11ba6-b4b5-45a6-aac7-1f7d4852a2f6')
        self.conf_get('webinspect_policy', 'criticalsandhighs', '7235cf62-ee1a-4045-88f8-898c1735856f')
        self.conf_get('webinspect_policy', 'crosssitescripting', '49cb3995-b3bc-4c44-8aee-2e77c9285038')
        self.conf_get('webinspect_policy', 'development', '9378c6fa-63ec-4332-8539-c4670317e0a6')
        self.conf_get('webinspect_policy', 'mobile', 'be20c7a7-8fdd-4bed-beb7-cd035464bfd0')
        self.conf_get('webinspect_policy', 'nosqlandnode.js', 'a2c788cc-a3a9-4007-93cf-e371339b2aa9')
        self.conf_get('webinspect_policy', 'opensslheartbleed', '5078b547-8623-499d-bdb4-c668ced7693c')
        self.conf_get('webinspect_policy', 'owasptop10applicationsecurityrisks2013',
                      '48cab8a0-669e-438a-9f91-d26bc9a24435')
        self.conf_get('webinspect_policy', 'owasptop10applicationsecurityrisks2007',
                      'ece17001-da82-459a-a163-901549c37b6d')
        self.conf_get('webinspect_policy', 'owasptop10applicationsecurityrisks2010',
                      '8a7152d5-2637-41e0-8b14-1330828bb3b1')
        self.conf_get('webinspect_policy', 'passivescan', '40bf42fb-86d5-4355-8177-4b679ef87518')
        self.conf_get('webinspect_policy', 'platform', 'f9ae1fc1-3aba-4559-b243-79e1a98fd456')
        self.conf_get('webinspect_policy', 'privilegeescalation', 'bab6348e-2a23-4a56-9427-2febb44a7ac4')
        self.conf_get('webinspect_policy', 'qa', '5b4d7223-a30f-43a1-af30-0cf0e5cfd8ed')
        self.conf_get('webinspect_policy', 'quick', 'e30efb2a-24b0-4a7b-b256-440ab57fe751')
        self.conf_get('webinspect_policy', 'safe', 'def6a5b3-d785-40bc-b63b-6b441b315bf0')
        self.conf_get('webinspect_policy', 'soap', 'a7eb86b8-c3fb-4e88-bc59-5253887ea5b1')
        self.conf_get('webinspect_policy', 'sqlinjection', '6df62f30-4d47-40ec-b3a7-dad80d33f613')
        self.conf_get('webinspect_policy', 'standard', 'cb72a7c2-9207-4ee7-94d0-edd14a47c15c')
        self.conf_get('webinspect_policy', 'transportlayersecurity', '0fa627de-3f1c-4640-a7d3-154e96cda93c')

        # smnp email host, port and email addresses required for email functionality.
        self.conf_get('emailer', 'smtp_host', 'smtp.example.com')
        self.conf_get('emailer', 'smtp_port', '25')
        self.conf_get('emailer', 'from_address', 'webbreaker-no-reply@example.com')
        self.conf_get('emailer', 'to_address', 'webbreaker-activity@example.com')
        self.conf_get('emailer', 'default_to_address', '')
        self.conf_get('emailer', 'chatroom', '')
        self.conf_get('emailer', 'email_template', WebBreakerHelper().email_template_config())

