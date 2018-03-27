#!/usr/bin/env python
# -*- coding: utf-8 -*-

from webbreaker.fortify.fortifyclient import FortifyClient
from webbreaker.fortify.fortifyconfig import FortifyConfig
from exitstatus import ExitStatus
import sys
from webbreaker.common.webbreakerlogger import Logger
from webbreaker.common.authorization import auth_prompt


class Fortify:
    def __init__(self):
        self.config = None

    def _set_config_(self):
        self.config = FortifyConfig()


