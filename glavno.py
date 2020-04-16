import definicije
from bottle import *
import requests

import psycopg2, psycopg2.extensions, psycopg2.extras
psycopg2.extensions.register_type(psycopg2.extensions.UNICODE) # se znebimo problemov s sumniki

@get('/')
def index():
    return template('zacetna_stran.html')
#=========================================================

@get('/nepremicnine/')
def nepremicnine_get():   
    return template('nepremicnine.html')
#=========================================================

@get('/zacetna_stran/')
def zacetna_get():   
    return template('zacetna_stran.html')
#=========================================================

@get('/agencije/')
def agencije_get():
    return template('agencije.html')
#=========================================================

@get('/regije/')
def regije_get():
    return template('regije.html')
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

@route("/static/<filename:path>")
def static(filename):
    """Splošna funkcija, ki servira vse statične datoteke iz naslova
       /static/..."""
    static_dir = 'static'
    return static_file(filename, root=static_dir)

run(host='localhost', port=8080, reloader=True)



