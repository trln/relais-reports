#!/usr/bin/python 

import report

report_key = 'requests_summary'

f = '/relaisdata/reports/{0}/{1}'.format(report_key, report.get_report_filename(report_key))

q = """DECLARE @startOfCurrentMonth DATETIME ;
 SET @startOfCurrentMonth = DATEADD(month, DATEDIFF(month, 0, CURRENT_TIMESTAMP), 0) ;
 SELECT
  P.INSTITUTION_NAME AS Borrower,
  D.INSTITUTION_NAME as Lender,
  D.REQUEST_NUMBER,
  P.PATRON_ID,
  P.PICKUP_LOCATION_DESC AS PICKUP_LOCATION,
  convert(varchar, R.DATE_SUBMITTED, 101) as REQUEST_DATE, 
  convert(varchar, R.DATE_SUBMITTED, 108) as REQUEST_TIME,
  convert(varchar, D.DATE_PROCESSED, 101) as DATE_PROCESSED, 
  convert(varchar, D.DATE_PROCESSED, 108) as TIME_PROCESSED,
  D.DELIVERY_DATE AS RECEIVED_DATE,
  P.PATRON_TYPE,
  R.AUTHOR, 
  R.TITLE,
  R.PUBLISHER,
  R.PUBLICATION_PLACE,
  R.PUBLICATION_YEAR,
  R.ISBN,
  R.ISBN_2,
  R.OCLC_NUM,
  -- LCCN
  R.CALL_NUMBER,
  R.LOCAL_ITEM_FOUND
 FROM ID_DELIVERY D INNER JOIN ID_REQUEST R
 ON D.REQUEST_NUMBER = R.REQUEST_NUMBER
 JOIN ID_LIBRARY L
 ON R.LIBRARY_ID = L.LIBRARY_ID 
 JOIN 
 (SELECT P.PATRON_ID,
     PT.PATRON_TYPE, 
         PB.INSTITUTION_NAME,
     PB.LIBRARY,
     PL.PICKUP_LOCATION_DESC
  FROM ID_PATRON P
  JOIN ID_PATRON_TYPE PT
  ON P.PATRON_TYPE = PT.PATRON_TYPE
  JOIN ID_PICKUP_LOCATION PL
  ON P.PICKUP_LOCATION = PL.PICKUP_LOCATION
  JOIN ID_LIBRARY PB
  ON P.LIBRARY_ID = PB.LIBRARY_ID) P
  on R.PATRON_ID = P.PATRON_ID
  WHERE 
 1=1 
 AND R.DATE_SUBMITTED >= DATEADD(month, -1, @startOfCurrentMonth)
 AND R.DATE_SUBMITTED < @startOfCurrentMonth
 ORDER BY D.REQUEST_NUMBER ;"""


#columns = ['Borrower', 'Lender', 'Request Number', 
#           'Pick Up Location', 'Request Date', 'Ship Date',
#           'Received Date', 'Status', 'Shelving Location',
#           'Patron Type', 'Author', 'Title', 'Publisher',
#           'Publication Place', 'Publication Year', 'ISBN',
#           'OCLC', 'LCCN', 'Call Number', 'Local Item Found']

# Temporary columns to help staff figure out what they want.
columns = ['PATRON.INSTITUTION_NAME', 'DELIVERY.INSTITUTION_NAME', 'DELIVERY.REQUEST_NUMBER',
           'PATRON.PATRON_ID', 'PATRON.PICKUP_LOCATION_DESC', 'REQUEST.DATE_SUBMITTED (DATE)',
           'REQUEST.DATE_SUBMITTED (TIME)', 'DELIVERY.DATE_PROCESSED (DATE)',
           'DELIVERY.DATE_PROCESSED (TIME)', 'DELIVERY.DELIVERY_DATE', 'PATRON.PATRON_TYPE',
           'REQUEST.AUTHOR', 'REQUEST.TITLE', 'REQUEST.PUBLISHER', 'REQUEST.PUBLICATION_PLACE',
           'REQUEST.PUBLICATION_YEAR', 'REQUEST.ISBN', 'REQUEST.ISBN_2', 'REQUEST.OCLC_NUM',
           'REQUEST.CALL_NUMBER', 'REQUEST.LOCAL_ITEM_FOUND']


if __name__ == "__main__":
  report.write_report(q, f, cols=columns)
