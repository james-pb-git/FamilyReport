import sys
import smtplib
import datetime
from email.mime.text import MIMEText
from email.header import Header
from email.utils import formataddr
import pandas as pd
import numpy as np
from data import conf

def days_between(d1, d2):
    d1 = datetime.datetime.strptime(d1, "%Y-%m-%d")
    d2 = datetime.datetime.strptime(d2, "%Y-%m-%d")
    return abs((d2 - d1).days)

def ord(n):
    return str(n)+("th" if 4 <= n%100 <= 20 else {1:"st",2:"nd",3:"rd"}.get(n%10, "th"))

class FamilyReport(object):

    def __init__(self):
        pass

    def generate_email(self):
        pass

    def send_email(self):

        # Date information

        date_of_landing='2018-11-12'
        date_of_today = datetime.date.today().strftime("%Y-%m-%d")
        day_of_year = datetime.date.today().strftime("%j")
        day_of_week = datetime.date.today().strftime("%A")
        # week_of_year = datetime.date.today().strftime("%W")
        percent = round((float(day_of_year) + 0.0) / 3.65, 1)
        progress_bar = str(percent) + '% |' + int(percent) * '#' + (100 - int(percent)) * '-' + '|'

        # Food expenses
        df = pd.read_csv(conf.data_path + '/' + 'food_expense', sep='\t')
        cost = round(df['Expense'].sum(), 2)
        days_since_landing = days_between(date_of_landing, date_of_today)

        mail_msg = """
        <h3>This is an automatically generated email, however, you can reply if you insist.</h3>
        <h3>To unsubscribe, please discuss with your husband in person.</h3>
        <hr />
        <h2>Date information</h2>
        <p>Today is <b>{date}</b>, <b>{week}</b>, the {doy} day in this year.</p>
        <p>This year's progress is as follows: </p>
        <p>{progress}</p>
        <hr />
        <h2>Expenses on food</h2>
        <p>We've landed in Toronto for {dsl} days, and spent ${cost} on food.</p>
        <p>Our average daily expense on food is: <b> ${cpd} / d </b>.</p>
        <hr />
        """.format(date=date_of_today, week=day_of_week, doy=ord(int(day_of_year)),
                   progress=progress_bar, dsl=days_since_landing, cost=cost, cpd=round(float(cost)/days_since_landing, 2))
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
            server.sendmail(conf.sender, conf.receivers, message.as_string())
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
