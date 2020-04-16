import psycopg2, psycopg2.extensions, psycopg2.extras
psycopg2.extensions.register_type(psycopg2.extensions.UNICODE)

import csv

from auth import *

#UVOZ SQL SKRIPTE
def uvoziSQL(cur, datoteka):
    with open(datoteka) as f:
        skripta = f.read()
        cur.execute(skripta)

#UVOZ CSV-JA
def uvoziCSV(cur, tabela):
    with open('tabele/{0}.csv'.format(tabela), encoding='utf-8') as csvfile:
        podatki = csv.reader(csvfile)
        vsiPodatki = [vrstica for vrstica in podatki]
        glava = vsiPodatki[0]
        vrstice = vsiPodatki[1:]
        cur.executemany("INSERT INTO {0} ({1}) VALUES ({2})".format(
            tabela, ",".join(glava), ",".join(['%s']*len(glava))), vrstice)

# def uvoziCSV(cur, tabela):
#     with open('tabele/{0}.csv'.format(tabela), encoding='utf-8') as csvfile:
#         podatki = csv.reader(csvfile)
#         print('helooo')
#         print(podatki)
#         vsiPodatki = [vrstica for vrstica in podatki]
#         glava = vsiPodatki[0]
#         i = 0
#         for vrstica in podatki:
#             cur.execute("INSERT INTO {0} ({1}) VALUES ({2})".format(
#                 tabela, ",".join(glava), ",".join(['%s']*len(glava))), vrstica)
#             i += 1
#             print(i)


with psycopg2.connect(database=db, host=host, user=user, password=password) as con:
    cur = con.cursor()
    uvoziSQL(cur, 'tabele.sql')
    uvoziCSV(cur, 'regije')
    uvoziCSV(cur, 'agencije')
    uvoziCSV(cur, 'nepremicnine')
    con.commit()