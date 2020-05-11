DROP TABLE IF EXISTS priljubljene;
DROP TABLE IF EXISTS nepremicnine;
DROP TABLE IF EXISTS agencije;
DROP TABLE IF EXISTS regije;
DROP TABLE IF EXISTS uporabniki;

CREATE TABLE regije (
  id serial PRIMARY KEY,
  regija text NOT NULL
);

CREATE TABLE agencije (
  id serial PRIMARY KEY,
  agencija text NOT NULL
);

CREATE TABLE nepremicnine (
  id serial PRIMARY KEY,
  ime text NOT NULL,
  vrsta text NOT NULL,
  opis text NOT NULL,
  leto_izgradnje integer,
  zemljisce text, --tu more bit real
  velikost real NOT NULL,
  cena real NOT NULL,
  agencija integer REFERENCES agencije(id),
  regija integer REFERENCES regije(id)
);

CREATE TABLE uporabniki(
	id serial PRIMARY KEY,
	ime text NOT NULL,
	priimek text NOT NULL,
  email text NOT NULL UNIQUE,
	uporabnisko_ime text NOT NULL UNIQUE,
	geslo text NOT NULL
  --CONSTRAINT blabla UNIQUE(kire stolpce)  lahko tudi tak delas
);

CREATE TABLE priljubljene(
  uporabnik integer REFERENCES uporabniki(id),
  nepremicnina integer REFERENCES nepremicnine(id)
);

GRANT ALL ON DATABASE sem2020_domenfb TO sabrinac;
GRANT ALL ON SCHEMA public TO sabrinac;
GRANT ALL ON ALL TABLES IN SCHEMA public TO sabrinac;
GRANT ALL ON ALL SEQUENCES IN SCHEMA public TO sabrinac;

GRANT ALL ON DATABASE sem2020_domenfb TO timotejg;
GRANT ALL ON SCHEMA public TO timotejg;
GRANT ALL ON ALL TABLES IN SCHEMA public TO timotejg;
GRANT ALL ON ALL SEQUENCES IN SCHEMA public TO timotejg;

GRANT ALL ON DATABASE sem2020_domenfb TO javnost;
GRANT ALL ON SCHEMA public TO javnost;
GRANT ALL ON ALL TABLES IN SCHEMA public TO javnost;
GRANT ALL ON ALL SEQUENCES IN SCHEMA public TO javnost;