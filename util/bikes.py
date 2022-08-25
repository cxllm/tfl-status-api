import requests
import xmltodict


def bikes():
    data = requests.get(
        "https://tfl.gov.uk/tfl/syndication/feeds/cycle-hire/livecyclehireupdates.xml"
    ).text
    data = xmltodict.parse(data)["stations"]["station"]
    stations = []
    for station in data:
        stations.append(
            {
                "name": station["name"].replace(" ,", ","),
                "coordinates": {
                    "latitude": float(station["lat"]),
                    "longitude": float(station["long"]),
                },
                "bikes_available": int(station["nbBikes"]),
                "number_of_docks": int(station["nbDocks"]),
                "id": int(station["id"]),
                "terminal_name": station["terminalName"],
            }
        )
    return stations
