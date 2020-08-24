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
        print(piskotek)
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
    cur.execute("SELECT id, ime, vrsta, opis, leto_izgradnje, zemljisce, velikost, cena, agencija_id, regija_id FROM nepremicnine")
    podatki = cur.fetchall()
    return rtemplate('nepremicnine.html', nepremicnine=podatki, stanje = stanje)

#=========================================================

@get('/dodaj_nepremicnine/')
def dodaj_nepremicnine(): 
    stanje = id_uporabnik()
    print(stanje)
    cur.execute("SELECT ime, vrsta, opis, leto_izgradnje, zemljisce, velikost, cena, agencija_id, regija_id FROM nepremicnine")
    podatki = cur.fetchall()
    return rtemplate('dodaj_nepremicnine.html', nepremicnine=podatki, stanje = stanje)

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
    cura = cur.fetchall()
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

@get('/priljubljene/')
def priljubljene():
    stanje = id_uporabnik()
    cur.execute("select ime, vrsta, opis, leto_izgradnje, zemljisce, velikost, cena, agencija_id, regija_id from ( nepremicnine join priljubljene on id = nepremicnina) where uporabnik = (%s)", (stanje, ))
    cura = cur.fetchall()

    ukaz = 'SELECT ime, priimek FROM uporabniki WHERE id = (%s)'
    cur.execute(ukaz, (stanje, ))
    podatki = cur.fetchone()
    ime = podatki[0]
    priimek = podatki[1]
    return rtemplate('priljubljene.html', nepremicnine=cura, ime = ime, priimek = priimek, stanje = stanje)

#=========================================================
#REGISTRACIJA

@get('/registracija/')
def register():
    stanje = id_uporabnik()
    if stanje !=0:
        redirect('{0}zacetna_stran/'.format(ROOT))
    polja_registracija = ("ime", "priimek", "email", "psw", "psw2", "uporabnisko_ime")
    podatki = {polje: "" for polje in polja_registracija} 
    napaka = 0
    return rtemplate('registracija.html', stanje=stanje, napaka=napaka, **podatki)


@post('/registracija/')
def registracija():
    stanje = id_uporabnik()
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
        return rtemplate('registracija.html', stanje= stanje, napaka = 1, **podatki)

    ukaz = """SELECT * FROM uporabniki WHERE email = (%s)"""
    cur.execute(ukaz, (email, ))
    podatek = cur.fetchone()
    if podatek != None:
        return rtemplate('registracija.html', stanje = stanje, napaka = 2, **podatki)

    if len(geslo1) < 4:
        return rtemplate('registracija.html', stanje = stanje, napaka = 4, **podatki)

    if str(geslo1) == str(geslo2):
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
        return rtemplate('registracija.html', stanje = stanje, napaka = 3, **podatki)

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
    return rtemplate('prijava.html', napaka=0, stanje = stanje)

@post('/prijava/')
def prijava_post():
    stanje = id_uporabnik()
    uime = request.forms.get('uime')
    geslo = request.forms.get('geslo')
    if preveri_uporabnika(uime, geslo):
        ukaz = 'SELECT id FROM uporabniki WHERE uporabnisko_ime = (%s)'
        cur.execute(ukaz, (uime, ))
        podatek = cur.fetchone()[0]
        response.set_cookie("id",podatek, path='/', secret = kodiranje)
        redirect('{0}uporabnik/{1}/'.format(ROOT, podatek))
    else:
        return rtemplate('prijava.html', napaka=1, stanje = stanje)


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
    if int(stanje) != id_uporabnik():
        redirect("{0}".format(ROOT))

    ukaz = 'SELECT ime, priimek FROM uporabniki WHERE id = (%s)'
    cur.execute(ukaz, (stanje, ))
    podatki = cur.fetchone()
    ime = podatki[0]
    priimek = podatki[1]
    return rtemplate('uporabnik.html', ime = ime, priimek = priimek, stanje = stanje)
#=========================================================
#Gumb dodaj v tabeli nepremičnine te preusmeri na stran potrditev

@get('/nepremicnine/<oznaka>')
def nepremicnina(oznaka):
    stanje = id_uporabnik()
    cur.execute('select ime, vrsta, opis, leto_izgradnje, zemljisce, velikost, cena, agencija_id, regija_id from nepremicnine where id = (%s)', (oznaka, ))
    podatki = cur.fetchall()
    return rtemplate('potrditev.html', stanje = stanje, podatki = podatki, id=oznaka)

@post('/nepremicnine/<oznaka>')
def potrditev(oznaka):
    stanje = id_uporabnik()
    cur.execute('select * from priljubljene where uporabnik = (%s) and nepremicnina = (%s)',(stanje, oznaka, ))
    podatki = cur.fetchall()
    if podatki == []:
        cur.execute('insert into priljubljene(uporabnik, nepremicnina) values ((%s), (%s))', (stanje, oznaka, ))
        redirect('{0}nepremicnine/'.format(ROOT))
    else:
        redirect('{0}priljubljene/'.format(ROOT))
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



