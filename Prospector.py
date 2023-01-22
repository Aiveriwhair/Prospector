import googlemaps
import time
from math import acos, sin, cos

# Location (lat, long)

class Prospector:
    def __init__(self, apiKey):
        self.gmaps = googlemaps.Client(apiKey)

    # Retourne la distance entre deux points (en mètres)
    def CoordDistance(location1, location2):

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

        dx  = self.CoordDistance(lonStart, latStart, lonStop, latStart)
        dy  = self.CoordDistance(lonStart, latStart, lonStart, latStop)
        return (dx,dy)

    # Retourne les coordonnées d'un point après une translation de dx et dy mètres
    def Translate(self, location, dx, dy):
        return

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
    
        
    # Scan une zone pour trouver TOUTES les places
    def ScanZonePlaces(self, gmapsClient, longStart, latStart, longStop, latStop, radius, types):
        place_ids = []
        next_page_token = None

        # On récupère la distance entre les deux points selon X et Y
        (dx, dy) = self.CoordDistance2Axes(latStart, longStart, latStop, longStop)
        incrX = dx / radius
        incrY = dy / radius
        currX, currY = (0,0)
        # Tant qu'on est dans la zone
        while (currX < dx and currY < dy):
            # On récupère les places a currX et currY pour les types demandés
            for type in types:
                places = gmapsClient.places_nearby((latStart + currY, longStart + currX), radius, type=type)
                # On ajoute les places trouvées
                place_ids += [result['place_id'] for result in places['results']]
                next_page_token = places['next_page_token']
                if not next_page_token:
                    break
            # Incrémenter les valeurs de currX et currY
            currX += incrX
            currY += incrY
        
        