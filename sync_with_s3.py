#!/usr/bin/env python3

import os
import boto3
import report
from datetime import datetime, timedelta

# Number of days of historical reports to keep
max_report_age_days = {'unfilled_requests' : 14, 'requests_summary' : 90, 'annual_reports': 700, 'tableau_reports': 185}

# Where are the reports stored locally
local_reports_base_path = '/relaisdata/reports'

# Name of the bucket where reports are stored
s3_bucket_name = os.environ['RELAIS_S3_BUCKET']

# Report: [Remote report folder, Local report folder, Report file name suffix]
reports = {'Unfilled Requests':['Unfilled Requests', 'unfilled_requests', 'unfilled_requests'],
           'Requests Summary' :['Requests Summary', 'requests_summary', 'requests_summary'],
           'Annual Reports' :['Annual Reports', 'annual_reports', 'annual_reports'],
           'Tableau Reports' :['Tableau Reports', 'tableau_reports', 'tableau_reports']}


def keep(filename):
    report_date = report.extract_date_from_filename(filename)
    report_name = report.extract_report_name_from_filename(filename)
    today = datetime.today()
    max_report_age = timedelta(days=max_report_age_days[report_name])
    return max_report_age >= today - report_date


# Gets a list of report files from S3
def get_remote_file_paths(report_folder_name):
    s3c = boto3.client('s3')
    results = s3c.list_objects_v2(Bucket=s3_bucket_name, StartAfter=report_folder_name)['Contents']
    remote_files = [rf['Key'] for rf in results
                        if rf['Key'].startswith(report_folder_name) and rf['Key'].endswith('.csv')]
    return remote_files


# Does all the operations
def sync():
    b = boto3.resource('s3').Bucket(s3_bucket_name)
    for report, vals in reports.items():
        remote_folder = vals[0]
        remote_file_paths = get_remote_file_paths(remote_folder)
        for path in remote_file_paths:
            filename = path.split('/')[-1]
            if not keep(filename):
                #print("Deleting {0}".format(path))
                b.delete_objects(Delete={'Objects':[{'Key':path}]})
        local_folder = os.path.join(local_reports_base_path, vals[1])
        local_file_paths = [f for f in os.listdir(local_folder) if f.endswith('.csv')]
        for path in local_file_paths:
            local = os.path.join(local_folder, path)
            if keep(path):
                remote = os.path.join(remote_folder, path)
                #print("Uploading {0} to {1}".format(local, remote))
                b.upload_file(local, remote)
            else:
                #print("Deleting local {0}".format(local))
                os.remove(local)


# Executes sync if run directly from the command line
if __name__ == "__main__":
    sync()
