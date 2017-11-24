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
        self.install = os.path.abspath('')
        self.config_name = 'config.ini'
        self.config = os.path.join(self.install, self.config_name)

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
            read_path = self.install

        if read_path == '':
            config.set('webbreaker_install', 'dir', self.install)
            with open(self.config, 'w') as configfile:
                config.write(configfile)
            read_path = self.install
        self.install = self.set_path(dir_path=read_path)
        self.config = self.set_path(file_name=self.config_name)
        self.etc = self.set_path(dir_path='etc')
        self.git = os.path.join(self.set_path(dir_path=os.path.join('etc', 'webinspect')), '.git')
        self.log = self.set_path(dir_path='log')
        self.secret = os.path.join(self.install, '.webbreaker')
        self.agent_json = self.set_path(dir_path='etc', file_name='agent.json')

    def set_path(self, dir_path=None, file_name=None):
        if dir_path and file_name:
            dir_path = os.path.join(self.install, dir_path)
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
            dir_path = self.install
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
            dir_path = os.path.join(self.install, dir_path)
            if not os.path.exists(dir_path):
                os.makedirs(dir_path)
            return dir_path
