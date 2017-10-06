#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from subprocess import CalledProcessError
try:
    from email.MIMEMultipart import MIMEMultipart
    from email.MIMEText import MIMEText
except ImportError: #Python3
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
import smtplib
from webbreaker.webbreakerlogger import Logger

try:
    import ConfigParser as configparser
except ImportError: #Python3
    import configparser

try:  # Python 2
    config = configparser.SafeConfigParser()
except NameError:  # Python 3
    config = configparser.ConfigParser()

class EmailNotifier(object):
    def __init__(self):
        self.__read_settings__()

    def notify(self, recipient, subject, git_url, ssc_url, state):
        try:
            msg = MIMEMultipart()
            msg['From'] = self.from_address
            msg['To'] = recipient
            msg['Subject'] = subject

            html = str(self.email_template).format(git_url, state, ssc_url)
            msg.attach(MIMEText(html, 'html'))

            mail_server = smtplib.SMTP(self.smtp_host, self.smtp_port)
            mail_server.sendmail(msg['From'], msg['To'], msg.as_string())

            mail_server.quit()
        except (Exception, AttributeError) as e:  # we don't want email failure to stop us, just log that it happened
            Logger.app.error("Error sending email. {}".format(e.message))
            Logger.console.error("Error sending email, see log: {}!".format(Logger.app_logfile))

    def __read_settings__(self):
        settings_file = os.path.abspath(os.path.join('webbreaker', 'webbreakeragent', 'email.ini'))
        try:
            config.read(settings_file)
            self.smtp_host = config.get("emailer", "smtp_host")
            self.smtp_port = config.get("emailer", "smtp_port")
            self.from_address = config.get("emailer", "from_address")
            self.email_template = config.get("emailer", "email_template")
            self.default_to_address = config.get("emailer", "default_to_address")

        except (configparser.NoOptionError, CalledProcessError) as noe:
            Logger.console.error("{} has incorrect or missing values {}".format(settings_file, noe))
        except configparser.Error as e:
            Logger.app.error("Error reading {} {}".format(settings_file, e))