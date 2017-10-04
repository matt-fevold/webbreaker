#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import sys
import os
from datetime import datetime
import json
import socket
from __init__ import __version__
from emailer import EmailNotifier
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

    def check(self):
        api = FortifyApi(host=self.fortify_config.ssc_url, username=self.fortify_config.username,
                         password=self.fortify_config.password, verify_ssl=False)

        response = api.get_cloudscan_jobs()
        if response.success:
            self.log("DATA", response.data)
            return 'COMPLETE'
        else:
            sys.exit()
        # self.log("CHECK", status)
        # return status

    def watch(self):
        self.log("WATCH", "START")
        status = self.check()
        while status == 'RUNNING':
            time.sleep(15)
            status = self.check()
        self.log("WATCH", "END")
        self.payload['end'] = datetime.now().isoformat()
        return status

    def notify(self):
        subject = "Static Scan Notification"
        notifier = EmailNotifier()
        for email in self.payload['notifiers']:
            notifier.notify(recipient=email, subject=subject, git_url=self.payload['git_url'],
                            ssc_url=self.payload['fortify_url'])

    def log(self, action, value):
        with open('log.txt', 'a') as log_file:
            log_file.write("{}|{}|{}|{}\n".format(self.pid, datetime.now().isoformat(), action, value))
        log_file.close()

    def write_json(self):
        with open('webbreaker.json', 'a') as json_file:
            json.dump(self.payload, json_file, sort_keys=True, indent=4, separators=(',', ': '))
            json_file.write('\n')
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

    # TODO: Eventually we'll need to block output and send it to an appropriate file
    # f = open(os.devnull, 'w')
    # sys.stdout = f
    # sys.stderr = f

    agent = AgentClient(sys.argv[1])
    response = agent.watch()
    # TODO: Test notifier
    # agent.notify()
    agent.write_json()
    sys.exit()

