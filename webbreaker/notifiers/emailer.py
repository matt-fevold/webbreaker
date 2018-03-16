#!/usr/bin/env python
# -*- coding: utf-8 -*-
import smtplib
from webbreaker.common.webbreakerlogger import Logger

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


class EmailNotifier:
    def __init__(self, emailer_settings=None):
        self.name = "EmailNotifier"
        self.emailer_settings = emailer_settings

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
            Logger.app.error("Your emailer settings in config.ini is incorrectly configured. Error: {}".format(e))

    def __str__(self):
        return "EmailNotifier"
