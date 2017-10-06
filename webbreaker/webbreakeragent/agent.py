#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import sys
import os
from datetime import datetime
import json
import socket
from __init__ import __version__
from webbreaker.notifiers.emailer import EmailNotifier
from webbreaker.fortifyconfig import FortifyConfig
from fortifyapi.fortify import FortifyApi


class AgentClient(object):
    def __init__(self, agent_json):
        self.pid = os.getpid()
        self.fqdn = socket.getfqdn()
        data = self.__read_json__(agent_json)
        self.payload = self.__formatted_elk_payload__(scan=data['fortify_build_id'], host=self.fqdn, version=__version__,
                                                      notifiers=data['git_emails'], git_url=data['git_url'],
                                                      fortify_url=data['fortify_pv_url'])
        self.payload['start'] = datetime.now().isoformat()
        self.fortify_config = FortifyConfig()
        self.check_count = 0
        self.timeout = 15

    def check(self):
        self.check_count += 1
        api = FortifyApi(host=self.fortify_config.ssc_url, username=self.fortify_config.username,
                         password=self.fortify_config.password, verify_ssl=False)

        response = api.get_cloudscan_job_status(self.scan_id)
        if response.success:
            self.log("CHECK", response.data['data']['jobState'])
            return response.data['data']['jobState']
        else:
            self.log("CHECK FAILURE", 'API REQUEST FAILED')
            sys.exit()

    def check_timeout(self):
        time_running = self.timeout * self.check_count
        # Kill any agent that is 3 days old
        if time_running > 259200:
            self.payload['status'].append('AGENT TIMEOUT')
            self.write_json()
            self.log("AGENT TIMEOUT", 'AGENT KILLED AFTER {} SECONDS'.format(time_running))
            sys.exit()

    def find_job_id(self):
        api = FortifyApi(host=self.fortify_config.ssc_url, username=self.fortify_config.username,
                         password=self.fortify_config.password, verify_ssl=False)
        response = api.get_cloudscan_jobs()
        if response.success:
            for scan in response.data['data']:
                if scan['scaBuildId'] == self.payload['scan']:
                    self.scan_id = scan['jobToken']
                    self.log('SCAN FOUND', self.scan_id)
                    self.payload['status'].append(scan['jobState'])
                    return
            for i in range(0,2):
                time.sleep(30)
                response = api.get_cloudscan_jobs()
                for scan in response.data['data']:
                    if scan['scaBuildId'] == self.payload['scan']:
                        self.scan_id = scan['jobToken']
                        self.log('SCAN FOUND', self.scan_id)
                        self.payload['status'].append(scan['jobState'])
                        return
            self.scan_id = None
            self.log('NO SCAN FOUND', "No scan was found within 1 minute")
        else:
            self.scan_id = None
            self.log('NO SCAN FOUND', response.message)

    def log(self, action, value):
        with open('/tmp/webbreaker_agent.log', 'a') as log_file:
            log_file.write("{}|{}|{}|{}\n".format(self.pid, datetime.now().isoformat(), action, value))
        log_file.close()

    def notify(self):
        subject = "Static Scan Notification"
        notifier = EmailNotifier()
        if notifier.default_to_address:
            self.payload['notifiers'].append(notifier.default_to_address)
        for email in self.payload['notifiers']:
            notifier.cloudscan_notify(recipient=email, subject=subject, git_url=self.payload['git_url'],
                                      ssc_url=self.payload['fortify_url'], state=self.payload['status'][-1],
                                      scan_name=self.payload['scan'], scan_id=self.scan_id)

    def run(self):
        agent.find_job_id()
        if not agent.scan_id:
            sys.exit()
        response = agent.watch()
        agent.notify()
        agent.write_json()

    def watch(self):
        self.log("WATCH", "START")
        status = self.check()
        end_states = ['FAILURE', 'UPLOAD_COMPLETED']
        while status not in end_states:
            time.sleep(self.timeout)
            status = self.check()
            if status != self.payload['status'][-1]:
                self.payload['status'].append(status)
            self.check_timeout()
        self.log("WATCH", "END")
        self.payload['end'] = datetime.now().isoformat()
        return status

    def write_json(self):
        if os.path.isfile('/tmp/webbreaker.json'):
            with open('/tmp/webbreaker.json', 'r') as json_file:
                try:
                    logs = json.load(json_file)
                except json.decoder.JSONDecodeError:
                    logs = {'logs': []}
                    pass
            json_file.close()
        else:
            logs = {'logs':[]}
        logs['logs'].append(self.payload)
        with open('/tmp/webbreaker.json', 'w') as json_file:
            json.dump(logs, json_file, sort_keys=True, indent=4, separators=(',', ': '))
        json_file.close()


    @staticmethod
    def __formatted_elk_payload__(scan, host, version, notifiers, git_url, fortify_url):

        elk_json = dict(scan='', host='', version='', notifiers=[], name=None, settings=None, overrides=None, git_url='',
                        start=None, end=None, events=None, status=[], fortify_url='')

        elk_json['scan'] = scan
        elk_json['host'] = host
        elk_json['version'] = version
        elk_json['notifiers'] = notifiers
        elk_json['git_url'] = git_url
        elk_json['fortify_url'] = fortify_url

        return elk_json

    def __read_json__(self, file_path):
        if os.path.isfile(file_path):
            with open(file_path, 'r') as json_file:
                try:
                    data = json.load(json_file)
                except json.decoder.JSONDecodeError:
                    return None
                json_file.close()
            return data
        else:
            return None


if __name__ == '__main__':
    f = open('/tmp/webbreaker_agent_error.log', 'a')
    sys.stdout = f
    sys.stderr = f

    agent = AgentClient(sys.argv[1])
    agent.run()

