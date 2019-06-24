# -*- coding: utf-8 -*-
import sys
import smtplib
from email.mime.text import MIMEText
from email.header import Header
from email.utils import formataddr
import pandas as pd
from weather import *
from gen_html import *
import requests


class FamilyReport(object):

    def __init__(self):
        pass

    def generate_email(self):
        pass

    def get_exchange_rate(self):
        exchange_rate_url = 'https://api.exchangeratesapi.io/latest?'
        payload = {'base': 'CNY'}
        exchange_rate_r = requests.get(exchange_rate_url, params=payload)
        exchange_rate_r.raise_for_status() # If not OK (200), raise exception
        res = exchange_rate_r.json()
        date_calculated = res['date']
        CAD_rate = 1.0 / res['rates']['CAD'] * 100
        USD_rate = 1.0 / res['rates']['USD'] * 100

        text = '''
        <h2>Exchange rate</h2>
        <p><font size="5" color="#E74C3C">100 CAD = {cad_rate:.2f} CNY</font></p>
        <p><font size="5" color="#E74C3C">100 USD = {usd_rate:.2f} CNY</font></p>
        <h4> The above information is provided by European Central Bank, updated on {date}. </h4>
        '''.format(cad_rate=CAD_rate, usd_rate=USD_rate, date=date_calculated)
        return text

    def send_email(self):

        param = {}

        # Date information
        date_of_landing='2018-11-12'
        date_of_today = date.today().strftime("%Y-%m-%d")
        day_of_year = date.today().strftime("%j")
        day_of_week = date.today().strftime("%A")
        weekday_of_today = date.today().weekday()
        # week_of_year = date.today().strftime("%W")
        percent = round((float(day_of_year) + 0.0) / 3.65, 1)
        progress_bar = str(percent) + '% <br />'
        tmp_bar = round(percent) * '\u25A0' + (100 - int(percent)) * '\u25A1'
        for idx in range(10):
            progress_bar += '\u25c0' + tmp_bar[idx*10:idx*10+10] + '\u25b6<br />'

        # Exchange rate
        exchange_rate_info = self.get_exchange_rate()

        # Weather
        list_weather = get_weather()
        param['weather'] = list_weather


        message = MIMEText(mail_msg, 'html', 'utf-8')
        message['From'] = Header("Bo Pang", 'utf-8')
        # message['To'] = Header("Ms. Egg", 'utf-8')
        subject = 'FAMILY REPORT @ {}'.format(date_of_today)
        message['Subject'] = Header(subject, 'utf-8')
        try:
            print("connect ...")
            server = smtplib.SMTP('{host}:{port}'.format(host=conf.mail_host, port=conf.mail_port))
            server.ehlo()
            server.starttls()
            print("login ...")
            server.login(conf.sender, conf.mail_pswd)
            print("send ...")
            receivers_today = conf.receivers
            if weekday_of_today in [1, 3, 5]:
                receivers_today += conf.conditional_receivers
            print("Today's receivers are: " + ", ".join(receivers_today))
            server.sendmail(conf.sender, receivers_today, message.as_string())
            server.quit()
            print("Successfully sent email.")
        except smtplib.SMTPException as e:
            print(e)

    def run(self):
        self.send_email()

if __name__ == '__main__':
    # main process
    family_report = FamilyReport()
    family_report.run()
    # family_report.get_exchange_rate()
