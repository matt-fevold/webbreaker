#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import shutil
from webbreaker.notifiers import emailer
from webbreaker.webbreakerlogger import Logger
from webbreaker.notifiers import reporter

try:
    import ConfigParser as configparser

    config = configparser.SafeConfigParser()
except ImportError:  # Python3
    import configparser

    config = configparser.ConfigParser()


class WebBreakerConfig(object):
    def __init__(self):
        self.install = os.path.abspath('')
        self.config = os.path.join(self.install, 'config.ini')
        self.etc = os.path.join(self.install, 'etc')
        self.git = os.path.join(self.install, 'etc', 'webinspect', '.git')
        self.log = os.path.join(self.install, 'log')

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
            return

        if not read_path == self.install:
            Logger.app.debug("Config webbreaker_install path is different than current directory")
            Logger.app.debug("Changing webbreaker_install path to Config settings")
            self.install = read_path
            self.config_path()
            self.etc_path()
            self.log_path()
            self.webinspect_git_path()
        else:
            Logger.app.debug("Config file & current configuration are the same.")

    # TODO: Put in error checking for all path functions
    # TODO: Turn into one method? 
    def config_path(self):
        old_path, core = os.path.split(self.config)
        while old_path != os.path.abspath(''):
            old_path, base = os.path.split(old_path)
            core = os.path.join(base, core)
        self.config = os.path.join(self.install, core)

    def etc_path(self):
        old_path, core = os.path.split(self.etc)
        while old_path != os.path.abspath(''):
            old_path, base = os.path.split(old_path)
            core = os.path.join(base, core)
        self.etc = os.path.join(self.install, core)

    def log_path(self):
        old_path, core = os.path.split(self.log)
        while old_path != os.path.abspath(''):
            old_path, base = os.path.split(old_path)
            core = os.path.join(base, core)
        self.log = os.path.join(self.install, core)

    def webinspect_git_path(self):
        old_path, core = os.path.split(self.git)
        while old_path != os.path.abspath(''):
            old_path, base = os.path.split(old_path)
            core = os.path.join(base, core)
        self.git = os.path.join(self.install, core)

    def parse_emailer_settings(self):
        emailer_dict = {}
        emailer_setting = os.path.abspath('.config')
        if os.path.exists(emailer_setting):
            config.read(emailer_setting)

            try:
                emailer_dict['smtp_host'] = config.get('emailer', 'smtp_host')
                emailer_dict['smtp_port'] = config.get('emailer', 'smtp_port')
                emailer_dict['from_address'] = config.get('emailer', 'from_address')
                emailer_dict['to_address'] = config.get('emailer', 'to_address')
                emailer_dict['email_template'] = config.get('emailer', 'email_template')
            except configparser.NoOptionError:
                Logger.console.error("{} has incorrect or missing values!".format(emailer_setting))

        else:
            Logger.console.info("Your scan email notifier is not configured: {}".format(emailer_setting))

        return emailer_dict

    def create_reporter(self):

        notifiers = []
        emailer_settings = self.parse_emailer_settings()
        notifiers.append(emailer.EmailNotifier(emailer_settings))

        return reporter.Reporter(notifiers)

    def test(self):
        return "DUMBER"

#
# #!/usr/bin/env python
# # -*- coding: utf-8 -*-
#
# import os
# import errno
# from webbreaker.notifiers import emailer
# from webbreaker.webbreakerlogger import Logger
# from webbreaker.notifiers import reporter
#
# try:
#     import ConfigParser as configparser
#
#     config = configparser.SafeConfigParser()
# except ImportError:  # Python3
#     import configparser
#
#     config = configparser.ConfigParser()
#
#
# class WebBreakerConfig(object):


#     #
#     # def git_path(self):
#     #
#     # def log_path(self):
#
#
#     def gitPath(self):
#         if os.path.isdir(self.git):
#             return self.git
#         else:
#             return self.etc
#
#     def parse_emailer_settings(self):
#         emailer_dict = {}
#         emailer_setting = os.path.abspath('.config')
#         if os.path.exists(emailer_setting):
#             config.read(emailer_setting)
#
#             try:
#                 emailer_dict['smtp_host'] = config.get('emailer', 'smtp_host')
#                 emailer_dict['smtp_port'] = config.get('emailer', 'smtp_port')
#                 emailer_dict['from_address'] = config.get('emailer', 'from_address')
#                 emailer_dict['to_address'] = config.get('emailer', 'to_address')
#                 emailer_dict['email_template'] = config.get('emailer', 'email_template')
#             except configparser.NoOptionError:
#                 Logger.console.error("{} has incorrect or missing values!".format(emailer_setting))
#
#         else:
#             Logger.console.info("Your scan email notifier is not configured: {}".format(emailer_setting))
#
#         return emailer_dict
#
#     def create_reporter(self):
#
#         notifiers = []
#         emailer_settings = self.parse_emailer_settings()
#         notifiers.append(emailer.EmailNotifier(emailer_settings))
#
#         return reporter.Reporter(notifiers)
#         #
#         # # TODO: Move to the WebInspectHelper class
#         # def fetch_webinspect_configs(self, options):
#         #
#         #     # Change to full path being main path
#         #     full_path = os.path.join(os.path.dirname(__file__), self.webinspect_dir)
#         #     # ./etc/webinspect/.git
#         #     git_dir = os.path.abspath(os.path.join(full_path, '.git'))
#         #
#         #     try:
#         #         if options['settings'] == 'Default':
#         #             Logger.app.debug("Default settings were used")
#         #         elif os.path.isdir(git_dir):
#         #             Logger.app.info("Updating your WebInspect configurations from {}".format(full_path))
#         #             check_output(['git', 'init', full_path])
#         #             check_output(['git', '--git-dir=' + git_dir, 'reset', '--hard'])
#         #             check_output(['git', '--git-dir=' + git_dir, 'pull', '--rebase'])
#         #             sys.stdout.flush()
#         #         elif not os.path.isdir(full_path):
#         #             Logger.app.info("Cloning your specified WebInspect configurations to {}".format(full_path))
#         #             check_output(['git', 'clone', self.webinspect_git, full_path])
#         #         else:
#         #             Logger.app.error(
#         #                 "No GIT Repo was declared in your .config, therefore nothing will be cloned!")
#         #     except (CalledProcessError, AttributeError) as e:
#         #         Logger.app.error("Uh oh something is wrong with your WebInspect configurations!!\nError: {}".format(e))
#         #     Logger.app.debug("Completed webinspect config fetch")
