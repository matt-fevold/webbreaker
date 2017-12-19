#!/usr/bin/env python
# -*- coding: utf-8 -*-
import smtplib
import os
from webbreaker.notifiers.notifier import Notifier
from webbreaker.webbreakerlogger import Logger
from webbreaker.confighelper import Config
from subprocess import CalledProcessError

try:
    from email.MIMEMultipart import MIMEMultipart
    from email.MIMEText import MIMEText
    import ConfigParser as configparser

    config = configparser.SafeConfigParser()


except ImportError:  # Python3
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    import configparser

    config = configparser.ConfigParser()


class EmailNotifier(Notifier):
    def __init__(self, emailer_settings=None):
        if emailer_settings:
            self.emailer_settings = emailer_settings
        else:
            self.is_agent = True
            self.__read_agent_settings__()
        Notifier.__init__(self, "EmailNotifier")

    def notify(self, event):
        try:
            msg = MIMEMultipart()
            msg['From'] = self.emailer_settings['from_address']
            msg['To'] = self.emailer_settings['to_address']
            msg['Subject'] = "{0} {1}".format(event['subject'], event['scanname'])
            targets = "".join(["<li>{0}</li>".format(t) for t in event['targets']]) if event['targets'] else ""
            html = str(self.emailer_settings['email_template']).format(event['server'],
                                                                       event['scanname'],
                                                                       event['scanid'],
                                                                       event['subject'],
                                                                       targets)
            msg.attach(MIMEText(html, 'html'))

            mail_server = smtplib.SMTP(self.emailer_settings['smtp_host'], self.emailer_settings['smtp_port'])
            mail_server.sendmail(msg['From'], msg['To'], msg.as_string())

            mail_server.quit()
        except (Exception, AttributeError) as e:  # we don't want email failure to stop us, just log that it happened
            Logger.app.error("Error sending email. Error: {}".format(e.message))

    def cloudscan_notify(self, recipient, subject, git_url, ssc_url, state, scan_id, scan_name):
        try:
            msg = MIMEMultipart()
            msg['From'] = self.from_address
            msg['To'] = recipient
            msg['Subject'] = subject

            html = str(self.email_template).format(git_url, ssc_url, scan_name, scan_id, state, self.chatroom)
            msg.attach(MIMEText(html, 'html'))

            mail_server = smtplib.SMTP(self.smtp_host, self.smtp_port)
            mail_server.sendmail(msg['From'], msg['To'], msg.as_string())

            mail_server.quit()
        except (Exception, AttributeError) as e:  # we don't want email failure to stop us, just log that it happened
            Logger.app.error("Error sending email. Error: {}".format(e.message))

    def __read_agent_settings__(self):
        settings_file = Config().config
        try:
            config.read(settings_file)
            self.smtp_host = config.get("agent_emailer", "smtp_host")
            self.smtp_port = config.get("agent_emailer", "smtp_port")
            self.from_address = config.get("agent_emailer", "from_address")
            self.email_template = config.get("agent_emailer", "email_template")
            self.default_to_address = config.get("agent_emailer", "default_to_address")
            self.chatroom = config.get("agent_emailer", "chatroom")

        except (configparser.NoOptionError, CalledProcessError) as noe:
            Logger.console.error("{} has incorrect or missing values {}".format(settings_file, noe))
        except configparser.Error as e:
            Logger.app.error("Error reading {} {}".format(settings_file, e))

    def __str__(self):
        return "EmailNotifier"
