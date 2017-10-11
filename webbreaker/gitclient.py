#!/usr/bin/env python
# -*- coding: utf-8 -*-

from webbreaker.gitapi.git import GitApi
from webbreaker.webbreakerlogger import Logger
import requests
import requests.exceptions
import requests.packages.urllib3
import os
import json
import re
try:
    import ConfigParser as configparser
except ImportError: #Python3
    import configparser
try:  # Python 2
    config = configparser.SafeConfigParser()
except NameError:  # Python 3
    config = configparser.ConfigParser()

class GitClient(object):
    def __init__(self, host):
        try:
            self.host = host
            self.token = self.get_token()
        except configparser.NoSectionError as e:
            Logger.app.error("You are missing a git OAuth Token in your webbreaker.ini: {}".format(e))

    def get_user_email(self, login):
        gitapi = GitApi(host=self.host, token=self.token, verify_ssl=False)
        response = gitapi.get_user(login)
        if response.success:
            return response.data['email']
        else:
            Logger.console.error("Error finding emails address for user {}: {}".format(login, response.message))
            return None

    def get_contributors(self, owner, repo):
        gitapi = GitApi(host=self.host, token=self.token, verify_ssl=False)
        response = gitapi.get_contributors(owner, repo)
        if response.success:
            contributors = []
            for contributor in response.data:
                contributors.append(contributor['login'])
            return contributors
        else:
            Logger.console.error("Error finding contributors: {}".format(response.message))
            return None

    def get_all_emails(self, owner, repo):
        emails = []
        logins = self.get_contributors(owner, repo)
        if logins:
            for login in logins:
                email = self.get_user_email(login)
                if email:
                    emails.append(email.lower())
        else:
            Logger.console.error("Unable to retrieve list of contributors for this repo.")
            return None
        if len(emails):
            return list(set(emails))
        else:
            Logger.console.error("No contributor emails where found for this repo.")
            return None

    def get_token(self):
        config_file = os.path.abspath(os.path.join('webbreaker', 'etc', 'webbreaker.ini'))
        config.read(config_file)
        return config.get("git", "token")


def write_agent_info(name, value):
    json_file_path = os.path.abspath(os.path.join('webbreaker', 'etc', 'agent.json'))
    try:
        if os.path.isfile(json_file_path):
            with open(json_file_path, 'r') as json_file:
                try:
                    data = json.load(json_file)
                except json.decoder.JSONDecodeError:
                    data = {}
                json_file.close()
        else:
            data = {}
        data[name] = value
        with open(json_file_path, 'w') as json_file:
            json.dump(data, json_file)
    except json.decoder.JSONDecodeError:
        Logger.console.error("Error writing {} to agent.json".format(name))
        exit(1)


def read_agent_info():
    json_file_path = os.path.abspath(os.path.join('webbreaker', 'etc', 'agent.json'))
    try:
        if os.path.isfile(json_file_path):
            with open(json_file_path, 'r') as json_file:
                try:
                    data = json.load(json_file)
                except json.decoder.JSONDecodeError:
                    data = {}
                json_file.close()
        else:
            data = {}
        if 'fortify_build_id' not in data:
            data['fortify_build_id'] = None
        if 'git_url' not in data:
            data['git_url'] = None
        if 'fortify_pv_url' not in data:
            data['fortify_pv_url'] = None
        if 'git_emails' not in data:
            data['git_emails'] = None
        return data

    except json.decoder.JSONDecodeError:
        Logger.console.error("Error reading from agent.json")
        exit(1)

def format_git_url(url):
    # if url ends in .git, remove
    url = url.replace('.git', '')

    https_matcher = re.compile('^https://.*/.*/.*')
    http_matcher = re.compile('^http://.*/.*/.*')
    ssh_matcher = re.compile('^git@.*:.*/.*')

    if http_matcher.match(url) or https_matcher.match(url):
        return url
    if ssh_matcher.match(url):
        url = url.replace('git@', '')
        url = url.replace(':', '/')
        url = 'https://' + url
        return url
    return None

class UploadJSON(object):
    def __init__(self, log_file):
        self.git_emails = None
        self.fortify_pv_url = None
        self.fortify_build_id = None
        if os.path.isfile(log_file):
            with open(log_file, 'r') as json_file:
                try:
                    data = json.load(json_file)
                except json.decoder.JSONDecodeError:
                    Logger.console.error("JSONDecodeError reading from agent.json")
                    exit(1)
                json_file.close()
            if self.__verify__(data) == -1:
                exit(1)
            self.git_emails = data['git_emails']
            self.fortify_pv_url = data['fortify_pv_url']
            self.fortify_build_id = data['fortify_build_id']
        else:
            Logger.console.error("Error while reading upload payload")
            exit(1)

    def __verify__(self, data):
        if not 'git_emails' in data:
            Logger.console.error("No emails were found to notify. Please run 'webbreaker git emails --url [REPO URL]'")
            return -1
        if not 'fortify_pv_url' in data:
            Logger.console.error("""No Fortify Project Version URL was found. Please run 'webbreaker fortify scan 
                                    --application <some_value> --version <some_value>'""")
            return -1
        if not 'fortify_build_id' in data:
            Logger.console.error("No Fortify Build ID found. Please run 'webbreaker fortify scan --build_id [BUILD_ID]'")
            return -1
        return 1

class AgentVerifier(object):
    def __init__(self, log_file):
        if os.path.isfile(log_file):
            with open(log_file, 'r') as json_file:
                try:
                    data = json.load(json_file)
                except json.decoder.JSONDecodeError:
                    Logger.console.error("JSONDecodeError reading from agent.json")
                    exit(1)
                json_file.close()
            if self.__verify__(data) == -1:
                exit(1)
        else:
            Logger.console.error("Error while reading upload payload")
            exit(1)

    def __verify__(self, data):
        if not 'git_emails' in data:
            Logger.console.error("No emails were found to notify. Please run 'webbreaker admin notifier --email --url [REPO URL]'")
            return -1
        if not 'fortify_pv_url' in data:
            Logger.console.error("""No Fortify Project Version URL was found. Please run 'webbreaker fortify scan 
                                            --application <some_value> --version <some_value>'""")
            return -1
        if not 'fortify_build_id' in data:
            Logger.console.error("No Fortify Build ID found. Please run 'webbreaker fortify scan --build_id [BUILD_ID]'")
            return -1
        if not 'git_url' in data:
            Logger.console.error("No Git Repo URL found. Please run 'webbreaker admin notifier --email --url [REPO URL]'")
            return -1
        return 1

class GitUploader(object):
    def __init__(self, agent_url=None):
        self.upload_log = UploadJSON(os.path.abspath(os.path.join('webbreaker', 'etc', 'agent.json')))
        self.agent_url = agent_url
        if not agent_url:
            self.agent_url = self.read_ini()


    def read_ini(self):
        config_file = os.path.abspath(os.path.join('webbreaker', 'etc', 'webbreaker.ini'))
        config.read(config_file)
        return config.get("agent", "webbreaker_agent")


    def upload(self):
        data = {}
        data['fortify_pv_url'] = self.upload_log.fortify_pv_url
        data['fortify_build_id'] = self.upload_log.fortify_build_id
        data['git_emails'] = self.upload_log.git_emails
        response = requests.put(self.agent_url, data=data)
        return response.status_code


