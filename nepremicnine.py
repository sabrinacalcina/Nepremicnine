import definicije
import bottle
from bottle import *

import psycopg2, psycopg2.extensions, psycopg2.extras
psycopg2.extensions.register_type(psycopg2.extensions.UNICODE) # se znebimo problemov s sumniki

#za sporocila o napakah
debug(True)

app = bottle.default_app()

@route('/')
def index():
    return bottle.template('spletne_strani\zacetna_stran.html')



bottle.run(host='localhost', port=8080, reloader=True)



