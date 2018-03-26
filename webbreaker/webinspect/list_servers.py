#!/usr/bin/env python
# -*- coding: utf-8 -*-

from webbreaker.webinspect.webinspect_config import WebInspectConfig


class WebInspectListServers:
    def __init__(self):
        self.list_servers()

    @staticmethod
    def list_servers():
        servers = [(e[0]) for e in WebInspectConfig().endpoints]
        print('\n\nFound WebInspect Servers')
        print('-' * 30)
        for server in servers:
            print(server)
        print('\n')
