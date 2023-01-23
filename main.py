import Prospector
import Env


key = Env.Env.getKey()
location = Env.Env.getGrenobleLocation()

location1 = (45.187207936661736,5.720326761222223)
location2 = (45.18562697096734,5.721473014913573)
radius = 100
types = ["restaurant"]
fields = ["name", "formatted_address", "formatted_phone_number", "place_id", "plus_code","rating", "url","website"]

prospector = Prospector.Prospector(key)
places = prospector.ScanZonePlaces(location1, location2, radius, types, fields)
f = open("./Dist/places_ids.txt", "w")
for place in places:
    f.write(place['result']['name']  +" : "+ place['result']['website']+"\n")