#!/usr/bin/env python
# -*- coding: utf-8 -*-

from webbreaker.common.webbreakerlogger import Logger


class Reporter(object):

    def __init__(self, notifiers):
        self.notifiers = notifiers

    def report(self, event):
        try:
            for notifier in self.notifiers:
                notifier.notify(event)
        except (Exception, AttributeError):
            Logger.console.error("Error sending email, see log: {}!".format(Logger.app_logfile))
