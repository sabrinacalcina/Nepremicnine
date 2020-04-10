-- Nepremičnine:
CREATE TABLE nepremicnine (
  id serial PRIMARY KEY,
  ime text NOT NULL,
  vrsta text NOT NULL,
  opis text NOT NULL,
  leto integer,
  zemljisce integer,
  velikost integer NOT NULL,
  cena integer NOT NULL,
);

-- Regije:
CREATE TABLE regije (
  id serial PRIMARY KEY,
  ime text NOT NULL,
);

-- Agencije:
CREATE TABLE agencije (
  id serial PRIMARY KEY,
  ime text NOT NULL,
);

-- Uporabniki:
CREATE TABLE uporabnik(
	id serial PRIMARY KEY,
	ime text NOT NULL,
	priimek text NOT NULL,
	uporabinsko_ime text NOT NULL,
	geslo text NOT NULL	
);


