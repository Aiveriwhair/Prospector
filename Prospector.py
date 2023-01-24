import googlemaps
import time
from math import acos, sin, cos, radians, degrees

# Location (lat, long)

class Prospector:
    def __init__(self, apiKey):
        self.gmaps = googlemaps.Client(apiKey)

    # Retourne la distance entre deux points (en mètres)
    def CoordDistance(self, location1, location2):

        (latStart, lonStart) = location1
        (latStop, lonStop) = location2

        # Rayon de la terre en mètres
        R = 6371000

        # Conversion des coordonnées en radians
        lat1 = latStart * (3.14159265359 / 180)
        lat2 = latStop * (3.14159265359 / 180)
        lon1 = lonStart * (3.14159265359 / 180)
        lon2 = lonStop * (3.14159265359 / 180)

        # Calcul de la distance (en mètres)
        d = R * acos(sin(lat1) * sin(lat2) + cos(lat1) * cos(lat2) * cos(lon2 - lon1))
        return d

    # Retourne la distance entre deux points en longitude et latitude selon l'axe X et Y (en mètres)
    def CoordDistance2Axes(self, location1, location2):
        (latStart, lonStart) = location1
        (latStop, lonStop) = location2

        dx  = self.CoordDistance((latStart, lonStart), (latStart, lonStop))
        dy  = self.CoordDistance((latStart, lonStart), (latStop, lonStart))
        return (dx,dy)

    # Retourne les coordonnées d'un point après une translation de dx et dy mètres
    def Translate(self, location, dx, dy):
        lat, lon = location
        earth_radius = 6371000 # Earth's radius in meters
        lat_change = dy / earth_radius
        lon_change = dx / (earth_radius * cos(radians(lat)))
        new_lat = lat + degrees(lat_change)
        new_lon = lon + degrees(lon_change)
        return (new_lat, new_lon)

    # Retourne l'ensemble des ID des places dans un rayon de radius mètres autour de location (max 60)
    def get_place_ids(self, location, radius):
        place_ids = []
        next_page_token = None
        while True:
            results = self.gmaps.places_nearby(location, radius, type='', page_token=next_page_token)
            place_ids += [result['place_id'] for result in results['results']]
            next_page_token = results.get('next_page_token')
            if not next_page_token:
                break
            time.sleep(2)
        return place_ids
    
        
    # Scan une zone pour trouver TOUS les lieux de types demandés
    def ScanZonePlacesId(self, location1, location2, radius, types):
        place_ids = []
        
        # On récupère la distance entre les deux points selon X et Y
        (dx, dy) = self.CoordDistance2Axes(location1, location2)
        incrX = dx / (radius * 2)
        incrY = dy / (radius * 2) 
        currX, currY = (0,0)

        requestTotal = len(types) * incrX * incrY
        print("Total requests: {} -- {}".format(requestTotal, requestTotal * 3))
        print("Expected time to scan: {} minutes".format(requestTotal * 2 / 60))
        x = input("Continue ? Y/N")
        if x != "Y": 
            return
            
        requestCount = 0
        # Tant qu'on est dans la zone
        while (currX < dx):
            currY = 0
            while(currY < dy):
                # On récupère les places a currX et currY pour les types demandés
                for type in types:
                    next_page_token = None
                    while True:
                        requestCount += 1
                        print("Request {}/{} == {}%".format(requestCount, requestTotal, requestCount/requestTotal*100, 2))
                        places = self.gmaps.places_nearby(self.Translate(location1, currX, currY), radius, type=type)
                        # On ajoute les places trouvées
                        place_ids += [result['place_id'] for result in places['results']]
                        if not next_page_token:
                            break
                        next_page_token = places['next_page_token']
                        time.sleep(2)
                # Incrémenter les valeurs de currX et currY
                currY += radius * 2
            currX += radius * 2

        return place_ids

    # Scan une zone pour trouver TOUS les lieux avec les details
    def ScanZonePlaces(self, location1, location2, radius, types, fields):
        place_ids = self.ScanZonePlacesId(location1, location2, radius, types)
        places = []
        requestCount = 0
        requestTotal = len(place_ids)
        x = input("Continue ? Y/N")
        if x != "Y": 
            return
        for place_id in place_ids:
            print("Request {}/{} == {}%".format(requestCount, requestTotal, requestCount/requestTotal*100, 2))
            
            place = self.gmaps.place(place_id, fields=fields)
            places.append(place)
            time.sleep(2)
            requestCount += 1
        return places
        
        