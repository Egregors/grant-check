# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

import logging
from _md5 import md5
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from smtplib import SMTP_SSL
from time import sleep

import requests

logging.basicConfig(level=logging.DEBUG)

URL = 'http://grant.rscf.ru/sys/p?rd-person-app-tasks.html'
LOGIN = ''
PASS = ''

# yandex main for example
EMAIL_LOGIN = ''
EMAIL_PASS = ''


class Grant(object):
    def __init__(self, url, login, pass_, email_login, email_pass):
        self.url = url
        self.login = login
        self.pass_ = pass_
        self.email_login = email_login
        self.email_pass = email_pass

        # default response hash
        self.hash = md5()

    def send_mail(self, html):
        logging.info('send mail..')
        msg = MIMEMultipart('alternative')
        msg['From'] = self.email_login
        msg['To'] = self.email_login
        msg['Subject'] = 'Grant Check'
        message = 'olololo'

        msg.attach(MIMEText(message, 'plant'))
        msg.attach(MIMEText(html, 'html'))

        smtp = SMTP_SSL()
        smtp.connect('smtp.yandex.ru')
        smtp.login(self.email_login, self.email_pass)
        smtp.sendmail(self.email_login, self.email_login, msg.as_string())
        smtp.quit()

    def make_request(self):
        cookies = {
            'Uname': self.login,
            'Upass': self.pass_
        }
        logging.info('make requests to grant.rscf.ru')
        try:
            response = requests.get(URL, cookies=cookies)
            logging.info('response code: {}'.format(response.status_code))
        except Exception as e:
            logging.error(e)
            return None

        return response.text

    def go(self):
        while True:
            data = self.make_request()
            new_hash = md5(data.encode('utf'))

            if self.hash.hexdigest() != new_hash.hexdigest() and data:
                logging.info('diff hash:\n{}\n{}'.format(self.hash.hexdigest(), new_hash.hexdigest()))
                self.send_mail(data)
                self.hash = new_hash
                logging.info('new hash is: {}'.format(new_hash.hexdigest()))

            logging.info('sleep 60 min')
            sleep(3600)


if __name__ == '__main__':
    logging.info('start for {}'.format(LOGIN))
    grant = Grant(URL, LOGIN, PASS, EMAIL_LOGIN, EMAIL_PASS)
    grant.go()
