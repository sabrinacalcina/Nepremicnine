import definicije
from bottle import *

import psycopg2, psycopg2.extensions, psycopg2.extras
psycopg2.extensions.register_type(psycopg2.extensions.UNICODE) # se znebimo problemov s sumniki

@route('/')
def index():
    return template('views\zacetna_stran.html')



run(host='localhost', port=8080, reloader=True)



