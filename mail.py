#!/usr/bin/env python3

import os
import smtplib
import unfilled_requests
import report

smtp_user = os.environ['SMTP_USER']
smtp_password = os.environ['SMTP_PASSWORD']

print(smtp_user)
print(smtp_password)

# file_name = report.get_report_filename('unfilled_requests')


def main():
    attachment = unfilled_requests.f

    smtp = smtplib.SMTP("email-smtp.us-east-1.amazonaws.com")
    smtp.starttls()
    smtp.login(SESSMTPUSERNAME, SESSMTPPASSWORD)
    smtp.sendmail(me, you, msg)


if __name__ == "__main__":
    main()
