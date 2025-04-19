class Waypoint:
    def __init__(self,name,lat,lon):
        self.name = name
        self.lat = lat
        self.lon = lon 

def ShowWaypoint(waypoint):
    print('Nombre:{0}, lat:{1}, lon:{2}'
    .format (
        waypoint.name,
        waypoint.lat,
        waypoint.lon
    ))

import math 

def distance(lat1,lat2,lon1,lon2):
    R = 6371.0

    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)

    # Haversine formula
    a = math.sin(delta_phi / 2)**2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    distance = R * c
    return distance

