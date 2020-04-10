import definicije
import bottle
from bottle import route, run, Response, template

app = bottle.default_app()

@route('/')
def index():
    return bottle.template('spletne_strani\zacetna_stran.html')


bottle.run(host='localhost', port=8080)



