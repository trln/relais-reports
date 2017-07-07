#!/usr/bin/python

import os
import boto3
import report
from datetime import datetime, timedelta

# Number of days of historical reports to keep
num_days_reports_to_retain = 14

# Where are the reports stored locally
local_reports_base_path = '/relaisdata/reports'

# Name of the bucket where reports are stored
s3_bucket_name = os.environ['RELAIS_S3_BUCKET']

# Report: [Remote report folder, Local report folder, Report file name suffix]
reports = {'Unfilled Requests':['Unfilled Requests', 'unfilled_requests', 'unfilled_requests'] }

# Computes the reference list of files based on todays date
def compute_reference_files(filename_suffix):
        candidates = [report.get_report_filename(filename_suffix, dt = d) 
                      for d in [datetime.today() - timedelta(days=i) for i in range(0, num_days_reports_to_retain)]]
	return candidates

# Computes what files to upload to S3 and what to delete from S3
def compute_files_to_put_and_delete(local_report_folder, reference_files, remote_report_folder, remote_files):
	deletes = [remote_report_folder + '/' + f for f in list(set(remote_files).difference(set(reference_files)))]
	candidate_puts = list(set(reference_files).difference(set(remote_files)))
	candidate_local_paths = [[f, os.path.join(local_reports_base_path, local_report_folder, f)] for f in candidate_puts]
	puts = [[p, remote_report_folder + '/' + f] for f,p in candidate_local_paths if os.path.exists(p)]
	return {'put':puts, 'delete':deletes}

# Gets a list of report files from S3
def get_remote_file_paths(report_folder_name):
	s3c = boto3.client('s3')
	results = s3c.list_objects_v2(Bucket=s3_bucket_name, StartAfter=report_folder_name)['Contents']
	remote_files = [rf['Key'].split('/')[1] for rf in results 
                        if rf['Key'].startswith(report_folder_name) and rf['Key'].endswith('.csv')]
	return remote_files

# Does all the operations
def sync():
	b = boto3.resource('s3').Bucket(s3_bucket_name)
	for report, vals in reports.iteritems():
		remote_folder = vals[0]
		local_folder = vals[1]
		file_name_suffix = vals[2]
		reference_files = compute_reference_files(file_name_suffix)
		remote_file_paths = get_remote_file_paths(remote_folder)
		paths = compute_files_to_put_and_delete(local_folder, reference_files, remote_folder, remote_file_paths)
		for local,remote in paths['put']:
			print("Uploading {0} to {1}".format(local, remote))
			b.upload_file(local, remote)
		for remote in paths['delete']:
			print("Deleting {0}".format(remote))
			b.delete_objects(Delete={'Objects':[{'Key':remote} for remote in paths['delete']]})

# Executes sync if run directly from the command line
if __name__ == "__main__":
	sync()
