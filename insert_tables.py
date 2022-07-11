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

# --------------------------------------------- CONVERT DATA ---------------------------------------------

def convert_data(data):
    for key, val in data.items():
        if val in gffa_utils.UNKNOWNS:
                data[key] = gffa_utils.convert_to_none(val)
        elif key in gffa_utils.INT_KEYS:
                    data[key] = gffa_utils.convert_to_int(val)
        elif key in gffa_utils.FLOAT_KEYS:
            data[key] = gffa_utils.convert_to_float(val)
        elif key in gffa_utils.LIST_KEYS:
            data[key] = gffa_utils.convert_to_list(val, ', ')
    return data

# --------------------------------------------- GFFA FILM ---------------------------------------------
# --------------- PREPARE FILM LIST ---------------

def prepare_film_list(film):
    film_list = []
    film_list.append(film["title"])
    film_list.append("description")
    film_attr = {k: film[k] for k in ['episode_id', 'opening_crawl', 'director', 'producer', 'release_date', 'characters', 'planets', 'starships', 'vehicles', 'species']}
    film_list.append(json.dumps(film_attr))
    film_list.append(json.dumps(film))
    film_list.append(datetime.datetime.now())
    film_list.append(datetime.datetime.now())
    return film_list

# --------------------------------------------- GFFA PLANET ---------------------------------------------
# --------------- PREPARE PLANET LIST ---------------

def prepare_planet_list(planet):
    planet_list = []
    planet_list.append(planet["name"])
    planet_list.append("description")
    planet_attr = {k: planet[k] for k in ['rotation_period', 'orbital_period', 'diameter', 'climate', 'gravity', 'terrain', 'surface_water', 'population', 'residents', 'films']}
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
        if species["language"] not in unknowns and species["language"] not in result:
            result.append(species["language"])
    return result

# --------------- PREPARE SENTIENT_BEING_TYPE LIST ---------------

def prepare_sentient_being_type_list(sentient_being_type):
    sentient_being_type_list = []
    sentient_being_type_list.append(sentient_being_type["name"])
    sentient_being_type_list.append(sentient_being_type["language"])
    sentient_being_type_list.append("description")
    sentient_being_type_attr = {k: sentient_being_type[k] for k in ['classification', 'designation', 'average_height', 'skin_colors', 'hair_colors', 'eye_colors', 'average_lifespan', 'homeworld', 'language', 'people', 'films']}
    sentient_being_type_list.append(json.dumps(sentient_being_type_attr))
    sentient_being_type_list.append(json.dumps(sentient_being_type))
    sentient_being_type_list.append(datetime.datetime.now())
    sentient_being_type_list.append(datetime.datetime.now())
    return sentient_being_type_list

# --------------- PREPARE SENTIENT_BEING LIST ---------------

def prepare_sentient_being_list(sentient_being):
    sentient_being_list = []
    sentient_being_list.append(gffa_utils.get_index_from_url(sentient_being["species"]))
    sentient_being_list.append(gffa_utils.get_index_from_url(sentient_being["homeworld"]))
    sentient_being_list.append(sentient_being["name"])
    sentient_being_list.append(sentient_being["name"])
    sentient_being_list.append("description")
    sentient_being_attr = {k: sentient_being[k] for k in ['height', 'mass', 'hair_color', 'skin_color', 'eye_color', 'birth_year', 'gender', 'films', 'species', 'vehicles', 'starships']}
    sentient_being_list.append(json.dumps(sentient_being_attr))
    sentient_being_list.append(json.dumps(sentient_being))
    sentient_being_list.append(datetime.datetime.now())
    sentient_being_list.append(datetime.datetime.now())
    return sentient_being_list

# --------------------------------------------- GFFA VEHICLE ---------------------------------------------
# --------------- EXTRACT UNIQUE VEHICLE_CLASS DATA ---------------

def extract_vehicle_class_list(vehicle_data):
    unknowns = ('n/a', 'none', 'unknown')
    result = []
    for vehicle in vehicle_data:
        if vehicle["vehicle_class"] not in unknowns and vehicle["vehicle_class"] not in result:
            result.append(vehicle["vehicle_class"])
    return result

# --------------- PREPARE VEHICLE LIST ---------------

def prepare_vehicle_list(vehicle):
    vehicle_list = []
    vehicle_list.append(vehicle["vehicle_class"])
    vehicle_list.append(vehicle["model"])
    vehicle_list.append("description")
    vehicle_attr = {k: vehicle[k] for k in ['model']}
    vehicle_list.append(json.dumps(vehicle_attr))
    vehicle_list.append(json.dumps(vehicle))
    vehicle_list.append(datetime.datetime.now())
    vehicle_list.append(datetime.datetime.now())
    return vehicle_list


