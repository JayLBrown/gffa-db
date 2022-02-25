import gffa_utils

# --------------- Prints all distinct Vehicle Classes ---------------

vehicle_data = gffa_utils.read_json('data/swapi_json/swapi_vehicles.json')
result = []
for vehicle in vehicle_data:
    if vehicle.get('vehicle_class') not in result:
        result.append(vehicle.get('vehicle_class'))
print("\nDistinct Vehicle Classes below: \n")
print(result)

# --------------- Prints all distinct Starship Classes ---------------

starship_data = gffa_utils.read_json('data/swapi_json/swapi_starships.json')
result = []
for starship in starship_data:
    if starship.get('starship_class') not in result:
        result.append(starship.get('starship_class'))
print("\nDistinct Starship Classes below: \n")
print(result)