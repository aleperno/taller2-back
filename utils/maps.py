import os
import re
from googlemaps import Client

GOOGLE_API_KEY = os.environ.get('GOOGLE_API_KEY')

REGEX = "^-?\d+\.\d+,-?\d+\.\d+$"

GARCIA_CASTRO = "-34.5865603,-58.4474571"
BUEN_LIBRO = "-34.600452,-58.372497"
PIZZERIA = "-34.571691,-58.4441975"
PANADERIA = "-34.5627322,-58.4564323"


def _extract_row_data(row):
    data = {
        'distance': None,
        'status': False,
        'duration': None
    }

    for d in row['elements']:
        for k,v in d.items():
            if k == 'status':
                data['status'] = (v == 'OK')
            else:
                data[k] = v['value']
    return data


def distance_between(origins: list, destination: str):
    if not origins or not destination:
        return None
    client = Client(key=GOOGLE_API_KEY)
    try:
        destinations = [destination]
        units = 'metric'
        raw = client.distance_matrix(origins, destinations, units=units)
        return [_extract_row_data(row) for row in raw['rows']]
    except Exception as e:
        return None


def is_coordinate(coordinate):
    return True if re.match(REGEX, coordinate) else False