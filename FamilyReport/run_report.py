import sys
import smtplib
from email.mime.text import MIMEText
from email.header import Header
from email.utils import formataddr
import data.conf as conf

class FamilyReport(object):

    def __init__(self):
        pass

    def generate_email(self):
        pass

    def send_email(self):
        sender = conf.sender
        receivers = conf.receivers
        mail_msg = """
        <p>Test for family report</p>
        <p><a href="http://www.google.com">Search Google</a></p>
        """
        message = MIMEText(mail_msg, 'html', 'utf-8')
        message['From'] = Header("Mr. Egg", 'utf-8')
        message['To'] = Header("Ms. Egg", 'utf-8')
        subject = 'SMTP Test'
        message['Subject'] = Header(subject, 'utf-8')
        try:
            smtpObj = smtplib.SMTP('localhost')
            smtpObj.sendmail(sender, receivers, message.as_string())
            print("邮件发送成功")
        except smtplib.SMTPException:
            print("Error: 无法发送邮件")

    def run(self):
        self.send_email()

if __name__ == '__main__':
    # main process
    family_report = FamilyReport()
    family_report.run()
