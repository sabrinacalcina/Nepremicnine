import psycopg2

from conf_baza import *

conn_string = "host='{0}' dbname='{1}' user='{2}' password='{3}'".format(host, dbname, user, password)

with psycopg2.connect(conn_string) as con:
    cur = con.cursor()
    cur.execute("DROP TABLE IF EXISTS nepremicnine")
    cur.execute("CREATE TABLE nepremicnine(id serial PRIMARY KEY, ime text NOT NULL)")
    cur.execute("INSERT INTO nepremicnine(ime) VALUES('hiska')")
    cur.execute("INSERT INTO nepremicnine(ime) VALUES('bungalov')")
    cur.execute("SELECT * from nepremicnine")
    con.commit()
    print(cur.fetchall())