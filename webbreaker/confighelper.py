#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import shutil

try:
    import ConfigParser as configparser

    config = configparser.SafeConfigParser()
except ImportError:  # Python3
    import configparser

    config = configparser.ConfigParser()


class Config(object):
    def __init__(self):
        # TODO: Confirm that files/folders exist, if not create them
        self.install = os.path.abspath('')
        self.config = os.path.join(self.install, 'config.ini')

        self.etc = None
        self.git = None
        self.log = None
        self.secret = None
        self.agent_json = None

        self.install_path()

    def install_path(self):
        if not os.path.exists(self.config):
            shutil.copy(self.config + '.example', self.config)

        try:
            config.read(self.config)
            read_path = config.get('webbreaker_install', 'dir')
        except configparser.NoSectionError as e:
            config.add_section('webbreaker_install')
            config.set('webbreaker_install', 'dir', self.install)
            with open(self.config, 'w') as configfile:
                config.write(configfile)
            read_path = config.get('webbreaker_install', 'dir')

        if read_path == '':
            config.set('webbreaker_install', 'dir', self.install)
            with open(self.config, 'w') as configfile:
                config.write(configfile)
        self.install = read_path
        self.config = os.path.join(self.install, 'config.ini')
        self.etc = os.path.join(self.install, 'etc')
        self.git = os.path.join(self.install, 'etc', 'webinspect', '.git')
        self.log = os.path.join(self.install, 'log')
        self.secret = os.path.join(self.install, '.webbreaker')
        self.agent_json = os.path.join(self.install, 'etc', 'agent.json')