def main():

    # Connect to an existing database
    conn = psycopg2.connect(f"dbname=gffa_db user={secrets.POSTGRES_USERNAME} password={secrets.POSTGRES_PASSWORD}")

    # Open a cursor to perform database operations
    cur = conn.cursor()

    # --------------- INSERT INTO FILM TABLE ---------------

    for film in film_data:
        film_list = prepare_film_list(convert_data(film))
        sql = """INSERT INTO public.film(title, description, attributes, attributes_orig, date_created, date_modified) VALUES (%s, %s, %s, %s, %s, %s) ON CONFLICT (title) DO NOTHING"""
        # Execute to insert records into film table
        cur.execute(sql, film_list)
        # Make the changes to the database persistent
        conn.commit()

    # --------------- INSERT INTO PLANET TABLE ---------------

    for planet in planet_data:
        if planet["name"] != "unknown":
            planet_list = prepare_planet_list(convert_data(planet))
            sql = """INSERT INTO public.planet(name, description, attributes, attributes_orig, date_created, date_modified) VALUES (%s, %s, %s, %s, %s, %s) ON CONFLICT (name) DO NOTHING"""
            # Execute to insert records into planet table
            cur.execute(sql, planet_list)
            # Make the changes to the database persistent
            conn.commit()
    
    # --------------- INSERT INTO LANGUAGE TABLE ---------------
    
    language_list = extract_language_list(species_data)
    for lang in language_list:
        sql = """INSERT INTO public.language(name, date_created, date_modified) VALUES (%s, %s, %s) ON CONFLICT (name) DO NOTHING"""
        # Execute to insert records into language table
        cur.execute(sql, (lang, datetime.datetime.now(), datetime.datetime.now()))
        # Make the changes to the database persistent
        conn.commit()
    
    # --------------- INSERT INTO SENTIENT_BEING_TYPE TABLE ---------------
    
    for species in species_data:
        sentient_being_type_list = prepare_sentient_being_type_list(convert_data(species))
        # Fetching language_id from language table
        # If language is None, it will assign id 34 made for None
        if sentient_being_type_list[1]!=None:
            sql = """SELECT language_id from public.language WHERE name=%s"""
            cur.execute(sql, (sentient_being_type_list[1],))
            sentient_being_type_list[1] = cur.fetchone()
        else:
            sentient_being_type_list[1] = 1
        sql = """INSERT INTO public.sentient_being_type(name, language_id, description, attributes, attributes_orig, date_created, date_modified) VALUES (%s, %s, %s, %s, %s, %s, %s) ON CONFLICT (name) DO NOTHING"""
        # Execute to insert records into sentient_being_type table
        cur.execute(sql, sentient_being_type_list)
        # Make the changes to the database persistent
        conn.commit()
    
    # --------------- INSERT INTO SENTIENT_BEING TABLE ---------------

    for people in people_data:
        sentient_being_list = prepare_sentient_being_list(convert_data(people))
        sql = """INSERT INTO public.sentient_being(sentient_being_type_id, home_world_id, name_first, name_last, description, attributes, attributes_orig, date_created, date_modified) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s) ON CONFLICT (name_first, name_last) DO NOTHING"""
        # Execute to insert records into sentient_being table
        cur.execute(sql, sentient_being_list)
        # Make the changes to the database persistent
        conn.commit()

    # --------------- INSERT INTO VEHICLE_CLASS TABLE ---------------

    vehicle_class_list = extract_vehicle_class_list(vehicle_data)
    for vehicle in vehicle_class_list:
        sql = """INSERT INTO public.vehicle_class(name, date_created, date_modified) VALUES (%s, %s, %s) ON CONFLICT (name) DO NOTHING"""
        # Execute to insert records into vehicle_class table
        cur.execute(sql, (vehicle, datetime.datetime.now(), datetime.datetime.now()))
        # Make the changes to the database persistent
        conn.commit()

    # --------------- INSERT INTO VEHICLE_TYPE TABLE ---------------

    vehicle_type_list = ["Aerial", "Aquatic", "Ground", "Space"]
    for vehicle in vehicle_type_list:
        sql = """INSERT INTO public.vehicle_type(name, date_created, date_modified) VALUES (%s, %s, %s) ON CONFLICT (name) DO NOTHING"""
        # Execute to insert records into vehicle_type table
        cur.execute(sql, (vehicle, datetime.datetime.now(), datetime.datetime.now()))
        # Make the changes to the database persistent
        conn.commit()
    
    # --------------- INSERT INTO VEHICLE TABLE ---------------

    for vehicle in vehicle_data:
        vehicle_list = prepare_vehicle_list(vehicle)
        # Fetching vehicle_class_id from vehicle_class
        sql = """SELECT vehicle_class_id from public.vehicle_class WHERE name=%s"""
        cur.execute(sql, (vehicle_list[0],))
        vehicle_list[0] = cur.fetchone()
        sql = """INSERT INTO public.vehicle(vehicle_class_id, model, description, attributes, attributes_orig, date_created, date_modified) VALUES (%s, %s, %s, %s, %s, %s, %s) ON CONFLICT (model) DO NOTHING"""
        # Execute to insert records into vehicle table
        cur.execute(sql, vehicle_list)
        # Make the changes to the database persistent
        conn.commit()

    # Close cursor
    cur.close()

    # Close connection
    conn.close()

if __name__ == '__main__':
    main()