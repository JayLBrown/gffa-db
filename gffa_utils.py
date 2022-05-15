import re
import json
from sys import intern

# --------------- CONSTANTS ---------------

UNKNOWNS = ('n/a', 'none', 'unknown', '')
INT_KEYS = ('rotation_period', 'orbital_period', 'population', 'average_lifespan', 'cost_in_credits', 'max_atmosphering_speed', 'crew', 'passengers', 'cargo_capacity', 'consumables', 'MGLT')
FLOAT_KEYS = ('diameter', 'surface_water', 'average_height', 'height', 'mass', 'length', 'hyperdrive_rating')
LIST_KEYS = ('producer', 'terrain', 'skin_colors', 'hair_colors', 'eye_colors', 'people', 'films', 'hair_color', 'skin_color', 'films', 'species', 'vehicles', 'starships', 'manufacturer', 'pilots', 'films')

# --------------- READ JSON ---------------

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

# --------------- WRITE JSON ---------------

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

# --------------- CONVERT TO FLOAT ---------------

def convert_to_float(value):
    """Attempts to convert a string or a number to a float. If unsuccessful
    returns the value unchanged. Note that this function will return True for
    boolean values, faux string boolean values (e.g., "true"), "NaN",
    exponential notation, etc.

    Parameters:
        value (str|int): string or number to be converted

    Returns:
        float: if value successfully converted else returns value unchanged
    """

    try:
        return float(value)
    except ValueError:
        return value

# --------------- CONVERT TO INT ---------------

def convert_to_int(value):
    """Attempts to convert a string or a number to an int. If unsuccessful
    returns the value unchanged. Note that this function will return True for
    boolean values, faux string boolean values (e.g., "true"), "NaN",
    exponential notation, etc.

    Parameters:
        value (str|int): string or number to be converted

    Returns:
        int: if value successfully converted else returns value unchanged
    """

    try:
        return int(value)
    except ValueError:
        return value

# --------------- CONVERT TO LIST ---------------

def convert_to_list(value, delimiter=None):
    """Attempts to convert a string < value > to a list using the provided < delimiter >. Removes
    leading/trailing spaces before converting < value > to a list. If unsuccessful or an exception
    is encountered returns the < value > unchanged.

    Parameters:
        value (str): string to be split.
        delimiter (str): optional delimiter provided for splitting the string

    Returns:
         list: string converted to a list.
    """
    try:
        if delimiter != None:
            return value.strip().split(delimiter)
        else:
            return value.strip().split()
    except:
        return value

# --------------- CONVERT TO NONE ---------------

def convert_to_none(value):
    """Attempts to convert the passed in < value > to < None > if it matches any of the following
    strings: "n/a", "N/A", "none", "None", "unknown" "Unknown" (i.e., a case-insensitive check).
    If no match is obtained or an exception is encountered the < value > is returned unchanged.

    Parameters:
        value (obj): string or number to be converted

    Returns:
        int: if value successfully converted; otherwise returns value unchanged
    """
    unknowns = ('n/a', 'none', 'unknown')
    try:
        if value.lower() in unknowns:
            return None
        else:
            return value
    except:
        return value

# --------------- EXTRACT INDEX FROM URL ---------------

def get_index_from_url(value):
    """Attempts to get numeral index from urls to ease the search across various
    tables while inserting foreign keys.

    Parameters:
        value (obj): url string to extract index from

    Returns:
        int: index extracted from the url
    """
    try:
        print("TESTING")
        print(str(value))
        if type(value) == str:
            return re.findall("\d+", value)[-1]
        else:
            return re.findall("\d+", str(value))[-1]
    except:
        return 1