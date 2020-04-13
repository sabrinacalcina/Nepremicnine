DROP TABLE IF EXISTS nepremicnine;
DROP TABLE IF EXISTS agencije;
DROP TABLE IF EXISTS regije;
DROP TABLE IF EXISTS uporabnik;

CREATE TABLE regije (
  id serial PRIMARY KEY,
  regije text NOT NULL
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
  zemljisce real,
  velikost real NOT NULL,
  cena real NOT NULL,
  agencija integer,
  regija integer
);

CREATE TABLE uporabnik(
	id serial PRIMARY KEY,
	ime text NOT NULL,
	priimek text NOT NULL,
	uporabinsko_ime text NOT NULL,
	geslo text NOT NULL	
);
