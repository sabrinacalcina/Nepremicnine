import definicije
import bottle
from bottle import route, run, Response, template

app = bottle.default_app()

@route('/')
def index():
    return bottle.template('zacetna_stran.html')






bottle.run(reloader=True, debug=True)


