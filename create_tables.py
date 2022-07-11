import psycopg2
import secrets

# Connect to an existing database
conn = psycopg2.connect(f"dbname=gffa_db user={secrets.USERNAME} password={secrets.PASSWORD}")

# Open a cursor to perform database operations
cur = conn.cursor()

# --------------- Query to create film table ---------------

sql = """CREATE TABLE IF NOT EXISTS public.film
(
    film_id integer NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1 ),
    title text NOT NULL,
    description text,
    attributes jsonb,
    attributes_orig jsonb,
    date_created TIMESTAMP NOT NULL,
    date_modified TIMESTAMP,
    PRIMARY KEY (film_id),
    UNIQUE (title)
)"""

# Execute to create film table
cur.execute(sql)

# --------------- Query to create planet table ---------------

sql = """CREATE TABLE IF NOT EXISTS public.planet
(
    planet_id integer NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1 ),
    name text NOT NULL,
    description text,
    attributes jsonb,
    attributes_orig jsonb,
    date_created TIMESTAMP NOT NULL,
    date_modified TIMESTAMP,
    PRIMARY KEY (planet_id),
    UNIQUE (name)
)"""

# Execute to create planet table
cur.execute(sql)

# --------------- Query to create language table ---------------

sql = """CREATE TABLE IF NOT EXISTS public.language
(
    language_id integer NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1 ),
    name text NOT NULL,
    description text,
    attributes jsonb,
    attributes_orig jsonb,
    date_created TIMESTAMP NOT NULL,
    date_modified TIMESTAMP,
    PRIMARY KEY (language_id),
    UNIQUE (name)
)"""

# Execute to create language table
cur.execute(sql)

# --------------- Query to create sentient_being_type table ---------------

sql = """CREATE TABLE IF NOT EXISTS public.sentient_being_type
(
    sentient_being_type_id integer NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1 ),
    name text NOT NULL,
    language_id integer NOT NULL,
    description text,
    attributes jsonb,
    attributes_orig jsonb,
    date_created TIMESTAMP NOT NULL,
    date_modified TIMESTAMP,
    PRIMARY KEY (sentient_being_type_id),
    FOREIGN KEY (language_id) REFERENCES public.language(language_id),
    UNIQUE (name)
)"""

# Execute to create sentient_being_type table
cur.execute(sql)

# --------------- Query to create sentient_being table ---------------

sql = """CREATE TABLE IF NOT EXISTS public.sentient_being
(
    sentient_being_id integer NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1 ),
    sentient_being_type_id int NOT NULL,
    home_world_id int NOT NULL,
    name_first text NOT NULL,
    name_last text,
    description text,
    attributes jsonb,
    attributes_orig jsonb,
    date_created TIMESTAMP NOT NULL,
    date_modified TIMESTAMP,
    PRIMARY KEY (sentient_being_id),
    FOREIGN KEY (sentient_being_type_id) REFERENCES public.sentient_being_type(sentient_being_type_id),
    FOREIGN KEY (home_world_id) REFERENCES public.planet(planet_id),
    UNIQUE (name_first, name_last)
)"""

# Execute to create sentient_being table
cur.execute(sql)

# --------------- Query to create crew_role table ---------------

sql = """CREATE TABLE IF NOT EXISTS public.crew_role
(
    crew_role_id integer NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1 ),
    name text NOT NULL,
    description text,
    attributes jsonb,
    attributes_orig jsonb,
    date_created TIMESTAMP NOT NULL,
    date_modified TIMESTAMP,
    PRIMARY KEY (crew_role_id),
    UNIQUE (name)
)"""

# Execute to create crew_role table
cur.execute(sql)

# --------------- Query to create vehicle_type table ---------------

sql = """CREATE TABLE IF NOT EXISTS public.vehicle_type
(
    vehicle_type_id integer NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1 ),
    name text NOT NULL,
    description text,
    attributes jsonb,
    attributes_orig jsonb,
    date_created TIMESTAMP NOT NULL,
    date_modified TIMESTAMP,
    PRIMARY KEY (vehicle_type_id),
    UNIQUE (name)
)"""

# Execute to create vehicle_type table
cur.execute(sql)

# --------------- Query to create vehicle_class table ---------------

