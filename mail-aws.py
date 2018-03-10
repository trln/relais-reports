#!/usr/bin/env python3

import smtplib
import email.utils
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
import unfilled_requests
import datetime


SENDER = 'jim.tuttle@unc.edu'
SENDERNAME = 'Jim Tuttle'
RECIPIENT  = 'jim.tuttle@unc.edu'
USERNAME_SMTP = os.environ['SMTP_USER']
PASSWORD_SMTP = os.environ['SMTP_PASSWORD']
HOST = "email-smtp.us-west-2.amazonaws.com"
PORT = 587
report_location = unfilled_requests.f

# The subject line of the email.
d = datetime.datetime.today().strftime('%Y-%m-%d')
SUBJECT = '[Relais Unfilled Report] {}'.format(d)

# The email body for recipients with non-HTML email clients.
BODY_TEXT = ("Relais Unfilled Report {}\r\n"
             "Please see the attached CSV file for unfilled requests."
             "This and previous reports are available at "
             "http://trln.relais.reports.s3-website-us-east-1.amazonaws.com/Unfilled%20Requests"
             " .".format(d)
            )

# The HTML body of the email.
BODY_HTML = """<html>
<head></head>
<body>
  <h1>Relais Unfilled Report {}</h1>
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
msg['Subject'] = SUBJECT
msg['From'] = email.utils.formataddr((SENDERNAME, SENDER))
msg['To'] = RECIPIENT


# Record the MIME types of both parts - text/plain and text/html.
part1 = MIMEText(BODY_TEXT, 'plain')
part2 = MIMEText(BODY_HTML, 'html')

# Build the attachment.
report_file = open(report_location)
attachment = MIMEText(report_file.read(), _subtype="csv", _charset="utf-8")
report_file.close()
attachment.add_header("Content-Disposition", "attachment",
                      filename="{}".format(report_location.rsplit('/', 1,)[1]))
msg.attach(attachment)


# Attach parts into message container.
# According to RFC 2046, the last part of a multipart message, in this case
# the HTML message, is best and preferred.
msg.attach(part1)
msg.attach(part2)

# Try to send the message.
try:
    server = smtplib.SMTP(HOST, PORT)
    server.ehlo()
    server.starttls()
    # stmplib docs recommend calling ehlo() before & after starttls()
    server.ehlo()
    server.login(USERNAME_SMTP, PASSWORD_SMTP)
    server.sendmail(SENDER, RECIPIENT, msg.as_string())
    server.close()
# Display an error message if something goes wrong.
except Exception as e:
    print ("Error: ", e)
else:
    print ("Email sent!")