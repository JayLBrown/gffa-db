import requests
import json
import psycopg2

def read_json(filepath, encoding='utf-8'):
    """Reads a JSON document, decodes the file content, and returns a
    dictionary if provided with a valid filepath.

    Parameters:
        filepath (str): path to file

    Returns:
        dict: dict representations of the decoded JSON document
    """

    with open(filepath, 'r', encoding=encoding) as file_obj:
        return json.load(file_obj)

def write_json(filepath, data, encoding='utf-8', ensure_ascii=False, indent=2):
    """Serializes object as JSON. Writes content to the provided filepath.

    Parameters:
        filepath (str): the path to the file
        data (dict)/(list): the data to be encoded as JSON and written to the file
        encoding (str): name of encoding used to encode the file
        ensure_ascii (str): if False non-ASCII characters are printed as is; otherwise
                            non-ASCII characters are escaped.
        indent (int): number of "pretty printed" indention spaces applied to encoded JSON

    Returns:
        None
    """

    with open(filepath, 'w', encoding=encoding) as file_obj:
        json.dump(data, file_obj, ensure_ascii=ensure_ascii, indent=indent)

def get_cleaned_list(data):
    """Takes dictionary data and converts its values it into list. Then rearranges the order of elements as per the database column order.

    Parameters:
        data (dict): one dict data from the whole json read file

    Returns:
        result (list): list of rearranged values as per database columns
    """
    result = []
    data = list(data.values())
    result.append(data[13])
    for i in data[:-1]:
        result.append(i)
    result.append(json.dumps(data))
    print(len(result))
    print(result[-1])
    return result

def main():

    # Connect to an existing database
    conn = psycopg2.connect("dbname=gffa_db user=postgres password=postgres")

    # Open a cursor to perform database operations
    cur = conn.cursor()

    # --------------- Query to insert records into film table ---------------

    # Read film data from swapi_films.json
    film_data = read_json('./data/swapi_json/swapi_films.json')

    #insertion process
    for film in film_data:
        film_list = get_cleaned_list(film)
        sql = """INSERT INTO public.film(url, title, episode_id, opening_crawl, director, producer, release_date, characters, planets, starships, vehicles, species, created, edited, raw_json) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) ON CONFLICT (url) DO NOTHING"""
        # Execute to insert records into film table
        cur.execute(sql, film_list)
        # Make the changes to the database persistent
        conn.commit()

    # # --------------- Query to insert records into person table ---------------

    # # Read person data from swapi_people.json
    # person_data = read_json('./data/swapi_json/swapi_people.json')

    # # insertion process
    # for person in person_data:
    #     person_list = get_cleaned_list(person)
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
    #     planet_list = get_cleaned_list(planet)
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