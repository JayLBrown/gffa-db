import requests
import json
import psycopg2
import datetime
import gffa_utils

# --------------------------------------------- READ ALL DATA ---------------------------------------------
film_data = gffa_utils.read_json('./data/swapi_json/swapi_films.json')
planet_data = gffa_utils.read_json('./data/swapi_json/swapi_planets.json')
species_data = gffa_utils.read_json('./data/swapi_json/swapi_species.json')

# --------------------------------------------- GFFA FILM ---------------------------------------------
# --------------- CONVERT FILM DATA ---------------

def convert_film_data(film):
    unknowns = ('n/a', 'none', 'unknown')
    list_keys = ('producer')
    for key, val in film.items():
        if val in unknowns:
                film[key] = gffa_utils.convert_to_none(val)
        elif key in list_keys:
            film[key] = gffa_utils.convert_to_list(val, ', ')
    return film

# --------------- PREPARE FILM LIST ---------------

def prepare_film_list(film):
    film_list = []
    film_list.append(film["title"])
    film_list.append("description")
    film_attr = dict((k, film[k]) for k in ['episode_id', 'opening_crawl', 'director', 'producer', 'release_date', 'characters', 'planets', 'starships', 'vehicles', 'species'])
    film_list.append(json.dumps(film_attr, sort_keys=False))
    film_list.append(datetime.datetime.now())
    film_list.append(datetime.datetime.now())
    return film_list

# --------------------------------------------- GFFA PLANET ---------------------------------------------
# --------------- CONVERT PLANET DATA ---------------

def convert_planet_data(planet):
    unknowns = ('n/a', 'none', 'unknown')
    int_keys = ('rotation_period', 'orbital_period', 'population')
    float_keys = ('diameter', 'surface_water')
    list_keys = ('producer', 'terrain')
    for key, val in planet.items():
        if val in unknowns:
                planet[key] = gffa_utils.convert_to_none(val)
        elif key in int_keys:
                    planet[key] = gffa_utils.convert_to_int(val)
        elif key in float_keys:
            planet[key] = gffa_utils.convert_to_float(val)
        elif key in list_keys:
            planet[key] = gffa_utils.convert_to_list(val, ', ')
    return planet

# --------------- PREPARE PLANET LIST ---------------

def prepare_planet_list(planet):
    planet_list = []
    planet_list.append(planet["name"])
    planet_attr = dict((k, planet[k]) for k in ['rotation_period', 'orbital_period', 'diameter', 'climate', 'gravity', 'terrain', 'surface_water', 'population', 'residents', 'films'])
    planet_list.append(json.dumps(planet_attr))
    planet_list.append(datetime.datetime.now())
    planet_list.append(datetime.datetime.now())
    return planet_list

# --------------- PREPARE LANGUAGE LIST ---------------

def prepare_language_list(species):
    language_list = []
    language_list.append(species["language"])
    language_list.append("description")
    # language_list.append("attributes")
    language_list.append(datetime.datetime.now())
    language_list.append(datetime.datetime.now())
    return language_list

# --------------- REMOVE DUPLICATES LANGUAGE LIST ---------------

# def refine_language_list(languages):
#     result = []
#     for language in languages:
#         if language.get('name') not in result:
#             result.append(language.get('name'))

def main():

    # Connect to an existing database
    conn = psycopg2.connect("dbname=gffa_db user=postgres password=postgres")

    # Open a cursor to perform database operations
    cur = conn.cursor()

    # --------------- INSERT INTO FILM TABLE ---------------
    
    for film in film_data:
        film_list = prepare_film_list(convert_film_data(film))
        sql = """INSERT INTO public.film(title, description, attributes, date_created, date_modified) VALUES (%s, %s, %s, %s, %s) ON CONFLICT (film_id) DO NOTHING"""
        # Execute to insert records into film table
        cur.execute(sql, film_list)
        # Make the changes to the database persistent
        conn.commit()
    
    # --------------- INSERT INTO PLANET TABLE ---------------

    for planet in planet_data:
        if planet["name"] != "unknown":
            planet_list = prepare_planet_list(convert_planet_data(planet))
            sql = """INSERT INTO public.planet(name, attributes, date_created, date_modified) VALUES (%s, %s, %s, %s) ON CONFLICT (planet_id) DO NOTHING"""
            # Execute to insert records into planet table
            cur.execute(sql, planet_list)
            # Make the changes to the database persistent
            conn.commit()

    # --------------- INSERT INTO LANGUAGE TABLE ---------------

    for species in species_data:
        language_list = prepare_language_list(species)
        sql = """INSERT INTO public.language(name, description, date_created, date_modified) VALUES (%s, %s, %s, %s) ON CONFLICT (language_id) DO NOTHING"""
        # Execute to insert records into language table
        cur.execute(sql, language_list)
        # Make the changes to the database persistent
        conn.commit()

    # Close cursor
    cur.close()

    # Close connection
    conn.close()

if __name__ == '__main__':
    main()