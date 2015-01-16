#!/usr/bin/python3

import psycopg2
from prettytable import PrettyTable

conn = psycopg2.connect("host=iservdb.cloudopenlab.org.tw dbname=eternity1357_db_6813 user=eternity1357_user_6813 password=Iie2steQ")
cur = conn.cursor()
cur.execute("""SELECT * FROM "your_twitt_tablename" WHERE q = '王建民' ORDER BY user_id""")
rows = cur.fetchall()

table = PrettyTable(['user_id', 'user_name', 'tweet'])
table.align['user_id'] = 'l'
table.padding_width = 1

for i in range(0, len(rows)):
    table.add_row([rows[i][3], rows[i][2], rows[i][1]])

table.sortby = 'user_id'

print (table)
