#!/usr/bin/env python3

import report

report_key = 'annual_report'

f = '/relaisdata/reports/{0}/{1}'.format(report_key, report.get_report_filename(report_key))

q = """ DECLARE @startOfCurrentMonth DATETIME ;
 SET @startOfCurrentMonth = DATEADD(month, DATEDIFF(month, 0, CURRENT_TIMESTAMP), 0) ;
 SELECT L.INSTITUTION_NAME AS Borrower, 
        S.LIBRARY as Lender,
        D.SUPPLIER_CODE_1, 
        D.REQUEST_NUMBER, 
        PL.PICKUP_LOCATION_DESC AS PICKUP_LOCATION,
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
        R.CALL_NUMBER, 
        R.LOCAL_ITEM_FOUND
FROM    ((((ID_REQUEST R
        LEFT JOIN ID_DELIVERY D ON R.REQUEST_NUMBER = D.REQUEST_NUMBER)
        LEFT JOIN dbo.ID_LIBRARY L ON R.LIBRARY_ID = L.LIBRARY_ID)
        LEFT JOIN dbo.ID_SUPPLIER S ON D.SUPPLIER_CODE_1 = S.SUPPLIER_CODE)
        LEFT JOIN ID_PATRON P ON R.PATRON_ID = P.PATRON_ID AND R.LIBRARY_ID = P.LIBRARY_ID)
        LEFT JOIN dbo.ID_PICKUP_LOCATION PL ON D.DELIV_ADDRESS = PL.PICKUP_LOCATION AND R.LIBRARY_ID = PL.LIBRARY_ID
WHERE   R.DATE_SUBMITTED >= DATEADD(month, -12, @startOfCurrentMonth)
AND     R.DATE_SUBMITTED < @startOfCurrentMonth
ORDER BY D.REQUEST_NUMBER
"""
# Temporary columns to help staff figure out what they want.
columns = ['PATRON.INSTITUTION_NAME', 'DELIVERY.INSTITUTION_NAME', 'DELIVERY.SUPPLIER_CODE_1', 'DELIVERY.REQUEST_NUMBER',
           'DELIVERY.PICKUP_LOCATION', 'REQUEST.DATE_SUBMITTED (DATE)',
           'REQUEST.DATE_SUBMITTED (TIME)', 'DELIVERY.DATE_PROCESSED (DATE)',
           'DELIVERY.DATE_PROCESSED (TIME)', 'DELIVERY.DELIVERY_DATE', 'PATRON.PATRON_TYPE',
           'REQUEST.AUTHOR', 'REQUEST.TITLE', 'REQUEST.PUBLISHER', 'REQUEST.PUBLICATION_PLACE',
           'REQUEST.PUBLICATION_YEAR', 'REQUEST.ISBN', 'REQUEST.ISBN_2', 'REQUEST.OCLC_NUM',
           'REQUEST.CALL_NUMBER', 'REQUEST.LOCAL_ITEM_FOUND']


if __name__ == "__main__":
    report.write_report(q, f, cols=columns)