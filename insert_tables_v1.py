import requests
import json
import psycopg2
import datetime
import gffa_utils

# --------------------------------------------- READ ALL DATA ---------------------------------------------
film_data = gffa_utils.read_json('./data/swapi_json/swapi_films.json')
planet_data = gffa_utils.read_json('./data/swapi_json/swapi_planets.json')
species_data = gffa_utils.read_json('./data/swapi_json/swapi_species.json')
people_data = gffa_utils.read_json('./data/swapi_json/swapi_people.json')
starship_data = gffa_utils.read_json('./data/swapi_json/swapi_starships.json')
vehicle_data = gffa_utils.read_json('./data/swapi_json/swapi_vehicles.json')

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
    film_list.append(json.dumps(film_attr))
    film_list.append(json.dumps(film))
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
    planet_list.append("description")
    planet_attr = dict((k, planet[k]) for k in ['rotation_period', 'orbital_period', 'diameter', 'climate', 'gravity', 'terrain', 'surface_water', 'population', 'residents', 'films'])
    planet_list.append(json.dumps(planet_attr))
    planet_list.append(json.dumps(planet))
    planet_list.append(datetime.datetime.now())
    planet_list.append(datetime.datetime.now())
    return planet_list

# --------------------------------------------- GFFA SPECIES ---------------------------------------------
# --------------- EXTRACT UNIQUUE LANGUAGE DATA ---------------

def extract_language_list(species_data):
    unknowns = ('n/a', 'none', 'unknown')
    result = []
    for species in species_data:
        if species["language"].lower() not in unknowns and species["language"].lower() not in result:
            result.append(species["language"].lower())
    return result

# --------------- CONVERT SENTIENT_BEING_TYPE DATA ---------------

def convert_sentient_being_type_data(sentient_being_type):
    unknowns = ('n/a', 'none', 'unknown')
    int_keys = ('average_lifespan')
    float_keys = ('average_height')
    list_keys = ('skin_colors', 'hair_colors', 'eye_colors', 'people', 'films')
    for key, val in sentient_being_type.items():
        if val in unknowns:
            sentient_being_type[key] = gffa_utils.convert_to_none(val)
        elif key in int_keys:
            sentient_being_type[key] = gffa_utils.convert_to_int(val)
        elif key in float_keys:
            sentient_being_type[key] = gffa_utils.convert_to_float(val)
        elif key in list_keys:
            sentient_being_type[key] = gffa_utils.convert_to_list(val, ', ')
    return sentient_being_type

# --------------- PREPARE SENTIENT_BEING_TYPE LIST ---------------

def prepare_sentient_being_type_list(sentient_being_type):
    sentient_being_type_list = []
    sentient_being_type_list.append(sentient_being_type["name"])
    sentient_being_type_list.append(1)
    sentient_being_type_list.append("description")
    sentient_being_type_attr = dict((k, sentient_being_type[k]) for k in ['classification', 'designation', 'average_height', 'skin_colors', 'hair_colors', 'eye_colors', 'average_lifespan', 'homeworld', 'language', 'people', 'films'])
    sentient_being_type_list.append(json.dumps(sentient_being_type_attr))
    sentient_being_type_list.append(json.dumps(sentient_being_type))
    sentient_being_type_list.append(datetime.datetime.now())
    sentient_being_type_list.append(datetime.datetime.now())
    print(sentient_being_type_list)
    return sentient_being_type_list

# --------------------------------------------- GFFA VEHICLE ---------------------------------------------
# --------------- EXTRACT UNIQUUE VEHICLE_CLASS DATA ---------------

def extract_vehicle_class_list(vehicle_data):
    unknowns = ('n/a', 'none', 'unknown')
    result = []
    for vehicle in vehicle_data:
        if vehicle["vehicle_class"].lower() not in unknowns and vehicle["vehicle_class"].lower() not in result:
            result.append(vehicle["vehicle_class"].lower())
    return result

def main():

    # Connect to an existing database
    conn = psycopg2.connect("dbname=gffa_db user=postgres password=postgres")

    # Open a cursor to perform database operations
    cur = conn.cursor()

    # --------------- INSERT INTO FILM TABLE ---------------
    
    for film in film_data:
        film_list = prepare_film_list(convert_film_data(film))
        sql = """INSERT INTO public.film(title, description, attributes, attributes_orig, date_created, date_modified) VALUES (%s, %s, %s, %s, %s, %s) ON CONFLICT (film_id) DO NOTHING"""
        # Execute to insert records into film table
        cur.execute(sql, film_list)
        # Make the changes to the database persistent
        conn.commit()
    
    # --------------- INSERT INTO PLANET TABLE ---------------

    for planet in planet_data:
        if planet["name"] != "unknown":
            planet_list = prepare_planet_list(convert_planet_data(planet))
            sql = """INSERT INTO public.planet(name, description, attributes, attributes_orig, date_created, date_modified) VALUES (%s, %s, %s, %s, %s, %s) ON CONFLICT (planet_id) DO NOTHING"""
            # Execute to insert records into planet table
            cur.execute(sql, planet_list)
            # Make the changes to the database persistent
            conn.commit()
    
    # --------------- INSERT INTO LANGUAGE TABLE ---------------
    
    language_list = extract_language_list(species_data)
    for lang in language_list:
        sql = """INSERT INTO public.language(name, date_created, date_modified) VALUES (%s, %s, %s) ON CONFLICT (language_id) DO NOTHING"""
        # Execute to insert records into language table
        cur.execute(sql, (lang, datetime.datetime.now(), datetime.datetime.now()))
        # Make the changes to the database persistent
        conn.commit()
    
    # --------------- INSERT AND UPDATE INTO SENTIENT_BEING_TYPE TABLE ---------------
    
    for species in species_data:
        sentient_being_type_list = prepare_sentient_being_type_list(convert_sentient_being_type_data(species))
        sql = """INSERT INTO public.sentient_being_type(name, language_id, description, attributes, attributes_orig, date_created, date_modified) VALUES (%s, %s, %s, %s, %s, %s, %s) ON CONFLICT (sentient_being_type_id) DO NOTHING"""
        # Execute to insert records into sentient_being_type table
        cur.execute(sql, sentient_being_type_list)
        sql = """UPDATE sentient_being_type SET language_id=public.language.language_id from public.language WHERE public.sentient_being_type.name=%s and public.language.name=%s"""
        # # Execute to insert records into sentient_being_type table
        cur.execute(sql, (species["name"], species["language"]))
        # # Make the changes to the database persistent
        conn.commit()
    
    # --------------- INSERT INTO VEHICLE_CLASS TABLE ---------------

    vehicle_class_list = extract_vehicle_class_list(vehicle_data)
    for vehicle in vehicle_class_list:
        sql = """INSERT INTO public.vehicle_class(name, date_created, date_modified) VALUES (%s, %s, %s) ON CONFLICT (vehicle_class_id) DO NOTHING"""
        # Execute to insert records into language table
        cur.execute(sql, (vehicle, datetime.datetime.now(), datetime.datetime.now()))
        # Make the changes to the database persistent
        conn.commit()

    # Close cursor
    cur.close()

    # Close connection
    conn.close()

if __name__ == '__main__':
    main()