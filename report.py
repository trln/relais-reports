import os
import pymssql

# This is set on the EC2 instance via a script
# in /etc/profile.d
def_host = os.environ['RELAIS_DB_HOST']
def_user = os.environ['RELAIS_DB_USER']
def_password = os.environ['RELAIS_DB_PASSWORD']
def_db = os.environ['RELAIS_DB_NAME']


def conn(host=def_host, user=def_user, password=def_password, db=def_db):
    return pymssql.connect(host, user, password, db)

# All daily-run reports have a filename with this pattern
def get_report_filename(file_name_suffix, ext='.csv', dt=None):
    import datetime
    d = datetime.datetime.today()
    if dt is not None:
        d = dt
    return d.strftime('%Y_%m_%d_%H_%M_%S_{0}{1}'.format(file_name_suffix, ext))

# Query the DB and write out SQL into a file
def write_report(query, file_name=None, connection=None, cols=None):
    import csv
    f = get_report_filename('report') if file_name is None else file_name
    c = conn() if connection is None else connection
    cursor = c.cursor()
    cursor.execute(query)
    wr = csv.writer(open(file_name, 'w'))
    if cols is not None:
        wr.writerow(cols)
    for row in cursor:
        wr.writerow([str(s).encode("utf-8") for s in row])

def extract_date_from_filename(filename):
    import datetime
        a = [int(i) for i in filename.split('_')[0:3]]
        return datetime.datetime(a[0], a[1], a[2])

def extract_report_name_from_filename(filename):
        return '_'.join(filename.split('_')[-2:]).split('.')[0]
