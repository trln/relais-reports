#!/usr/bin/python 

import report

f = '/relaisdata/reports/unfilled_requests/{0}'.format(report.get_report_filename('unfilled_requests'))

q = """SELECT ID_DELIVERY.REQUEST_NUMBER, ID_DELIVERY.DATE_PROCESSED, 
              ID_REQUEST.AUTHOR, ID_REQUEST.TITLE 
       FROM ID_DELIVERY INNER JOIN ID_REQUEST 
       ON ID_DELIVERY.REQUEST_NUMBER = ID_REQUEST.REQUEST_NUMBER 
       WHERE 
	1=1 
	/*AND ID_DELIVERY.REQUEST_NUMBER Like 'duk%'*/ 
	AND ID_DELIVERY.DATE_PROCESSED > DATEADD(day, -1, GETDATE()) 
	AND ID_DELIVERY.SUPPLIER_CODE_1 Like '%list exhausted%' 
	ORDER BY ID_DELIVERY.REQUEST_NUMBER;"""

columns = ['Request Number', 'Date Processed', 'Author', 'Title']

if __name__ == "__main__":
	report.write_report(q, f, cols=columns)
