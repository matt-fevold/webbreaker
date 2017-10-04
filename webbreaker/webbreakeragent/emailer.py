#!/usr/bin/env python
# -*- coding: utf-8 -*-


try:
    from email.MIMEMultipart import MIMEMultipart
    from email.MIMEText import MIMEText
except ImportError: #Python3
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
import smtplib
from webbreaker.webbreakerlogger import Logger


class EmailNotifier(object):
    def __init__(self):
        # TODO: Read and init from email.ini
        pass

    def notify(self, recipient, subject, git_url, ssc_url):
        try:
            msg = MIMEMultipart()
            msg['From'] = self.emailer_settings['from_address']
            msg['To'] = recipient
            msg['Subject'] = subject

            html = str(self.emailer_settings['email_template']).format(git_url, ssc_url)
            msg.attach(MIMEText(html, 'html'))

            mail_server = smtplib.SMTP(self.emailer_settings['smtp_host'], self.emailer_settings['smtp_port'])
            mail_server.sendmail(msg['From'], msg['To'], msg.as_string())

            mail_server.quit()
        except (Exception, AttributeError) as e:  # we don't want email failure to stop us, just log that it happened
            Logger.app.error("Error sending email. {}".format(e.message))
            Logger.console.error("Error sending email, see log: {}!".format(Logger.app_logfile))
