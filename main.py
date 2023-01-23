import Prospector
import Env


key = Env.Env.getKey()
location = Env.Env.getGrenobleLocation()

location1 = (45.187207936661736,5.720326761222223)
location2 = (45.18162697096734,5.731473014913573)
radius = 100
types = ["restaurant"]

prospector = Prospector.Prospector(key)
place_ids = prospector.ScanZonePlaces(location1, location2, radius, types)
f = open("./Dist/places_ids.txt", "w")