import sqlite3

baza = 'nepremicnine.db'

with sqlite3.connect(baza) as con:
    cur = con.cursor()
    cur.execute("DROP TABLE IF EXISTS nepremicnine")
    cur.execute("CREATE TABLE nepremicnine(id SERIAL PRIMARY KEY, ime text NOT NULL)")
    cur.execute("INSERT INTO nepremicnine(ime) VALUES('hiska')")
    cur.execute("SELECT * from nepremicnine")
    print(cur.fetchall())