import requests
import json
import psycopg2
import gffa_utils

# --------------- CREATE FILM ATTRIBUTES ---------------

def create_film_attributes(film_data):
    unknowns = ('n/a', 'none', 'unknown')
    list_keys = ('producer', 'characters', 'planets', 'starships', 'vehicles', 'species')
    film_attr = {}
    for film in film_data:
        for key, val in film.items():
            if key in unknowns:
                    film[key] = None
            elif key in list_keys:
                film[key] = gffa_utils.convert_to_list(val, ', ')
    return film_data

def main():

    # Connect to an existing database
    conn = psycopg2.connect("dbname=gffa_db user=postgres password=postgres")

    # Open a cursor to perform database operations
    cur = conn.cursor()

    # --------------- Query to insert records into film table ---------------

    # Read film data from swapi_films.json
    film_data = gffa_utils.read_json('./data/swapi_json/swapi_films.json')

    #insertion process
    for film in film_data:
        film_attr = create_film_attributes(film)
        sql = """INSERT INTO public.film(title, description, attributes, date_created, date_modified) VALUES (%s, %s, %s, %s, %s) ON CONFLICT (attributes) DO NOTHING"""
        print(film_attr)
        # Execute to insert records into film table
        # cur.execute(sql, film_list)
        # Make the changes to the database persistent
        # conn.commit()

    # # --------------- Query to insert records into person table ---------------

    # # Read person data from swapi_people.json
    # person_data = read_json('./data/swapi_json/swapi_people.json')

    # # insertion process
    # for person in person_data:
    #     person_list = get_rearranged_list(person)
    #     sql = """INSERT INTO public.person(url, name, height, mass, hair_color, skin_color, eye_color, birth_year, gender, homeworld, films, species, vehicles, starships, created, edited, raw_json) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) ON CONFLICT (url) DO NOTHING"""
    #     # Execute to insert records into person table
    #     cur.execute(sql, person_list)
    #     # Make the changes to the database persistent
    #     conn.commit()

    # # --------------- Query to insert records into planet table ---------------

    # # Read person data from swapi_planets.json
    # planet_data = read_json('./data/swapi_json/swapi_planets.json')

    # # insertion process
    # for planet in planet_data:
    #     planet_list = get_rearranged_list(planet)
    #     sql = """INSERT INTO public.planet(url, name, rotation_period, orbital_period, diameter, climate, gravity, terrain, surface_water, population, residents, films, created, edited, raw_json) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) ON CONFLICT (url) DO NOTHING"""
    #     # Execute to insert records into planet table
    #     cur.execute(sql, planet_list)
    #     # Make the changes to the database persistent
    #     conn.commit()

    # Close cursor
    cur.close()

    # Close connection
    conn.close()

if __name__ == '__main__':
    main()