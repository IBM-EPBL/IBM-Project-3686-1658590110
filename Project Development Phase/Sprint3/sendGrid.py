import os

import mail
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import *


def send_email():
    from_email = Email('m.arunkumarmar12@gmail.com')
    to_email = To('bensonruban2001@gmail.com')
    subject = 'Personal expense tracker'
    content = Content("text/plain", "your balance is less than 1000")
    mail = Mail(from_email, to_email, subject, content)

    try:
        sg = SendGridAPIClient('<API KEY>')
        response = sg.send(mail)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(e)


send_email()