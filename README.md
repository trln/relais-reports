##  OCLC Relais Unfilled Requests Reporter

Generate and email reports about unfilled requests in OCLC Relais

## Features

Your staff wants to know when an interlibrary loan request goes unfilled, right?  This project makes it easy to email reports to staff on a schedule (we do it daily at 5 AM) and retains 14 days of reports in a web-accessible archive.

The email is designed to be easy for staff to consume, too.  The subject line shows the data and number of unfilled requests like so:  [listname] Unfilled Requests:4 2018-03-20.  [listname] is the subject line prefix that our listserv system automatically adds to incoming emails.  The body contains a header that also shows that information and an attached CSV of the unfilled requests is attached if there are any.  If not, there is not attachment.  

Here's a sample email:

Subject: [listname] Unfilled Requests:4 2018-03-20

Body: 

### TRLN Direct Unfilled Requests: 4

There are 4 requests today.
Please see the attached CSV file for unfilled requests. This and previous reports are available here. 

The attached CSV looks like this:
Request Number	Date Processed	TimeProcessed	Date Received	Time Received	Author	Title	Requesting Institution
NCS-10013642	03/19/2018	08:51:29	03/16/2018	11:12:19	JOHN GREEN	LOOKING FOR ALASKA	North Carolina State University
NCS-10013692	03/19/2018	12:52:57	03/18/2018	02:04:48	OLYMPIA NICODEMI	AN INTRODUCTION TO ABSTRACT ALGEBRA	North Carolina State University
NCS-10013705	03/19/2018	12:51:06	03/18/2018	23:41:54	STUART TYSON SMITH	ASKUT IN NUBIA	North Carolina State University



## Requirements

You'll need: 
- an Amazon Web Services (AWS) instance
- Python 3
- pymssql 

## Getting Started

After installing the prerequisits and confirming that all of the credentials and connects are working, to automate the process you'll need the following:

Cron Job

This is our daily cron job, daily.sh

#!/bin/bash                                                                                                                                
                                                                                                                                           
. /etc/profile.d/relais_db_env.sh                                                                                                          
                                                                                                                                           
# First run all the reports                                                                                                                
/relaisdata/scripts/unfilled_requests.py                                                                                                   
                                                                                                                                           
# Then sync with s3                                                                                                                        
/relaisdata/scripts/sync_with_s3.py                                                                                                        
                                                                                                                                           
# Then email report to user listserv                                                                                                       
/relaisdata/scripts/mail-aws.py 

It's run daily at 6 AM.  Here's the line from cron:

0 6 * * * /relaisdata/cron/daily.sh > /relaisdata/cron/log

And here is the /etc/profile.d/relais_db_env.sh file with our details removed:

export RELAIS_DB_HOST=                                                                                                     
export RELAIS_DB_USER=                                                                                                             
export RELAIS_DB_PASSWORD=                                                                                                          
export RELAIS_DB_NAME=                                                                                                                
export RELAIS_S3_BUCKET=
export SMTP_USER=
export SMTP_PASSWORD=

We're using Amazon Simple Email Service to provide SMTP.  See https://aws.amazon.com/ses/

This is the /relaisdata/cron/monthly.sh script:

#!/bin/bash

. /etc/profile.d/relais_db_env.sh

# First run all the reports
/relaisdata/scripts/requests_summary.py

