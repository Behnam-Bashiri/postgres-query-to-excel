import psycopg2
from openpyxl import Workbook

def fetch(key):
    # connect to the database
    print("connecting database .... ")
    conn = psycopg2.connect(
        host=key['host'],
        database=key['db'],
        user=key['user'],
        password=key['password']
    )
    print("connected !")
    # execute the query
    cur = conn.cursor()
    cur.execute(key['execute'])
    rows = cur.fetchall()
    print("fetch done !")

    # create a new workbook
    wb = Workbook()

    # select the active worksheet
    ws = wb.active
    print("template excel create ....")
    # write the header row
    header = [desc[0] for desc in cur.description]
    ws.append(header)

    # write the data rows
    for row in rows:
        ws.append(row)

    # save the workbook
    wb.save("{}.xlsx".format(key['excelName']))

    # close the connection
    cur.close()
    conn.close()
    print("almost done :)")