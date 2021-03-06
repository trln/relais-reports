#!/usr/bin/env python3

import report


reportname = report.get_report_filename('unfilled_requests')
f = '/relaisdata/reports/unfilled_requests/{0}'.format(reportname)


def build_query():
    """Return MS-SQL query and column names for unfilled request details."""
    q = """SELECT 
      D.REQUEST_NUMBER,
      convert(varchar, D.DATE_PROCESSED, 101) as DATE_PROCESSED, 
      convert(varchar, D.DATE_PROCESSED, 108) as TIME_PROCESSED,
      convert(varchar, R.DATE_SUBMITTED, 101) as DATE_RECEIVED, 
      convert(varchar, R.DATE_SUBMITTED, 108) as TIME_RECEIVED,
      R.AUTHOR, 
      R.TITLE,
      L.INSTITUTION_NAME as REQUESTING_INSTITUTION
     FROM ID_DELIVERY D INNER JOIN ID_REQUEST R
     ON D.REQUEST_NUMBER = R.REQUEST_NUMBER
     JOIN ID_LIBRARY L
     ON R.LIBRARY_ID = L.LIBRARY_ID 
     WHERE 
     1=1 
     AND D.DATE_PROCESSED > DATEADD(day, -1, GETDATE()) 
     AND D.SUPPLIER_CODE_1 Like '%list exhausted%' 
     ORDER BY D.REQUEST_NUMBER ;"""
    columns = ['Request Number', 'Date Processed', 'TimeProcessed',
               'Date Received', 'Time Received', 'Author', 'Title',
               'Requesting Institution']
    return q, columns


def main():
    """Main logic to makes this module callable from other code."""
    q, columns = build_query()
    report.write_report(q, f, cols=columns)


if __name__ == "__main__":
    main()


