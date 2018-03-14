#!/usr/bin/env python3

import smtplib
import email.utils
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
import unfilled_requests
import datetime


sender = 'trln-direct@listserv.unc.edu'
sender_name = 'TRLN Direct'
recipient = 'trln-direct@listserv.unc.edu'
smtp_user = os.environ['SMTP_USER']
smtp_password = os.environ['SMTP_PASSWORD']
host = "email-smtp.us-east-1.amazonaws.com"
port = 587
report_location = unfilled_requests.f


def request_count(path):
    """Return number of unfilled requests in report"""
    requests = sum(1 for line in open(path)) - 1
    print(requests)
    return requests


def build_email(requests, path):
    """Construct the message and add attachment"""

    # The subject line of the email.
    d = datetime.datetime.today().strftime('%Y-%m-%d')
    subject = '[TRLN Direct Unfilled Report] {}'.format(d)

    # The email body for recipients with non-HTML email clients.
    body_text = ("TRLN Direct Unfilled Report  {}\r\n"
                 "Please see the attached CSV file for unfilled requests."
                 "This and previous reports are available at "
                 "http://trln.relais.reports.s3-website-us-east-1.amazonaws.com/Unfilled%20Requests"
                 " .".format(d)
    )

    # The HTML body of the email.
    body_html = """<html>
    <head></head>
    <body>
      <h1>TRLN Direct Unfilled Report {}</h1>
      <p>Please see the attached CSV file for unfilled requests. 
      This and previous reports are available 
      <a href='http://trln.relais.reports.s3-website-us-east-1.amazonaws.com/Unfilled%20Requests'>
      here</a>.
      </p>
    </body>
    </html>
                """.format(d)

    # Create message container - the correct MIME type is multipart/alternative.
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = email.utils.formataddr((sender_name, sender))
    msg['To'] = recipient

    # Record the MIME types of both parts - text/plain and text/html.
    part1 = MIMEText(body_text, 'plain')
    part2 = MIMEText(body_html, 'html')

    # Build the attachment.
    report_file = open(report_location)
    attachment = MIMEText(report_file.read(), _subtype="csv", _charset="utf-8")
    report_file.close()
    attachment.add_header("Content-Disposition", "attachment",
                          filename="{}".format(report_location.rsplit('/', 1, )[1]))
    msg.attach(attachment)

    # Attach parts into message container.
    # According to RFC 2046, the last part of a multipart message, in this case
    # the HTML message, is best and preferred.
    msg.attach(part1)
    msg.attach(part2)


def send_email():
    # Try to send the message.
    try:
        server = smtplib.SMTP(host, port)
        server.ehlo()
        server.starttls()
        # stmplib docs recommend calling ehlo() before & after starttls()
        server.ehlo()
        server.login(smtp_user, smtp_password)
        server.sendmail(sender, recipient, msg.as_string())
        server.close()
    # Display an error message if something goes wrong.
    except Exception as e:
        print ("Error: ", e)
    else:
        print ("Email sent!")


def main():
    """Main logic to makes this module callable from other code."""
    requests = request_count(report_location)
    build_email(requests, report_location)

if __name__ == "__main__":
    main()


