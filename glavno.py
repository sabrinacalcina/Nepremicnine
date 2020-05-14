import definicije
from bottle import *
import requests

# uvozimo ustrezne podatke za povezavo
import auth_public 
from auth_public import *

import psycopg2, psycopg2.extensions, psycopg2.extras
psycopg2.extensions.register_type(psycopg2.extensions.UNICODE) # se znebimo problemov s sumniki


# Mapa za statične vire (slike, css, ...)
static_dir = "./static"

# streženje statičnih datotek
@route("/static/<filename:path>")
def static(filename):
    return static_file(filename, root=static_dir)


@get('/')
def index():
    return template('zacetna_stran.html')
#=========================================================

@get('/zacetna_stran/')
def zacetna_get():  
    return redirect('/')
#=========================================================

@get('/nepremicnine/')
def nepremicnine_get(): 
    cur.execute("SELECT ime, vrsta, opis, leto_izgradnje, zemljisce, velikost, cena, agencija_id, regija_id FROM nepremicnine")
    return template('nepremicnine.html', nepremicnine=cur)
#=========================================================

@get('/agencije/')
def agencije_get():
    cur.execute("SELECT agencija FROM agencije")
    return template('agencije.html', agencije=cur)
#=========================================================

@get('/regije/')
def regije_get():
    cur.execute("SELECT regija FROM regije")
    return template('regije.html', regije=cur)
#=========================================================

@get('/registracija/')
def registracija_get():
    return template('registracija.html')
#=========================================================
def check(uime, geslo):
    return True

@get('/prijava/')
def prijava_get():
    return template('prijava.html')

@post('/prijava/')
def prijava_post():
    uime = request.forms.get('uime')
    geslo = request.forms.get('geslo')
    if check(uime, geslo):
        return template('uporabnik.html')

#=========================================================

# priklopimo se na bazo
baza = psycopg2.connect(database=db, host=host, user=user, password=password)
baza.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
cur = baza.cursor(cursor_factory=psycopg2.extras.DictCursor)

#=========================================================

run(host='localhost', port=8080, reloader=True)



