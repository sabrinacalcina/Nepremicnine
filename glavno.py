import definicije
from bottle import *
import requests
import hashlib


# uvozimo ustrezne podatke za povezavo
import auth_public 
from auth_public import *

import psycopg2, psycopg2.extensions, psycopg2.extras
psycopg2.extensions.register_type(psycopg2.extensions.UNICODE) # se znebimo problemov s sumniki


import os

# privzete nastavitve
SERVER_PORT = os.environ.get('BOTTLE_PORT', 8080)
RELOADER = os.environ.get('BOTTLE_RELOADER', True)
ROOT = os.environ.get('BOTTLE_ROOT', '/')
DB_PORT = os.environ.get('POSTGRES_PORT', 5432)


def rtemplate(*largs, **kwargs):
    """
    Izpis predloge s podajanjem spremenljivke ROOT z osnovnim URL-jem.
    """
    return template(ROOT=ROOT, *largs, **kwargs)


kodiranje = 'laqwXUtKfHTp1SSpnkSg7VbsJtCgYS89QnvE7PedkXqbE8pPj7VeRUwqdXu1Fr1kEkMzZQAaBR93PoGWks11alfe8y3CPSKh3mEQ'

#funkcija za piškotke
def id_uporabnik():
    if request.get_cookie("id", secret = kodiranje):
        piskotek = request.get_cookie("id", secret = kodiranje)
        return piskotek
    else:
        return 0


# Mapa za statične vire (slike, css, ...)
static_dir = "./static"

# streženje statičnih datotek
@route("/static/<filename:path>")
def static(filename):
    return static_file(filename, root=static_dir)


@get('/')
def index():
    stanje = id_uporabnik()
    return rtemplate('zacetna_stran.html', stanje = stanje)
#=========================================================

@get('/zacetna_stran/')
def zacetna_get():  
    return redirect('/')

#=========================================================

@get('/nepremicnine/')
def nepremicnine_get(): 
    stanje = id_uporabnik()
    cur.execute("SELECT ime, vrsta, opis, leto_izgradnje, zemljisce, velikost, cena, agencija_id, regija_id FROM nepremicnine")
    podatki = cur.fetchall()
    return rtemplate('nepremicnine.html', nepremicnine=podatki, stanje = stanje)

#=========================================================

@get('/agencije/')
def agencije_get():
    stanje = id_uporabnik()
    cur.execute("SELECT * FROM agencije")
    podatki = cur.fetchall()
    return rtemplate('agencije.html', agencije=podatki, stanje = stanje)

#=========================================================

@get('/agencije/<oznaka>')
def agencije(oznaka):
    stanje = id_uporabnik()
    ukaz = ("SELECT ime, vrsta, opis, leto_izgradnje, zemljisce, velikost, cena, regija_id FROM nepremicnine WHERE agencija_id = (%s)")
    cur.execute(ukaz,(oznaka, ))
    cura = cur.fetchall()
    return rtemplate('agencije_klik.html', nepremicnine=cura, oznaka=oznaka, stanje = stanje)


#=========================================================

@get('/regije/')
def regije_get():
    stanje = id_uporabnik()
    cur.execute("SELECT * FROM regije")
    cura = cur.fethcall()
    return rtemplate('regije.html', regije=cura, stanje = stanje)

#=========================================================

@get('/regije/<oznaka>')
def regije(oznaka):
    stanje = id_uporabnik()
    ukaz = ("SELECT ime, vrsta, opis, leto_izgradnje, zemljisce, velikost, cena, agencija_id FROM nepremicnine WHERE regija_id = (%s)")
    cur.execute(ukaz,(oznaka, ))
    cura = cur.fetchall()
    return rtemplate('regije_klik.html', nepremicnine=cura, oznaka=oznaka, stanje = stanje)

#=========================================================
#REGISTRACIJA

#@get('/registracija/')
#def registracija_get():
#    return rtemplate('registracija.html')

@get('/registracija/')
def register():
    print(1)
    stanje = id_uporabnik()
    if stanje !=0:
        print(2)
        redirect('{0}zacetna_stran/'.format(ROOT))
    polja_registracija = ("ime", "priimek", "email", "psw", "psw2", "uporabnisko_ime")
    podatki = {polje: "" for polje in polja_registracija}
    print(3)    
    return rtemplate('registracija.html', stanje=stanje, napaka=0, **podatki)


