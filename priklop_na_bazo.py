import sqlite3
import csv

baza = 'nepremicnine.db'

#UVOZ SQL SKRIPTE
def uvoziSQL(cur, datoteka):
    with open(datoteka) as f:
        skripta = f.read()
        cur.executescript(skripta)

#UVOZ CSV-JA
def uvoziCSV(cur, tabela):
    with open('test_podatki/{0}.csv'.format(tabela)) as csvfile:
        podatki = csv.reader(csvfile)
        vsiPodatki = [vrstica for vrstica in podatki]
        glava = vsiPodatki[0]
        vrstice = vsiPodatki[1:]
        cur.executemany("INSERT INTO {0} ({1}) VALUES ({2})".format(
            tabela, ",".join(glava), ",".join(['?']*len(glava))), vrstice)

with sqlite3.connect(baza) as baza:
    cur = baza.cursor()
    uvoziSQL(cur, 'test_tabele.sql')
    uvoziCSV(cur, 'regije')
    uvoziCSV(cur, 'nepremicnine')
    uvoziCSV(cur, 'agencije')





# #UVOZ Z SQL SKRIPTAMI
# def uvoziSQL(cur, datoteka):
#     with open(datoteka) as f:
#         skripta = f.read()
#         cur.executescript(skripta)

# with sqlite3.connect(baza) as baza:
#     cur = baza.cursor()
#     uvoziSQL(cur, 'tabele.sql')
#     uvoziSQL(cur, 'test_podatki/agencije.sql')
#     uvoziSQL(cur, 'test_podatki/nepremicnine.sql')
#     uvoziSQL(cur, 'test_podatki/regije.sql')




    #c.execute("DROP TABLE IF EXISTS regije")
    #c.execute("CREATE TABLE regije(id integer PRIMARY KEY AUTOINCREMENT, regije text NOT NULL)")
    # with open("regije.sql") as f:
    #     skripta = f.read()
    #     c.executescript(skripta)
    
    
   
    
    # cur.execute("DROP TABLE IF EXISTS nepremicnine")
    # cur.execute("CREATE TABLE nepremicnine(id integer PRIMARY KEY AUTOINCREMENT, ime text NOT NULL)")
    # cur.execute("INSERT INTO nepremicnine(ime) VALUES('hiska')")
    # cur.execute("SELECT * from nepremicnine")
    # print(cur.fetchall())