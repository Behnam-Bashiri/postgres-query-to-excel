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
    cur.execute('''
select *
from pg_catalog.pg_tables
where schemaname = 'public';
''')
    tables_quey = {}
    index_tables = 0
    for table_name in cur:
        tables_quey[index_tables] = '{}.{}'.format(table_name[0],table_name[1])
        print("{}. {}.{}".format(index_tables,table_name[0],table_name[1]))
        index_tables +=1
    tables_slector  = int(input("enter table index number(INT): ->"))
    conditions = str(input("Are you have condition for quety ? (T/F)"))
    if conditions == 'T':
        condition_txt = str(input("condition ->"))
        conditions = str(input("Are you have JOIN for quety ? (T/F)"))
        if conditions == 'T':
            tables_slector_join  = int(input("enter table JOIN index number(INT): ->"))
            cur.execute('SELECT * FROM {} JOIN {} ON {}.{}_ptr_id = {}.id WHERE {}'\
                        .format(tables_quey[tables_slector],tables_quey[tables_slector_join],tables_quey[tables_slector],tables_quey[tables_slector_join].split('api_')[1],tables_quey[tables_slector_join],condition_txt))
        elif conditions == "F":
            cur.execute('SELECT * FROM {} WHERE {}'\
                        .format(tables_quey[tables_slector],condition_txt))
    elif conditions == 'F':
        conditions = str(input("Are you have JOIN for quety ? (T/F)"))
        if conditions == 'T':
            tables_slector_join  = int(input("enter table JOIN index number(INT): ->"))
            cur.execute('SELECT * FROM {} JOIN {} ON {}.{}_ptr_id = {}.id'\
                        .format(tables_quey[tables_slector],tables_quey[tables_slector_join],tables_quey[tables_slector],tables_quey[tables_slector_join].split('api_')[1],tables_quey[tables_slector_join]))
        elif conditions == "F":
            cur.execute('SELECT * FROM {}'.format(tables_quey[tables_slector]))
# SELECT * FROM public.api_finder_profit JOIN public.api_base_crypto ON public.api_finder_profit.base_crypto_ptr_id = public.api_base_crypto.id ; 
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