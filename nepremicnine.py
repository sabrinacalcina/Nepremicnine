import definicije
import bottle
from bottle import *
import sqlite3

# Tole nastavimo, da bomo videli sporočila o napakah
debug(True)

import hashlib



import psycopg2, psycopg2.extensions, psycopg2.extras
psycopg2.extensions.register_type(psycopg2.extensions.UNICODE) # se znebimo problemov s sumniki



@route("/")
def main():
    return template("views/zacetna_stran.html")



# poženemo strežnik na portu 8010, glej http://localhost:8080/
bottle.run(host='localhost', port=8080, reloader=True)



