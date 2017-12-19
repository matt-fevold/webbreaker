#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import random
import string
from subprocess import Popen, PIPE, check_output

WEBBREAKER_EXE = "/usr/local/bin/webbreaker"
PROXY_NAME = "ZeroBankTest" + "-" + "".join(random.choice(string.ascii_uppercase + string.digits) for _ in range(5))
PROXY_SERVER = ""
PROXY_PORT = 9001
THREADFIX_TEAM = "TEST"
THREADFIX_APPLICATION = "ZeroBankTest"
FORTIFY_USER = ""
FORTIFY_PASSWORD = ""
ZERO_BANK_ONE = os.path.abspath(os.path.join("zero_bank_1.py"))
ZERO_BANK_TWO = os.path.abspath(os.path.join("zero_bank_2.py"))


class ZeroBankDriver(object):
    @classmethod
    def zero_bank_tests(cls):
        print(Popen(
            [str(WEBBREAKER_EXE), "webinspect", "proxy", "--start", "--port", str(PROXY_PORT), "--proxy_name",
             str(PROXY_NAME), "--server", str(PROXY_SERVER)], stdout=PIPE).stdout.read())

        if os.path.isfile(ZERO_BANK_ONE):
            print(check_output(
                ["python" + " " + str(ZERO_BANK_ONE) + " " + str(PROXY_SERVER) + ":" + str(PROXY_PORT)], shell=True))

        if os.path.isfile(ZERO_BANK_TWO):
            print(check_output(
                ["python" + " " + str(ZERO_BANK_TWO) + " " + str(PROXY_SERVER) + ":" + str(PROXY_PORT)],
                shell=True))

        print(Popen(
            [str(WEBBREAKER_EXE), "webinspect", "proxy", "--stop", "--proxy_name",
             str(PROXY_NAME)], stdout=PIPE).stdout.read())

        print(Popen(
            [str(WEBBREAKER_EXE), "webinspect", "scan", "--settings", str(os.path.abspath(os.path.join(PROXY_NAME + '-proxy.xml'))), "--scan_name",
             str(PROXY_NAME)], stdout=PIPE).stdout.read())

        if os.path.isfile(PROXY_NAME + '.xml'):
            print(Popen(
                [str(WEBBREAKER_EXE), "threadfix", "create", "-team", str(THREADFIX_TEAM),
                  "--url", "http://zero.webappsecurity.com/"], stdout=PIPE).stdout.read())

            print(Popen(
                [str(WEBBREAKER_EXE), "threadfix", "upload", "--application", str(THREADFIX_APPLICATION),
                  "--scan_file", str(os.path.abspath(os.path.join(PROXY_NAME + '.xml')))], stdout=PIPE).stdout.read())

        if os.path.isfile(PROXY_NAME + '.fpr'):
            print(Popen(
                [str(WEBBREAKER_EXE), "fortify", "upload", "--fortify_user", str(FORTIFY_USER), "--fortify_password",
                 str(FORTIFY_PASSWORD), "--version", str(PROXY_NAME), "--scan_name", str(PROXY_NAME)],
                 stdout=PIPE).stdout.read())

if __name__ == '__main__':
    ZeroBankDriver.zero_bank_tests()
