import psycopg2

# Connect to an existing database
conn = psycopg2.connect("dbname=gffa_db user=postgres password=postgres")

# Open a cursor to perform database operations
cur = conn.cursor()

# --------------- Query to create film table ---------------

sql = """CREATE TABLE IF NOT EXISTS public.film
(
    film_id integer NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1 ),
    url text NOT NULL,
    title text NOT NULL,
    episode_id integer NOT NULL,
    opening_crawl text,
    director text,
    producer text,
    release_date date,
    characters text[],
    planets text[],
    starships text[],
    vehicles text[],
    species text[],
    created TIMESTAMP NOT NULL,
    edited TIMESTAMP,
    raw_json json,
    PRIMARY KEY (film_id),
    UNIQUE (url)
);"""

# Execute to create film table
cur.execute(sql)

# --------------- Query to create person table ---------------

sql = """CREATE TABLE IF NOT EXISTS public.person
(
    person_id integer NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1 ),
    url text NOT NULL,
    name text NOT NULL,
    height integer,
    mass integer,
    hair_color text,
    skin_color text,
    eye_color text,
    birth_year text,
    gender text,
    homeworld text,
    films text[],
    species text[],
    vehicles text[],
    starships text[],
    created TIMESTAMP NOT NULL,
    edited TIMESTAMP,
    raw_json json,
    PRIMARY KEY (person_id),
    UNIQUE (url)
)"""

# Execute to create person table
cur.execute(sql)

# --------------- Query to create planet table ---------------

sql = """CREATE TABLE IF NOT EXISTS public.planet
(
    planet_id integer NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1 ),
    url text NOT NULL,
    name text NOT NULL,
    rotation_period integer,
    orbital_period integer,
    diameter integer,
    climate text,
    gravity text,
    terrain text,
    surface_water integer,
    population integer,
    residents text[],
    films text[],
    created TIMESTAMP NOT NULL,
    edited TIMESTAMP,
    raw_json json,
    PRIMARY KEY (planet_id),
    UNIQUE (url)
)"""

# Execute to create planet table
cur.execute(sql)

# --------------- Query to create species table ---------------

sql = """CREATE TABLE IF NOT EXISTS public.species
(
    species_id integer NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1 ),
    url text NOT NULL,
    name text NOT NULL,
    classification text,
    designation text,
    average_height integer,
    skin_colors text,
    hair_colors text,
    eye_colors text,
    average_lifespan integer,
    homeworld text,
    language text,
    people text[],
    films text[],
    created TIMESTAMP NOT NULL,
    edited TIMESTAMP,
    raw_json json,
    PRIMARY KEY (species_id),
    UNIQUE (url)
)"""

# Execute to create species table
cur.execute(sql)

# --------------- Query to create starship table ---------------

sql = """CREATE TABLE IF NOT EXISTS public.starship
(
    starship_id integer NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1 ),
    url text NOT NULL,
    name text NOT NULL,
    model text,
    manufacturer text,
    cost_in_credits integer,
    length float,
    max_atmosphering_speed integer,
    crew integer,
    passengers integer,
    cargo_capacity integer,
    consumables text,
    hyperdrive_rating float,
    mglt integer,
    starship_class text,
    pilots text[],
    films text[],
    created TIMESTAMP NOT NULL,
    edited TIMESTAMP,
    raw_json json,
    PRIMARY KEY (starship_id),
    UNIQUE (url)
)"""

# Execute to create starship table
cur.execute(sql)

# --------------- Query to create vehicle table ---------------

sql = """CREATE TABLE IF NOT EXISTS public.vehicle
(
    vehicle_id integer NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1 ),
    url text NOT NULL,
    name text NOT NULL,
    model text,
    manufacturer text,
    cost_in_credits integer,
    length float,
    max_atmosphering_speed integer,
    crew integer,
    passengers integer,
    cargo_capacity integer,
    consumables text,
    vehicle_class text,
    pilots text[],
    films text[],
    created TIMESTAMP NOT NULL,
    edited TIMESTAMP,
    raw_json json,
    PRIMARY KEY (vehicle_id),
    UNIQUE (url)
)"""

# Execute to create vehicle table
cur.execute(sql)

# Make the changes to the database persistent
conn.commit()

# Close cursor
cur.close()

# Close connection
conn.close()