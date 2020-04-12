import psycopg2

from auth_public import *

with psycopg2.connect(database=db, host=host, user=user, password=password) as con:
    cur = con.cursor()
    cur.execute("DROP TABLE IF EXISTS nepremicnine")
    cur.execute("CREATE TABLE nepremicnine(id serial PRIMARY KEY, ime text NOT NULL)")
    cur.execute("INSERT INTO nepremicnine(ime) VALUES('hiska')")
    cur.execute("INSERT INTO nepremicnine(ime) VALUES('bungalov')")
    cur.execute("INSERT INTO nepremicnine(ime) VALUES('sotor v portorozu')")
    cur.execute("SELECT * from nepremicnine")
    con.commit()
    print(cur.fetchall())