sql = """CREATE TABLE IF NOT EXISTS public.vehicle_class
(
    vehicle_class_id integer NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1 ),
	vehicle_type_id int,
    name text NOT NULL,
    description text,
    attributes jsonb,
    attributes_orig jsonb,
    date_created TIMESTAMP NOT NULL,
    date_modified TIMESTAMP,
	PRIMARY KEY (vehicle_class_id),
    FOREIGN KEY (vehicle_type_id) REFERENCES public.vehicle_type(vehicle_type_id),
    UNIQUE (name)
)"""

# Execute to create vehicle_class table
cur.execute(sql)

# --------------- Query to create vehicle table ---------------

sql = """CREATE TABLE IF NOT EXISTS public.vehicle
(
    vehicle_id integer NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1 ),
	vehicle_class_id integer NOT NULL,
    model text,
    description text,
    attributes jsonb,
    attributes_orig jsonb,
    date_created TIMESTAMP NOT NULL,
    date_modified TIMESTAMP,
	PRIMARY KEY (vehicle_id),
    FOREIGN KEY (vehicle_class_id) REFERENCES public.vehicle_class(vehicle_class_id),
    UNIQUE (model)
)"""

# Execute to create vehicle table
cur.execute(sql)

# --------------- Query to create vehicle_crew table ---------------

sql = """CREATE TABLE IF NOT EXISTS public.vehicle_crew
(
    vehicle_crew_id integer NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1 ),
	vehicle_id integer NOT NULL,
	sentient_being_id integer NOT NULL,
    crew_role_id integer NOT NULL,
	PRIMARY KEY (vehicle_crew_id),
    FOREIGN KEY (vehicle_id) REFERENCES public.vehicle(vehicle_id),
    FOREIGN KEY (sentient_being_id) REFERENCES public.sentient_being(sentient_being_id),
    FOREIGN KEY (crew_role_id) REFERENCES public.crew_role(crew_role_id)
)"""

# Execute to create vehicle_crew table
cur.execute(sql)

# --------------- Query to create vehicle_passenger table ---------------

sql = """CREATE TABLE IF NOT EXISTS public.vehicle_passenger
(
    vehicle_passenger_id integer NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1 ),
	vehicle_id integer NOT NULL,
	sentient_being_id integer NOT NULL,
    PRIMARY KEY (vehicle_passenger_id),
    FOREIGN KEY (vehicle_id) REFERENCES public.vehicle(vehicle_id),
    FOREIGN KEY (sentient_being_id) REFERENCES public.sentient_being(sentient_being_id)
)"""

# Execute to create vehicle_passenger table
cur.execute(sql)

# --------------- Query to create film_character table ---------------

sql = """CREATE TABLE IF NOT EXISTS public.film_character
(
    film_character_id integer NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1 ),
    film_id integer NOT NULL,
    sentient_being_id integer NOT NULL,
    PRIMARY KEY (film_character_id),
    FOREIGN KEY (film_id) REFERENCES public.film(film_id),
    FOREIGN KEY (sentient_being_id) REFERENCES public.sentient_being(sentient_being_id)
)"""

# Execute to create film_character table
cur.execute(sql)

# --------------- Query to create film_vehicle table ---------------

sql = """CREATE TABLE IF NOT EXISTS public.film_vehicle
(
    film_vehicle_id integer NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1 ),
    film_id integer NOT NULL,
    vehicle_id integer NOT NULL,
    PRIMARY KEY (film_vehicle_id),
    FOREIGN KEY (film_id) REFERENCES public.film(film_id),
    FOREIGN KEY (vehicle_id) REFERENCES public.vehicle(vehicle_id)
)"""

# Execute to create film_vehicle table
cur.execute(sql)

# --------------- Query to create film_planet table ---------------

sql = """CREATE TABLE IF NOT EXISTS public.film_planet
(
    film_planet_id integer NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1 ),
    film_id integer NOT NULL,
    planet_id integer NOT NULL,
    PRIMARY KEY (film_planet_id),
    FOREIGN KEY (film_id) REFERENCES public.film(film_id),
    FOREIGN KEY (planet_id) REFERENCES public.planet(planet_id)
)"""

# Execute to create film_planet table
cur.execute(sql)

# Make the changes to the database persistent
conn.commit()

# Close cursor
cur.close()

# Close connection
conn.close()