DROP TABLE IF EXISTS nepremicnine;
DROP TABLE IF EXISTS agencije;
DROP TABLE IF EXISTS regije;
DROP TABLE IF EXISTS uporabnik;

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

CREATE TABLE uporabnik(
	id serial PRIMARY KEY,
	ime text NOT NULL,
	priimek text NOT NULL,
	uporabinsko_ime text NOT NULL,
	geslo text NOT NULL	
);

-- GRANT ALL ON DATABASE sem2020_domenfb TO sabrinac;
-- GRANT ALL ON DATABASE sem2020_domenfb TO timotejg;
-- GRANT ALL ON SCHEMA public TO sabrinac;
-- GRANT ALL ON ALL TABLES IN SCHEMA public TO andrazp;
-- GRANT ALL ON ALL SEQUENCES IN SCHEMA public TO andrazp;

-- GRANT SELECT ON ALL TABLES IN SCHEMA public TO javnost;
-- GRANT INSERT ON tabela TO javnost;
-- GRANT USAGE ON ALL SEQUENCES IN SCHEMA public TO javnost;
