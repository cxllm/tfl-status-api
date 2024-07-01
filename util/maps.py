import requests
import urllib.parse
from math import radians, sin, cos, atan2, sqrt


def get_coordinates(address):
    # get coordinates from open street map
    url = (
        "https://nominatim.openstreetmap.org/search.php?q="
        + urllib.parse.quote(address)
        + "&format=jsonv2"
    )
    response = requests.get(url, headers={"User-Agent": "http"}).json()
    if len(response) == 0:
        return None
    coords = (float(response[0]["lat"]), float(response[0]["lon"]))
    return coords


def get_distance_between(coords1, coords2):
    # the haversine algorithm that I do not understand but works so I'm not complaining
    lat1, lon1 = coords1
    lat2, lon2 = coords2
    lat1, lon1, lat2, lon2 = (
        radians(lat1),
        radians(lon1),
        radians(lat2),
        radians(lon2),
    )
    R = 6371.0  # Earth radius in kilometers
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = (sin(dlat / 2)) ** 2 + cos(lat1) * cos(lat2) * (sin(dlon / 2)) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    km = R * c
    miles = km_to_miles(km)
    return {"km": km, "miles": miles}


def km_to_miles(value, to_miles=True):
    factor = 0.621371
    if to_miles:
        return value * factor
    else:
        return value / factor