@post('/registracija/')
def registracija():
    stanje = id_uporabnik()
    print(4)
    polja_registracija = ("ime", "priimek", "email", "uporabnisko_ime", "psw", "psw2")
    podatki = {polje: "" for polje in polja_registracija}
    podatki = {polje: getattr(request.forms, polje) for polje in polja_registracija}

    ime = podatki.get('ime')
    priimek = podatki.get('priimek')
    email = podatki.get('email')
    uporabnisko_ime = podatki.get('uporabnisko_ime')
    geslo1 = podatki.get('psw')
    geslo2 = podatki.get('psw2')


    if ime == '' or priimek == '' or email == '' or uporabnisko_ime == '' or geslo1 == '' or geslo2 == '':
        print(5)
        return rtemplate('registracija.html', stanje= stanje, napaka = 1, **podatki)

    if len(geslo1) < 4:
        print(6)
        return rtemplate('registracija.html', stanje = stanje, napaka =5, **podatki)

    if str(geslo1) == str(geslo2):
        print(7)
        podatki["geslo"] = hashGesla(podatki["psw"])
        ukaz = """INSERT INTO uporabniki (ime,priimek,email,uporabnisko_ime,geslo)
                  VALUES((%(ime)s), (%(priimek)s), (%(email)s),(%(uporabnisko_ime)s),(%(geslo)s)) returning id
                  """
        cur.execute(ukaz, podatki)
        uid = cur.fetchone()[0]
        response.set_cookie("id",uid, path='/', secret = kodiranje)
        string = '{0}uporabnik/{1}/'.format(ROOT,uid)
        redirect(string)
        
    else:
        print(8)
        return rtemplate('registracija.html', stanje = stanje, napaka = 4, **podatki)

#=========================================================
#PRIJAVA

def check(uime, geslo):
    cur.execute('select geslo from uporabniki where uporabnisko_ime = (%s)',(uime, ))
    try:
        podatek = cur.fetchone()[0]
        if podatek == geslo:
            return True
        return False
    except:
        return False

@get('/prijava/')
def prijava_get():
    stanje = id_uporabnik()
    if stanje != 0:
        redirect('{0}zacetna_stran/'.format(ROOT))
    return rtemplate('prijava.html', stanje = stanje)

@post('/prijava/')
def prijava_post():
    uime = request.forms.get('uime')
    geslo = request.forms.get('geslo')
    if preveri_uporabnika(uime, geslo):
        ukaz = 'SELECT id FROM uporabniki WHERE uporabnisko_ime = (%s)'
        cur.execute(ukaz, (uime, ))
        podatek = cur.fetchone()[0]
        response.set_cookie("id",podatek, path='/', secret = kodiranje)
        redirect('{0}uporabnik/{1}/'.format(ROOT, podatek))
    else:
        redirect('{0}prijava/'.format(ROOT))


#=========================================================
#HASH GESLO

def preveri_uporabnika(ime,geslo):
    ukaz = ("SELECT geslo FROM uporabniki WHERE uporabnisko_ime = (%s)")
    cur.execute(ukaz,(ime, ))
    for psw in cur:
        if psw[0] == hashGesla(geslo):
            return True
        else:
            return False
            

def hashGesla(s):
    m = hashlib.sha256()
    m.update(s.encode("utf-8"))
    return m.hexdigest()


#=========================================================
#POZNA UPORABNIKA

@get('/uporabnik/<stanje>/')
def uporabnik(stanje):
    ukaz = 'SELECT ime, priimek FROM uporabniki WHERE id = (%s)'
    cur.execute(ukaz, (stanje, ))
    podatki = cur.fetchone()
    ime = podatki[0]
    priimek = podatki[1]
    return rtemplate('uporabnik.html', ime = ime, priimek = priimek, stanje = stanje)

#=========================================================
#ODJAVA

@get('/odjava/')
def odjava():
    response.delete_cookie("id", path='/')
    redirect('{0}zacetna_stran/'.format(ROOT))    

#=========================================================

# priklopimo se na bazo
baza = psycopg2.connect(database=db, host=host, user=user, password=password, port = DB_PORT)
baza.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
cur = baza.cursor(cursor_factory=psycopg2.extras.DictCursor)

#=========================================================

run(host='localhost', port=SERVER_PORT, reloader=RELOADER)



