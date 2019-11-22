import os
import re
from googlemaps import Client

GOOGLE_API_KEY = os.environ.get('GOOGLE_API_KEY')

REGEX = "^-?\d+\.\d+,-?\d+\.\d+$"


def distance_between(origin, destination):
    try:
        origins = [origin]
        destinations = [destination]
        units = 'metric'
        client = Client(key=GOOGLE_API_KEY)
        r = client.distance_matrix(origins, destinations, units=units)
        distance = r['rows'][0]['elements'][0]['distance']
        return distance
    except Exception as e:
        pass


def is_coordinate(coordinate):
    return True if re.match(REGEX, coordinate) else False